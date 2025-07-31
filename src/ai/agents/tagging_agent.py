"""
Tagging Agent for automatic email tagging
"""

from typing import List, Dict, Set
from collections import defaultdict
import re

class TaggingAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.tag_hierarchy = self._initialize_tag_hierarchy()
        
    def _initialize_tag_hierarchy(self) -> Dict[str, List[str]]:
        """Initialize the hierarchical tag structure"""
        return {
            "work": ["project", "meeting", "report", "deadline", "review"],
            "personal": ["family", "friends", "health", "travel", "shopping"],
            "finance": ["invoice", "payment", "budget", "expense", "receipt"],
            "communication": ["request", "update", "announcement", "feedback", "question"]
        }
        
    async def generate_tags(self, email_content: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Generate tags for an email
        
        Returns:
            Dict with 'automatic' and 'suggested' tag lists
        """
        automatic_tags = self._extract_automatic_tags(email_content)
        suggested_tags = await self._generate_ai_tags(email_content)
        
        return {
            "automatic": list(automatic_tags),
            "suggested": suggested_tags
        }
        
    def _extract_automatic_tags(self, email_content: Dict[str, str]) -> Set[str]:
        """Extract tags based on patterns and keywords"""
        tags = set()
        
        # Extract from subject and body
        text = f"{email_content.get('subject', '')} {email_content.get('body', '')}".lower()
        
        # Pattern-based extraction
        if re.search(r'\b(invoice|bill|payment)\b', text):
            tags.add("finance")
        if re.search(r'\b(meeting|conference|call)\b', text):
            tags.add("meeting")
        if re.search(r'\b(deadline|due date|by \d+)\b', text):
            tags.add("deadline")
            
        return tags
