from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
import uuid
from ..config.settings import settings


class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            port=6333,
            https=False
        )
        self.collection_name = "textbook_content"
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
        """Create the collection if it doesn't exist."""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # Size for sentence-transformers/all-MiniLM-L6-v2
                    distance=models.Distance.COSINE
                )
            )

    def store_text_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        """
        Store text chunks in Qdrant with metadata.

        Args:
            chunks: List of dictionaries containing:
                - content_id: UUID of the content
                - content_type: "chapter" or "section"
                - textbook_id: UUID of the textbook
                - chapter_id: UUID of the chapter (if content_type is "section")
                - text: The actual content to be embedded
                - metadata: Additional information like headings, context
                - embedding: The vector embedding of the text
        """
        try:
            points = []
            for chunk in chunks:
                point = models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=chunk["embedding"],
                    payload={
                        "content_id": chunk["content_id"],
                        "content_type": chunk["content_type"],
                        "textbook_id": chunk["textbook_id"],
                        "chapter_id": chunk.get("chapter_id", ""),
                        "text": chunk["text"],
                        "metadata": chunk.get("metadata", {})
                    }
                )
                points.append(point)

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return True
        except Exception as e:
            print(f"Error storing text chunks: {e}")
            return False

    def search_similar(self, query_embedding: List[float], textbook_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar content in the vector store.

        Args:
            query_embedding: The embedding vector to search for
            textbook_id: The textbook ID to limit search to
            limit: Number of results to return

        Returns:
            List of dictionaries containing content and metadata
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="textbook_id",
                            match=models.MatchValue(value=textbook_id)
                        )
                    ]
                ),
                limit=limit
            )

            return [
                {
                    "content_id": result.payload["content_id"],
                    "content_type": result.payload["content_type"],
                    "textbook_id": result.payload["textbook_id"],
                    "chapter_id": result.payload["chapter_id"],
                    "text": result.payload["text"],
                    "metadata": result.payload["metadata"],
                    "score": result.score
                }
                for result in results
            ]
        except Exception as e:
            print(f"Error searching for similar content: {e}")
            return []

    def delete_by_textbook_id(self, textbook_id: str) -> bool:
        """
        Delete all content associated with a textbook ID.

        Args:
            textbook_id: The textbook ID to delete content for

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="textbook_id",
                                match=models.MatchValue(value=textbook_id)
                            )
                        ]
                    )
                )
            )
            return True
        except Exception as e:
            print(f"Error deleting content by textbook ID: {e}")
            return False