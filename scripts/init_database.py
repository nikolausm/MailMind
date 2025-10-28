"""
Initialize database and load sample data
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.backend.database.session import engine, SessionLocal
from src.backend.database.models import Base, Email, EmailMetadata, User
from sqlalchemy.exc import IntegrityError


def create_tables():
    """Create all database tables"""
    print("📊 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")


def create_test_user(db):
    """Create a test user"""
    print("\n👤 Creating test user...")
    user = User(
        email="user@mailmind.local",
        full_name="Test User",
        is_active=True
    )
    db.add(user)
    db.commit()
    print("✅ Test user created")
    return user


def load_sample_emails(db, user_id: int, filename: str = "data/sample_emails.json"):
    """Load sample emails from JSON file"""
    print(f"\n📧 Loading sample emails from {filename}...")

    try:
        with open(filename, "r") as f:
            emails_data = json.load(f)

        loaded_count = 0
        for email_data in emails_data:
            try:
                # Create email
                email = Email(
                    user_id=user_id,
                    message_id=email_data["message_id"],
                    subject=email_data["subject"],
                    sender_email=email_data["sender_email"],
                    sender_name=email_data["sender_name"],
                    recipient_email=email_data["recipient_email"],
                    recipient_name=email_data["recipient_name"],
                    body_text=email_data["body_text"],
                    body_html=email_data["body_html"],
                    received_date=datetime.fromisoformat(email_data["received_date"]),
                    sent_date=datetime.fromisoformat(email_data["sent_date"]),
                    is_read=email_data["is_read"],
                    is_starred=email_data["is_starred"],
                )
                db.add(email)
                db.flush()  # Get the email ID

                # Create metadata (will be populated by AI agents later)
                metadata = EmailMetadata(
                    email_id=email.id,
                    category=email_data.get("category"),
                    priority=email_data.get("priority"),
                    tags=email_data.get("tags", []),
                    confidence_score=1.0,  # Mock data is 100% confident
                    processed_at=datetime.utcnow(),
                )
                db.add(metadata)

                loaded_count += 1

            except IntegrityError as e:
                db.rollback()
                print(f"⚠️  Skipping duplicate email: {email_data['message_id']}")
                continue

        db.commit()
        print(f"✅ Loaded {loaded_count} emails successfully")

    except FileNotFoundError:
        print(f"❌ Sample data file not found: {filename}")
        print("💡 Run: python scripts/generate_sample_emails.py first")
        sys.exit(1)


def main():
    """Main initialization function"""
    print("🚀 MailMind Database Initialization\n")
    print("=" * 50)

    # Create tables
    create_tables()

    # Create database session
    db = SessionLocal()

    try:
        # Create test user
        user = create_test_user(db)

        # Load sample emails
        load_sample_emails(db, user.id)

        # Print summary
        email_count = db.query(Email).count()
        print(f"\n" + "=" * 50)
        print(f"✨ Database initialized successfully!")
        print(f"📊 Total emails in database: {email_count}")
        print(f"👤 Test user: user@mailmind.local")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
