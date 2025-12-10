from typing import List, Dict, Any
from ..vector_store.embedding_service import EmbeddingService
from ..vector_store.qdrant_client import QdrantService


class RAGService:
    """
    Service for Retrieval Augmented Generation, handling vector search and retrieval.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def search(self, query: str, textbook_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Searches for content similar to the query within a specific textbook.

        Args:
            query: The user's search query.
            textbook_id: The ID of the textbook to search within.
            limit: The maximum number of results to return.

        Returns:
            A list of search results, each containing content, metadata, and score.
        """
        # 1. Generate an embedding for the user's query
        query_embedding = self.embedding_service.embed_text(query)

        # 2. Search for similar content in the vector store, filtered by textbook_id
        search_results = self.qdrant_service.search_similar(
            query_embedding=query_embedding,
            textbook_id=textbook_id,
            limit=limit
        )

        return search_results
