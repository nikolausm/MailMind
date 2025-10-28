"""
Pydantic schemas for API request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Email Schemas
class EmailBase(BaseModel):
    subject: str
    sender_email: EmailStr
    sender_name: Optional[str] = None
    recipient_email: Optional[EmailStr] = None
    recipient_name: Optional[str] = None
    cc: Optional[List[str]] = Field(default_factory=list)
    bcc: Optional[List[str]] = Field(default_factory=list)
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    received_date: Optional[datetime] = None
    sent_date: Optional[datetime] = None
    attachments: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


class EmailCreate(EmailBase):
    """Schema for creating a new email"""
    message_id: Optional[str] = None


class EmailUpdate(BaseModel):
    """Schema for updating email flags"""
    is_read: Optional[bool] = None
    is_starred: Optional[bool] = None
    is_archived: Optional[bool] = None
    is_deleted: Optional[bool] = None


class EmailMetadataBase(BaseModel):
    category: Optional[str] = None
    priority: Optional[str] = None
    sentiment: Optional[str] = None
    confidence_score: Optional[float] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    summary: Optional[str] = None
    key_points: Optional[List[str]] = Field(default_factory=list)
    action_items: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    entities: Optional[Dict[str, Any]] = Field(default_factory=dict)


class EmailMetadata(EmailMetadataBase):
    id: int
    email_id: int
    embedding_id: Optional[str] = None
    processed_at: datetime
    processing_duration: Optional[float] = None
    model_version: Optional[str] = None

    class Config:
        from_attributes = True


class Email(EmailBase):
    """Full email schema with metadata"""
    id: int
    message_id: Optional[str] = None
    is_read: bool
    is_starred: bool
    is_archived: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    metadata: Optional[EmailMetadata] = None

    class Config:
        from_attributes = True


class EmailList(BaseModel):
    """Schema for email list response"""
    total: int
    emails: List[Email]
    page: int = 1
    page_size: int = 50


# Search Schemas
class SearchQuery(BaseModel):
    """Schema for search requests"""
    query: str
    limit: int = Field(default=20, ge=1, le=100)
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict)


class SearchResult(BaseModel):
    """Schema for search result item"""
    email: Email
    score: float
    highlights: Optional[Dict[str, str]] = Field(default_factory=dict)


class SearchResponse(BaseModel):
    """Schema for search response"""
    query: str
    total: int
    results: List[SearchResult]
    processing_time: float


# Classification Request
class ClassificationRequest(BaseModel):
    """Request to classify an email"""
    email_id: int
    force_reclassify: bool = False
