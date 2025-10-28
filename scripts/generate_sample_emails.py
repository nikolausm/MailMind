"""
Generate sample email dataset for testing
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Sample email templates categorized by type
EMAIL_TEMPLATES = {
    "work": [
        {
            "subject": "Q4 Budget Review Meeting",
            "sender": "sarah.johnson@company.com",
            "sender_name": "Sarah Johnson",
            "body": """Hi Team,

I'd like to schedule our Q4 budget review meeting for next week. Please review the attached spreadsheet and come prepared with your department's spending projections.

Key discussion points:
- Current spending vs. budget
- Q1 2024 projections
- Resource allocation

Best regards,
Sarah""",
            "priority": "high",
            "tags": ["meeting", "finance", "budget"]
        },
        {
            "subject": "Project Milestone Update",
            "sender": "mike.chen@company.com",
            "sender_name": "Mike Chen",
            "body": """Team,

Great news! We've successfully completed Phase 2 of the project, ahead of schedule. The client is very pleased with our progress.

Next steps:
1. Begin Phase 3 development
2. Schedule demo with stakeholders
3. Update project documentation

Let's celebrate this win!

Mike""",
            "priority": "medium",
            "tags": ["project", "milestone", "update"]
        },
        {
            "subject": "URGENT: Server Maintenance Tonight",
            "sender": "ops@company.com",
            "sender_name": "IT Operations",
            "body": """URGENT: Scheduled Maintenance

The production servers will be taken offline tonight from 11 PM to 2 AM for critical security patches.

Please ensure:
- All work is saved before 10:45 PM
- Notify your clients of potential downtime
- Be available for verification after maintenance

Contact the ops team if you have concerns.

IT Operations Team""",
            "priority": "urgent",
            "tags": ["urgent", "IT", "maintenance", "security"]
        },
    ],
    "personal": [
        {
            "subject": "Weekend Plans?",
            "sender": "alex.rivera@email.com",
            "sender_name": "Alex Rivera",
            "body": """Hey!

Hope you're doing well! I was thinking we could grab dinner this weekend. There's a new Italian place downtown that got great reviews.

Are you free Saturday evening around 7?

Let me know!
Alex""",
            "priority": "low",
            "tags": ["social", "dinner", "weekend"]
        },
        {
            "subject": "Happy Birthday! 🎂",
            "sender": "emily.watson@email.com",
            "sender_name": "Emily Watson",
            "body": """Happy Birthday!!!

Wishing you an amazing day filled with joy and laughter. Hope all your wishes come true!

Can't wait to celebrate with you this weekend!

Lots of love,
Emily""",
            "priority": "medium",
            "tags": ["birthday", "celebration", "personal"]
        },
    ],
    "finance": [
        {
            "subject": "Your Monthly Statement is Ready",
            "sender": "statements@bank.com",
            "sender_name": "City Bank",
            "body": """Dear Customer,

Your monthly statement for October 2024 is now available.

Account Summary:
- Starting Balance: $5,234.56
- Total Credits: $3,450.00
- Total Debits: $2,890.12
- Ending Balance: $5,794.44

You can view your full statement online at www.bank.com/statements

City Bank Customer Service""",
            "priority": "medium",
            "tags": ["finance", "statement", "banking"]
        },
        {
            "subject": "Invoice #2024-1056 - Payment Due",
            "sender": "billing@cloudservices.com",
            "sender_name": "Cloud Services Billing",
            "body": """Invoice Details

Invoice Number: 2024-1056
Invoice Date: October 28, 2024
Due Date: November 11, 2024
Amount Due: $299.00

Service Period: October 1-31, 2024
Description: Premium Cloud Hosting Plan

Please ensure payment is received by the due date to avoid service interruption.

Cloud Services Inc.""",
            "priority": "high",
            "tags": ["invoice", "payment", "billing"]
        },
    ],
    "newsletter": [
        {
            "subject": "Weekly Tech Digest - AI Breakthroughs",
            "sender": "newsletter@technews.com",
            "sender_name": "Tech News Daily",
            "body": """This Week in Technology

