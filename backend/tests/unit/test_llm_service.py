import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from backend.services.llm_service import LLMService

@pytest.fixture
def llm_service():
    """Fixture to create an LLMService instance with a mocked Groq client."""
    with patch('backend.services.llm_service.Groq') as mock_groq:
        mock_client = MagicMock()
        mock_groq.return_value = mock_client
        
        service = LLMService()
        service.client = mock_client
        yield service

@pytest.mark.asyncio
async def test_generate_chapter_content_success(llm_service):
    """Test successful chapter content generation."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Generated chapter content."
    llm_service.client.chat.completions.create = AsyncMock(return_value=mock_response)

    result = await llm_service.generate_chapter_content(
        topic="Test Topic",
        subject_area="Test Subject",
        target_audience="Test Audience"
    )

    assert result["content"] == "Generated chapter content."
    llm_service.client.chat.completions.create.assert_awaited_once()

@pytest.mark.asyncio
async def test_generate_chapter_content_failure(llm_service):
    """Test chapter content generation failure."""
    llm_service.client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))

    with pytest.raises(Exception, match="Error generating chapter content: API Error"):
        await llm_service.generate_chapter_content(
            topic="Test Topic",
            subject_area="Test Subject",
            target_audience="Test Audience"
        )

@pytest.mark.asyncio
async def test_generate_textbook_overview_success(llm_service):
    """Test successful textbook overview generation."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Textbook overview."
    llm_service.client.chat.completions.create = AsyncMock(return_value=mock_response)

    result = await llm_service.generate_textbook_overview(
        subject_area="Test Subject",
        target_audience="Test Audience",
        chapter_topics=["Topic 1", "Topic 2"]
    )

    assert result == "Textbook overview."
    llm_service.client.chat.completions.create.assert_awaited_once()

@pytest.mark.asyncio
async def test_validate_content_accuracy_success(llm_service):
    """Test successful content accuracy validation."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Potential issue found."
    llm_service.client.chat.completions.create = AsyncMock(return_value=mock_response)

    result = await llm_service.validate_content_accuracy(
        content="Some content to validate.",
        subject_area="Test Subject"
    )

    assert result == ["Potential issue found."]
    llm_service.client.chat.completions.create.assert_awaited_once()

@pytest.mark.asyncio
async def test_generate_chat_response_streaming(llm_service):
    """Test successful streaming chat response generation."""
    
    # Create a mock for the stream object
    mock_stream_chunk = MagicMock()
    mock_stream_chunk.choices[0].delta.content = "Hello"
    
    mock_stream_chunk_2 = MagicMock()
    mock_stream_chunk_2.choices[0].delta.content = " world"
    
    async def mock_stream_context_manager():
        yield mock_stream_chunk
        yield mock_stream_chunk_2

    # Mock the create method to return an async generator
    llm_service.client.chat.completions.create = MagicMock(return_value=mock_stream_context_manager())

    response_generator = llm_service.generate_chat_response(query="A test query", context="Some context")
    
    # Consume the generator and collect the results
    result_chunks = [chunk async for chunk in response_generator]
    
    # Assertions
    assert "".join(result_chunks) == "Hello world"
    llm_service.client.chat.completions.create.assert_called_once()
