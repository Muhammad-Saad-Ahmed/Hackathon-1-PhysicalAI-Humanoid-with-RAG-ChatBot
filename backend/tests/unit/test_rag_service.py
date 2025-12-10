import pytest
from unittest.mock import MagicMock, patch
from backend.services.rag_service import RAGService

@pytest.fixture
def mock_embedding_service():
    """Fixture for a mocked EmbeddingService."""
    service = MagicMock()
    service.embed_text.return_value = [0.4, 0.5, 0.6]  # Dummy query embedding
    return service

@pytest.fixture
def mock_qdrant_service():
    """Fixture for a mocked QdrantService."""
    service = MagicMock()
    # Dummy search result
    service.search_similar.return_value = [
        {"id": "result1", "payload": {"text": "some relevant text"}, "score": 0.9}
    ]
    return service

@pytest.fixture
def rag_service(mock_embedding_service, mock_qdrant_service):
    """Fixture to create a RAGService instance with mocked dependencies."""
    with patch('backend.services.rag_service.EmbeddingService', return_value=mock_embedding_service), \
         patch('backend.services.rag_service.QdrantService', return_value=mock_qdrant_service):
        service = RAGService()
        yield service

def test_search_success(rag_service, mock_embedding_service, mock_qdrant_service):
    """Test a successful search call."""
    # Arrange
    query = "What is quantum mechanics?"
    textbook_id = "book-123"
    limit = 5
    
    # Act
    results = rag_service.search(query=query, textbook_id=textbook_id, limit=limit)
    
    # Assert
    # 1. Check that the embedding service was called with the query
    mock_embedding_service.embed_text.assert_called_once_with(query)
    
    # 2. Check that the vector store search was called with the correct parameters
    mock_qdrant_service.search_similar.assert_called_once_with(
        query_embedding=[0.4, 0.5, 0.6],
        textbook_id=textbook_id,
        limit=limit
    )
    
    # 3. Check that the results from the vector store are returned
    assert len(results) == 1
    assert results[0]["id"] == "result1"
    assert results[0]["score"] == 0.9

@patch('backend.services.rag_service.EmbeddingService')
@patch('backend.services.rag_service.QdrantService')
def test_search_handles_empty_results(MockQdrant, MockEmbedding, rag_service):
    """Test the search method when the vector store returns no results."""
    # Arrange
    MockEmbedding.return_value.embed_text.return_value = [0.7, 0.8, 0.9]
    # Configure Qdrant mock to return an empty list
    MockQdrant.return_value.search_similar.return_value = []
    
    query = "A query that finds nothing"
    textbook_id = "book-456"
    
    # Act
    results = rag_service.search(query=query, textbook_id=textbook_id)
    
    # Assert
    assert results == []
    MockQdrant.return_value.search_similar.assert_called_once()
