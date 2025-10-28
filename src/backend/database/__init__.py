"""
Database module for MailMind
"""

from .session import engine, SessionLocal, get_db, init_db
from .models import Email, EmailMetadata, User

__all__ = [
    "engine",
    "SessionLocal",
    "get_db",
    "init_db",
    "Email",
    "EmailMetadata",
    "User",
]