TOP STORIES:
1. Major AI Model Release Achieves 95% Accuracy
2. New Open Source Framework for ML
3. Quantum Computing Milestone Reached

UPCOMING EVENTS:
- AI Conference 2024 (Nov 15-17)
- DevOps Summit (Dec 1-3)

Read more at www.technews.com

Unsubscribe | Update Preferences""",
            "priority": "low",
            "tags": ["newsletter", "technology", "AI"]
        },
    ],
    "spam": [
        {
            "subject": "You've Won $1,000,000!!!",
            "sender": "winner@lottery-notification.com",
            "sender_name": "Lottery Notification",
            "body": """CONGRATULATIONS!!!

You have been selected as the winner of our $1,000,000 grand prize!

To claim your prize, simply click the link below and provide your banking information.

[CLAIM YOUR PRIZE NOW]

Act fast! This offer expires in 24 hours!

*This is not a scam*""",
            "priority": "low",
            "tags": ["spam", "scam", "phishing"]
        },
    ]
}


def generate_email(category: str, template: Dict[str, Any], days_ago: int) -> Dict[str, Any]:
    """Generate a single email from template"""
    received_date = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))

    return {
        "message_id": f"<{random.randint(10000, 99999)}@mailmind.local>",
        "subject": template["subject"],
        "sender_email": template["sender"],
        "sender_name": template["sender_name"],
        "recipient_email": "user@mailmind.local",
        "recipient_name": "Test User",
        "body_text": template["body"],
        "body_html": f"<html><body><pre>{template['body']}</pre></body></html>",
        "received_date": received_date.isoformat(),
        "sent_date": (received_date - timedelta(minutes=random.randint(1, 30))).isoformat(),
        "is_read": random.choice([True, False]),
        "is_starred": random.choice([True, False]) if random.random() > 0.8 else False,
        "category": category,
        "priority": template["priority"],
        "tags": template["tags"],
    }


def generate_sample_dataset(num_emails: int = 100) -> List[Dict[str, Any]]:
    """Generate a dataset of sample emails"""
    emails = []

    # Calculate distribution
    categories = list(EMAIL_TEMPLATES.keys())
    weights = {
        "work": 0.40,      # 40% work emails
        "personal": 0.25,  # 25% personal emails
        "finance": 0.15,   # 15% finance emails
        "newsletter": 0.15, # 15% newsletters
        "spam": 0.05       # 5% spam
    }

    # Generate emails
    for i in range(num_emails):
        # Select category based on weights
        category = random.choices(categories, weights=[weights[c] for c in categories])[0]
        template = random.choice(EMAIL_TEMPLATES[category])

        # Generate email with varying receive dates (last 30 days)
        days_ago = random.randint(0, 30)
        email = generate_email(category, template, days_ago)
        emails.append(email)

    # Sort by received_date (most recent first)
    emails.sort(key=lambda x: x["received_date"], reverse=True)

    return emails


def save_sample_data(emails: List[Dict[str, Any]], filename: str = "sample_emails.json"):
    """Save sample emails to JSON file"""
    with open(filename, "w") as f:
        json.dump(emails, f, indent=2)
    print(f"✅ Generated {len(emails)} sample emails")
    print(f"📁 Saved to {filename}")


if __name__ == "__main__":
    # Generate 100 sample emails
    sample_emails = generate_sample_dataset(100)

    # Save to file
    save_sample_data(sample_emails, "data/sample_emails.json")

    # Print statistics
    categories = {}
    priorities = {}
    for email in sample_emails:
        cat = email["category"]
        pri = email["priority"]
        categories[cat] = categories.get(cat, 0) + 1
        priorities[pri] = priorities.get(pri, 0) + 1

    print("\n📊 Dataset Statistics:")
    print("\nBy Category:")
    for cat, count in categories.items():
        print(f"  {cat}: {count}")

    print("\nBy Priority:")
    for pri, count in priorities.items():
        print(f"  {pri}: {count}")
