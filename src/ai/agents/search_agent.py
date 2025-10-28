"""
Search Agent for semantic email search using RAG
"""

import numpy as np
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass, asdict
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class SearchResult:
    email_id: int
    score: float
    subject: str
    snippet: str
    metadata: Dict[str, Any]

    def to_dict(self):
        return asdict(self)


class SearchAgent:
    """
    Semantic search agent using sentence transformers and Weaviate
    """

    def __init__(self, weaviate_client=None, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize SearchAgent

        Args:
            weaviate_client: Weaviate client instance
            embedding_model: Sentence transformer model name
        """
        self.weaviate_client = weaviate_client
        self.encoder = SentenceTransformer(embedding_model)
        self.collection_name = "EmailEmbedding"

    def initialize_schema(self):
        """Initialize Weaviate schema for email embeddings"""
        if self.weaviate_client is None:
            return

        try:
            # Check if collection exists
            if self.weaviate_client.collections.exists(self.collection_name):
                print(f"✅ Collection '{self.collection_name}' already exists")
                return

            # Create collection
            self.weaviate_client.collections.create(
                name=self.collection_name,
                properties=[
                    {
                        "name": "email_id",
                        "dataType": ["int"],
                        "description": "Database email ID",
                    },
                    {
                        "name": "subject",
                        "dataType": ["text"],
                        "description": "Email subject",
                    },
                    {
                        "name": "body_text",
                        "dataType": ["text"],
                        "description": "Email body content",
                    },
                    {
                        "name": "sender_email",
                        "dataType": ["text"],
                        "description": "Sender email address",
                    },
                    {
                        "name": "category",
                        "dataType": ["text"],
                        "description": "Email category",
                    },
                    {
                        "name": "priority",
                        "dataType": ["text"],
                        "description": "Email priority",
                    },
                    {
                        "name": "tags",
                        "dataType": ["text[]"],
                        "description": "Email tags",
                    },
                ]
            )
            print(f"✅ Created collection '{self.collection_name}'")

        except Exception as e:
            print(f"⚠️  Error initializing schema: {e}")

    def add_email_embedding(self, email_data: Dict[str, Any]) -> Optional[str]:
        """
        Generate and store embedding for an email

        Args:
            email_data: Dictionary with email information

        Returns:
            Weaviate object ID if successful, None otherwise
        """
        if self.weaviate_client is None:
            return None

        try:
            # Create text for embedding
            text = f"{email_data.get('subject', '')} {email_data.get('body_text', '')}"
            text = text[:5000]  # Limit text length

            # Generate embedding
            embedding = self.encoder.encode(text)

            # Store in Weaviate
            collection = self.weaviate_client.collections.get(self.collection_name)
            obj_id = collection.data.insert(
                properties={
                    "email_id": email_data.get("id"),
                    "subject": email_data.get("subject", ""),
                    "body_text": email_data.get("body_text", "")[:1000],  # Store snippet
                    "sender_email": email_data.get("sender_email", ""),
                    "category": email_data.get("category", ""),
                    "priority": email_data.get("priority", ""),
                    "tags": email_data.get("tags", []),
                },
                vector=embedding.tolist()
            )

            return str(obj_id)

        except Exception as e:
            print(f"Error adding email embedding: {e}")
            return None

    async def search(
        self,
        query: str,
        filters: Optional[Dict] = None,
        top_k: int = 10
    ) -> List[SearchResult]:
        """
        Perform semantic search on emails

        Args:
            query: Natural language search query
            filters: Optional filters (category, priority, sender, etc.)
            top_k: Number of results to return

        Returns:
            List of SearchResult objects
        """
        if self.weaviate_client is None:
            return []

        try:
            # Generate query embedding
            query_embedding = self.encoder.encode(query)

            # Build Weaviate query
            collection = self.weaviate_client.collections.get(self.collection_name)

            # Perform vector search
            response = collection.query.near_vector(
                near_vector=query_embedding.tolist(),
                limit=top_k,
                return_metadata=["distance"]
            )

            # Format results
            return self._format_results(response.objects, query)

        except Exception as e:
            print(f"Error during search: {e}")
            return []

    def _format_results(self, raw_results, query: str) -> List[SearchResult]:
        """Format Weaviate results into SearchResult objects"""
        results = []

        for obj in raw_results:
            props = obj.properties
            metadata = obj.metadata

            # Calculate similarity score (Weaviate returns distance, convert to similarity)
            distance = metadata.distance if hasattr(metadata, 'distance') else 1.0
            score = 1.0 / (1.0 + distance)  # Convert distance to similarity

            # Create snippet with query highlighting
            body = props.get("body_text", "")
            snippet = self._create_snippet(body, query, max_length=200)

            result = SearchResult(
                email_id=props.get("email_id", 0),
                score=score,
                subject=props.get("subject", ""),
                snippet=snippet,
                metadata={
                    "sender_email": props.get("sender_email", ""),
                    "category": props.get("category", ""),
                    "priority": props.get("priority", ""),
                    "tags": props.get("tags", []),
                }
            )
            results.append(result)

        return results

    def _create_snippet(self, text: str, query: str, max_length: int = 200) -> str:
        """Create a snippet of text with query context"""
        if not text:
            return ""

        text = text.strip()
        if len(text) <= max_length:
            return text

        # Try to find query terms in text
        query_lower = query.lower()
        text_lower = text.lower()

        if query_lower in text_lower:
            pos = text_lower.index(query_lower)
            start = max(0, pos - 50)
            end = min(len(text), pos + len(query) + 150)
            snippet = text[start:end]
            if start > 0:
                snippet = "..." + snippet
            if end < len(text):
                snippet = snippet + "..."
            return snippet

        # If query not found, return beginning
        return text[:max_length] + "..."
