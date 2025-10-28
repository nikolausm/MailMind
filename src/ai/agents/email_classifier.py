"""
Email Classifier Agent
Categorizes and prioritizes incoming emails using AI
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import json
import os
from dotenv import load_dotenv

load_dotenv()


class EmailCategory(Enum):
    WORK = "work"
    PERSONAL = "personal"
    FINANCE = "finance"
    NEWSLETTER = "newsletter"
    SPAM = "spam"
    SOCIAL = "social"
    OTHER = "other"


class Priority(Enum):
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Sentiment(Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@dataclass
class ClassificationResult:
    category: str
    priority: str
    confidence: float
    tags: List[str]
    sentiment: str
    reasoning: Optional[str] = None

    def to_dict(self):
        return asdict(self)


class EmailClassifierAgent:
    """
    AI-powered email classifier using LLM
    Supports both OpenAI and Anthropic models
    """

    def __init__(self, provider: str = None, model: str = None):
        self.provider = provider or os.getenv("LLM_PROVIDER", "openai")
        self.model = model or os.getenv("LLM_MODEL", "gpt-4")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.3"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "1000"))

        # Initialize LLM client
        self._init_client()

    def _init_client(self):
        """Initialize the appropriate LLM client"""
        if self.provider == "openai":
            import openai
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif self.provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _create_classification_prompt(self, email_data: Dict[str, Any]) -> str:
        """Create the classification prompt"""
        subject = email_data.get("subject", "")
        sender = email_data.get("sender_email", "")
        body = email_data.get("body_text", "")[:1000]  # Limit body length

        prompt = f"""Analyze the following email and classify it:

Subject: {subject}
From: {sender}
Body: {body}

Provide a JSON response with:
1. category: one of [work, personal, finance, newsletter, spam, social, other]
2. priority: one of [urgent, high, medium, low]
3. sentiment: one of [positive, neutral, negative]
4. tags: array of relevant tags (3-5 tags)
5. confidence: float between 0 and 1
6. reasoning: brief explanation of the classification

Example response:
{{
  "category": "work",
  "priority": "high",
  "sentiment": "positive",
  "tags": ["meeting", "project", "deadline"],
  "confidence": 0.92,
  "reasoning": "Email is about a work meeting with project deadlines"
}}

Respond ONLY with valid JSON, no other text."""

        return prompt

    async def classify(self, email_data: Dict[str, Any]) -> ClassificationResult:
        """
        Classify an email using LLM

        Args:
            email_data: Dictionary containing email information
                - subject: Email subject
                - sender_email: Sender email address
                - body_text: Email body text

        Returns:
            ClassificationResult with category, priority, tags, etc.
        """
        try:
            prompt = self._create_classification_prompt(email_data)

            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an email classification assistant. Always respond with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    response_format={"type": "json_object"}
                )
                result_text = response.choices[0].message.content

            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                result_text = response.content[0].text

            # Parse JSON response
            result_data = json.loads(result_text)

            return ClassificationResult(
                category=result_data.get("category", "other"),
                priority=result_data.get("priority", "medium"),
                sentiment=result_data.get("sentiment", "neutral"),
                tags=result_data.get("tags", []),
                confidence=result_data.get("confidence", 0.5),
                reasoning=result_data.get("reasoning")
            )

        except json.JSONDecodeError as e:
            print(f"Error parsing LLM response: {e}")
            # Return default classification on error
            return self._default_classification()

        except Exception as e:
            print(f"Error during classification: {e}")
            return self._default_classification()

    def _default_classification(self) -> ClassificationResult:
        """Return default classification on error"""
        return ClassificationResult(
            category="other",
            priority="medium",
            sentiment="neutral",
            tags=["unclassified"],
            confidence=0.0,
            reasoning="Classification failed, using defaults"
        )
