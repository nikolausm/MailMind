"""
Email API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import List, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from backend.database import get_db, Email, EmailMetadata
from backend.database.schemas import (
    Email as EmailSchema,
    EmailCreate,
    EmailUpdate,
    EmailList,
    ClassificationRequest,
    SearchQuery,
    SearchResponse,
    SearchResult
)
from ai.agents.email_classifier import EmailClassifierAgent
from ai.agents.search_agent import SearchAgent
from backend.vector_db import get_weaviate_client

router = APIRouter(prefix="/emails", tags=["emails"])

# Initialize agents (will be done in lifespan in main.py, but for now we'll initialize here)
classifier_agent = None
search_agent = None


def get_classifier_agent():
    """Get or create classifier agent"""
    global classifier_agent
    if classifier_agent is None:
        classifier_agent = EmailClassifierAgent()
    return classifier_agent


def get_search_agent():
    """Get or create search agent"""
    global search_agent
    if search_agent is None:
        weaviate_client = get_weaviate_client()
        search_agent = SearchAgent(weaviate_client)
        if weaviate_client:
            search_agent.initialize_schema()
    return search_agent


@router.get("/", response_model=EmailList)
async def list_emails(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    priority: Optional[str] = None,
    is_read: Optional[bool] = None,
    is_starred: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    List emails with optional filtering

    - **skip**: Number of emails to skip (pagination)
    - **limit**: Maximum number of emails to return
    - **category**: Filter by category
    - **priority**: Filter by priority
    - **is_read**: Filter by read status
    - **is_starred**: Filter by starred status
    """
    query = db.query(Email).filter(Email.is_deleted == False)

    # Apply filters
    if is_read is not None:
        query = query.filter(Email.is_read == is_read)
    if is_starred is not None:
        query = query.filter(Email.is_starred == is_starred)

    # Join with metadata for category/priority filters
    if category or priority:
        query = query.join(EmailMetadata)
        if category:
            query = query.filter(EmailMetadata.category == category)
        if priority:
            query = query.filter(EmailMetadata.priority == priority)

    # Get total count
    total = query.count()

    # Get paginated results
    emails = query.order_by(desc(Email.received_date)).offset(skip).limit(limit).all()

    return {
        "total": total,
        "emails": emails,
        "page": (skip // limit) + 1,
        "page_size": limit
    }


@router.get("/{email_id}", response_model=EmailSchema)
async def get_email(email_id: int, db: Session = Depends(get_db)):
    """Get a specific email by ID"""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email


@router.post("/", response_model=EmailSchema, status_code=201)
async def create_email(
    email_data: EmailCreate,
    db: Session = Depends(get_db)
):
    """Create a new email (for testing/import)"""
    email = Email(**email_data.dict(exclude_unset=True))
    db.add(email)
    db.commit()
    db.refresh(email)
    return email


@router.patch("/{email_id}", response_model=EmailSchema)
async def update_email(
    email_id: int,
    email_update: EmailUpdate,
    db: Session = Depends(get_db)
):
    """Update email flags (read, starred, archived, deleted)"""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    # Update only provided fields
    update_data = email_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(email, field, value)

    db.commit()
    db.refresh(email)
    return email


@router.delete("/{email_id}")
async def delete_email(email_id: int, db: Session = Depends(get_db)):
    """Soft delete an email"""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    email.is_deleted = True
    db.commit()
    return {"message": "Email deleted successfully"}


@router.post("/{email_id}/classify")
async def classify_email(
    email_id: int,
    request: ClassificationRequest,
    db: Session = Depends(get_db)
):
    """
    Classify an email using AI

    Generates category, priority, sentiment, tags, and stores in metadata
    """
    # Get email
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    # Check if already classified
    if email.metadata and not request.force_reclassify:
        return {
            "message": "Email already classified",
            "metadata": email.metadata
        }

    # Classify email
    classifier = get_classifier_agent()
    classification = await classifier.classify({
        "subject": email.subject,
        "sender_email": email.sender_email,
        "body_text": email.body_text or ""
    })

    # Store or update metadata
    if email.metadata:
        metadata = email.metadata
        metadata.category = classification.category
        metadata.priority = classification.priority
        metadata.sentiment = classification.sentiment
        metadata.tags = classification.tags
        metadata.confidence_score = classification.confidence
    else:
        metadata = EmailMetadata(
            email_id=email.id,
            category=classification.category,
            priority=classification.priority,
            sentiment=classification.sentiment,
            tags=classification.tags,
            confidence_score=classification.confidence
        )
        db.add(metadata)

    db.commit()
    db.refresh(email)

    return {
        "message": "Email classified successfully",
        "classification": classification.to_dict(),
        "metadata": email.metadata
    }


@router.post("/search", response_model=SearchResponse)
async def search_emails(
    search_query: SearchQuery,
    db: Session = Depends(get_db)
):
    """
    Perform semantic search on emails

    Uses vector embeddings for semantic similarity
    """
    import time
    start_time = time.time()

    # Get search agent
    search = get_search_agent()

    # Perform search
    results = await search.search(
        query=search_query.query,
        filters=search_query.filters,
        top_k=search_query.limit
    )

    # Fetch full email data from database
    email_ids = [r.email_id for r in results]
    emails = db.query(Email).filter(Email.id.in_(email_ids)).all()
    email_dict = {e.id: e for e in emails}

    # Combine search results with email data
    search_results = []
    for result in results:
        if result.email_id in email_dict:
            email = email_dict[result.email_id]
            search_results.append(
                SearchResult(
                    email=email,
                    score=result.score,
                    highlights={"snippet": result.snippet}
                )
            )

    processing_time = time.time() - start_time

    return SearchResponse(
        query=search_query.query,
        total=len(search_results),
        results=search_results,
        processing_time=processing_time
    )


@router.post("/batch-classify")
async def batch_classify_emails(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Classify multiple unclassified emails in batch

    Useful for processing newly imported emails
    """
    # Get unclassified emails
    emails = (
        db.query(Email)
        .filter(Email.is_deleted == False)
        .outerjoin(EmailMetadata)
        .filter(EmailMetadata.id == None)
        .limit(limit)
        .all()
    )

    if not emails:
        return {"message": "No unclassified emails found", "classified": 0}

    classifier = get_classifier_agent()
    search = get_search_agent()
    classified_count = 0

    for email in emails:
        try:
            # Classify
            classification = await classifier.classify({
                "subject": email.subject,
                "sender_email": email.sender_email,
                "body_text": email.body_text or ""
            })

            # Store metadata
            metadata = EmailMetadata(
                email_id=email.id,
                category=classification.category,
                priority=classification.priority,
                sentiment=classification.sentiment,
                tags=classification.tags,
                confidence_score=classification.confidence
            )
            db.add(metadata)

            # Generate and store embedding
            if search.weaviate_client:
                embedding_id = search.add_email_embedding({
                    "id": email.id,
                    "subject": email.subject,
                    "body_text": email.body_text,
                    "sender_email": email.sender_email,
                    "category": classification.category,
                    "priority": classification.priority,
                    "tags": classification.tags
                })
                if embedding_id:
                    metadata.embedding_id = embedding_id

            classified_count += 1

        except Exception as e:
            print(f"Error classifying email {email.id}: {e}")
            continue

    db.commit()

    return {
        "message": f"Classified {classified_count} emails",
        "classified": classified_count,
        "total_requested": len(emails)
    }


@router.get("/stats/overview")
async def get_stats(db: Session = Depends(get_db)):
    """Get email statistics for dashboard"""
    total_emails = db.query(Email).filter(Email.is_deleted == False).count()
    unread_count = db.query(Email).filter(
        Email.is_deleted == False,
        Email.is_read == False
    ).count()
    starred_count = db.query(Email).filter(
        Email.is_deleted == False,
        Email.is_starred == True
    ).count()

    # Category breakdown
    category_stats = (
        db.query(EmailMetadata.category, db.func.count(EmailMetadata.id))
        .group_by(EmailMetadata.category)
        .all()
    )

    # Priority breakdown
    priority_stats = (
        db.query(EmailMetadata.priority, db.func.count(EmailMetadata.id))
        .group_by(EmailMetadata.priority)
        .all()
    )

    return {
        "total": total_emails,
        "unread": unread_count,
        "starred": starred_count,
        "by_category": {cat: count for cat, count in category_stats},
        "by_priority": {pri: count for pri, count in priority_stats}
    }
