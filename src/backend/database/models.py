"""
SQLAlchemy database models for MailMind
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model for authentication (future implementation)"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    emails = relationship("Email", back_populates="user")


class Email(Base):
    """Email model storing email content and basic metadata"""
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Email headers
    message_id = Column(String(500), unique=True, index=True)
    subject = Column(String(500), index=True)
    sender_email = Column(String(255), index=True)
    sender_name = Column(String(255))
    recipient_email = Column(String(255))
    recipient_name = Column(String(255))
    cc = Column(JSON)  # List of CC recipients
    bcc = Column(JSON)  # List of BCC recipients

    # Email content
    body_text = Column(Text)  # Plain text version
    body_html = Column(Text)  # HTML version

    # Timestamps
    received_date = Column(DateTime, index=True)
    sent_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Flags
    is_read = Column(Boolean, default=False)
    is_starred = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    # Attachments metadata (stored as JSON)
    attachments = Column(JSON, default=list)

    # Relationships
    user = relationship("User", back_populates="emails")
    metadata = relationship("EmailMetadata", back_populates="email", uselist=False)

    def __repr__(self):
        return f"<Email(id={self.id}, subject='{self.subject}', sender='{self.sender_email}')>"


class EmailMetadata(Base):
    """AI-generated metadata for emails"""
    __tablename__ = "email_metadata"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"), unique=True, nullable=False)

    # AI Classification
    category = Column(String(100), index=True)  # e.g., "work", "personal", "finance", "social"
    priority = Column(String(20), index=True)  # e.g., "urgent", "high", "medium", "low"
    sentiment = Column(String(20))  # e.g., "positive", "negative", "neutral"
    confidence_score = Column(Float)  # 0.0 to 1.0

    # AI-generated tags
    tags = Column(JSON, default=list)  # List of tags

    # AI-generated summary
    summary = Column(Text)
    key_points = Column(JSON, default=list)  # List of key points

    # Action items and entities
    action_items = Column(JSON, default=list)  # List of detected action items
    entities = Column(JSON, default=dict)  # Extracted entities (people, dates, locations, etc.)

    # Embedding reference (vector stored in Weaviate)
    embedding_id = Column(String(255), index=True)  # Reference to vector in Weaviate

    # Processing metadata
    processed_at = Column(DateTime, default=datetime.utcnow)
    processing_duration = Column(Float)  # Processing time in seconds
    model_version = Column(String(50))  # e.g., "gpt-4", "claude-3-sonnet"

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    email = relationship("Email", back_populates="metadata")

    def __repr__(self):
        return f"<EmailMetadata(email_id={self.email_id}, category='{self.category}', priority='{self.priority}')>"
