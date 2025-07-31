"""
Summary Agent for email thread summarization
"""

from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ThreadSummary:
    thread_id: str
    subject: str
    participants: List[str]
    key_points: List[str]
    action_items: List[str]
    sentiment: str
    summary: str

class SummaryAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        
    async def summarize_thread(self, emails: List[Dict[str, Any]]) -> ThreadSummary:
        """Generate a summary of an email thread"""
        # Sort emails by timestamp
        sorted_emails = sorted(emails, key=lambda x: x['timestamp'])
        
        # Extract key information
        participants = self._extract_participants(sorted_emails)
        
        # Generate summary using LLM
        summary_prompt = self._build_summary_prompt(sorted_emails)
        summary_result = await self.llm_client.generate(summary_prompt)
        
        return ThreadSummary(
            thread_id=sorted_emails[0].get('thread_id'),
            subject=sorted_emails[0].get('subject'),
            participants=participants,
            key_points=summary_result.get('key_points', []),
            action_items=summary_result.get('action_items', []),
            sentiment=summary_result.get('sentiment', 'neutral'),
            summary=summary_result.get('summary', '')
        )
        
    def _extract_participants(self, emails: List[Dict]) -> List[str]:
        """Extract unique participants from email thread"""
        participants = set()
        for email in emails:
            participants.add(email.get('sender'))
            participants.update(email.get('recipients', []))
        return list(participants)
