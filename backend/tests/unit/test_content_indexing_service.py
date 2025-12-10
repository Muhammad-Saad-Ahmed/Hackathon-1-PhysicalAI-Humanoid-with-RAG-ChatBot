import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from backend.services.content_indexing import ContentIndexingService, DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP
from backend.models.textbook import Textbook, TextbookStatus

@pytest.fixture
def mock_db_session():
    """Fixture for a mocked SQLAlchemy session."""
    return MagicMock(spec=Session)

@pytest.fixture
def mock_embedding_service():
    """Fixture for a mocked EmbeddingService."""
    service = MagicMock()
    service.embed_text.return_value = [0.1, 0.2, 0.3]  # Dummy embedding
    return service

@pytest.fixture
def mock_qdrant_service():
    """Fixture for a mocked QdrantService."""
    return MagicMock()

@pytest.fixture
def content_indexing_service(mock_db_session, mock_embedding_service, mock_qdrant_service):
    """Fixture to create a ContentIndexingService instance with mocked dependencies."""
    with patch('backend.services.content_indexing.EmbeddingService', return_value=mock_embedding_service), \
         patch('backend.services.content_indexing.QdrantService', return_value=mock_qdrant_service):
        service = ContentIndexingService(db=mock_db_session)
        yield service

def test_chunk_text_simple(content_indexing_service):
    """Test chunking of text shorter than the chunk size."""
    text = "This is a short text."
    chunks = content_indexing_service._chunk_text(text)
    assert chunks == [text]

def test_chunk_text_multiple_chunks(content_indexing_service):
    """Test chunking of text that should be split into multiple chunks."""
    text = "a" * (DEFAULT_CHUNK_SIZE + 100)
    chunks = content_indexing_service._chunk_text(text)
    assert len(chunks) > 1
    assert len(chunks[0]) == DEFAULT_CHUNK_SIZE
    # Test overlap
    expected_start_of_second_chunk = text[DEFAULT_CHUNK_SIZE - DEFAULT_CHUNK_OVERLAP:]
    assert chunks[1].startswith(expected_start_of_second_chunk[:10])

@patch('backend.database.repositories.TextbookRepository')
@patch('backend.database.repositories.ChapterRepository')
@patch('backend.database.repositories.SectionRepository')
def test_index_textbook_success(
    MockSectionRepo, MockChapterRepo, MockTextbookRepo,
    content_indexing_service, mock_qdrant_service, mock_embedding_service
):
    """Test successful indexing of a complete textbook."""
    # Arrange
    textbook_id = "test-book-id"
    mock_textbook = Textbook(id=textbook_id, status=TextbookStatus.COMPLETED)
    MockTextbookRepo.get.return_value = mock_textbook
    
    mock_chapter = MagicMock(id="chap1", title="Chapter 1")
    MockChapterRepo.get_by_textbook.return_value = [mock_chapter]
    
    mock_section = MagicMock(id="sec1", title="Section 1", content="This is the content of section one.")
    MockSectionRepo.get_by_chapter.return_value = [mock_section]
    
    # Act
    content_indexing_service.index_textbook(textbook_id)
    
    # Assert
    MockTextbookRepo.get.assert_called_once_with(content_indexing_service.db, textbook_id)
    mock_qdrant_service.delete_by_textbook_id.assert_called_once_with(textbook_id)
    MockChapterRepo.get_by_textbook.assert_called_once_with(content_indexing_service.db, textbook_id)
    MockSectionRepo.get_by_chapter.assert_called_once_with(content_indexing_service.db, "chap1")
    mock_embedding_service.embed_text.assert_called_once()
    mock_qdrant_service.store_text_chunks.assert_called_once()
    
    # Check the data passed to store_text_chunks
    stored_chunks = mock_qdrant_service.store_text_chunks.call_args[0][0]
    assert len(stored_chunks) == 1
    assert stored_chunks[0]['textbook_id'] == textbook_id
    assert "Chapter: Chapter 1" in stored_chunks[0]['text']
    assert "This is the content" in stored_chunks[0]['text']
    assert stored_chunks[0]['embedding'] == [0.1, 0.2, 0.3]

@patch('backend.database.repositories.TextbookRepository')
def test_index_textbook_not_found(MockTextbookRepo, content_indexing_service):
    """Test indexing a textbook that does not exist."""
    MockTextbookRepo.get.return_value = None
    
    with pytest.raises(ValueError, match="Textbook not found or not completed."):
        content_indexing_service.index_textbook("non-existent-id")

@patch('backend.database.repositories.TextbookRepository')
def test_index_textbook_not_completed(MockTextbookRepo, content_indexing_service):
    """Test indexing a textbook that is not in COMPLETED status."""
    mock_textbook = Textbook(id="generating-book", status=TextbookStatus.GENERATING)
    MockTextbookRepo.get.return_value = mock_textbook
    
    with pytest.raises(ValueError, match="Textbook not found or not completed."):
        content_indexing_service.index_textbook("generating-book")

