"""
Weaviate vector database client wrapper
"""

import weaviate
from weaviate.classes.config import Configure
import os
from dotenv import load_dotenv

load_dotenv()


class WeaviateClient:
    """Wrapper for Weaviate client with configuration"""

    def __init__(self):
        self.url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
        self.api_key = os.getenv("WEAVIATE_API_KEY")
        self.client = None

    def connect(self):
        """Connect to Weaviate instance"""
        try:
            if self.api_key:
                self.client = weaviate.connect_to_custom(
                    http_host=self.url.replace("http://", "").replace("https://", ""),
                    http_port=8080,
                    http_secure=False,
                    auth_credentials=weaviate.auth.AuthApiKey(self.api_key)
                )
            else:
                # Local development without authentication
                self.client = weaviate.connect_to_local(
                    host=self.url.replace("http://", "").replace("https://", ""),
                    port=8080
                )

            if self.client.is_ready():
                print(f"✅ Connected to Weaviate at {self.url}")
                return self.client
            else:
                print(f"⚠️  Weaviate is not ready")
                return None

        except Exception as e:
            print(f"❌ Error connecting to Weaviate: {e}")
            return None

    def close(self):
        """Close Weaviate connection"""
        if self.client:
            self.client.close()
            print("✅ Weaviate connection closed")

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def get_weaviate_client():
    """Get Weaviate client instance"""
    client_wrapper = WeaviateClient()
    return client_wrapper.connect()
