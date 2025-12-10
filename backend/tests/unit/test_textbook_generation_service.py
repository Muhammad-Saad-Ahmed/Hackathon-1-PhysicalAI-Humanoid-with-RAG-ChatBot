import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from sqlalchemy.orm import Session
from backend.services.textbook_generation import TextbookGenerationService
from backend.models.textbook import TextbookCreate, TextbookUpdate, TextbookStatus
from backend.models.chapter import ChapterCreate
from backend.models.section import SectionCreate, SectionType
from backend.models.textbook_generation import GenerateTextbookRequest, StylePreferences, FormatPreferences

@pytest.fixture
def mock_db_session():
    """Fixture for a mocked SQLAlchemy session."""
    return MagicMock(spec=Session)

@pytest.fixture
def mock_llm_service():
    """Fixture for a mocked LLMService."""
    service = MagicMock()
    service.generate_chapter_content = AsyncMock(return_value={"content": "Mocked chapter content", "sections": []})
    service.validate_content_coherence = AsyncMock(return_value=[])
    service.validate_content_accuracy = AsyncMock(return_value=[])
    return service

@pytest.fixture
def textbook_generation_service(mock_db_session, mock_llm_service):
    """Fixture to create a TextbookGenerationService instance with mocked dependencies."""
    with patch('backend.services.textbook_generation.LLMService', return_value=mock_llm_service):
        service = TextbookGenerationService(db=mock_db_session)
        yield service

@pytest.mark.asyncio
@patch('backend.database.repositories.TextbookRepository')
@patch('backend.database.repositories.ChapterRepository')
@patch('backend.database.repositories.SectionRepository')
async def test_generate_textbook_success(
    MockSectionRepo, MockChapterRepo, MockTextbookRepo,
    textbook_generation_service, mock_llm_service
):
    """Test successful textbook generation from end to end."""
    # Arrange
    mock_textbook = MagicMock()
    mock_textbook.id = "test-textbook-id"
    MockTextbookRepo.create.return_value = mock_textbook
    
    mock_chapter = MagicMock()
    mock_chapter.id = "test-chapter-id"
    MockChapterRepo.create.return_value = mock_chapter
    
    request = GenerateTextbookRequest(
        subject_area="Quantum Physics",
        target_audience="University",
        chapter_topics=["Introduction to Quantum Mechanics", "Wave-Particle Duality"],
        style_preferences=StylePreferences(include_exercises=True, include_summaries=True, include_diagrams=False),
        format_preferences=FormatPreferences(font_size="medium", layout="standard")
    )
    
    # Act
    result = await textbook_generation_service.generate_textbook(request)
    
    # Assert
    assert result["textbook_id"] == "test-textbook-id"
    assert result["status"] == "success"
    
    # Check that textbook was created and status updated
    assert MockTextbookRepo.create.call_count == 1
    assert MockTextbookRepo.update.call_count == 2 # GENERATING and then COMPLETED
    
    # Check that chapters and sections were generated
    assert mock_llm_service.generate_chapter_content.call_count == 2
    assert MockChapterRepo.create.call_count == 2
    assert MockSectionRepo.create.call_count >= 2 # At least one section per chapter

def test_determine_section_type(textbook_generation_service):
    """Test the logic for determining section type from a title."""
    assert textbook_generation_service._determine_section_type("Introduction") == SectionType.TEXT
    assert textbook_generation_service._determine_section_type("Chapter Summary") == SectionType.SUMMARY
    assert textbook_generation_service._determine_section_type("Practice Exercises") == SectionType.EXERCISE
    assert textbook_generation_service._determine_section_type("Code Example") == SectionType.CODE
    assert textbook_generation_service._determine_section_type("Architectural Diagram") == SectionType.DIAGRAM

def test_extract_sections_from_content(textbook_generation_service):
    """Test extraction of sections from markdown content."""
    content = """
# Main Title (should be ignored)
## Introduction
Some intro content.
## Main Content
More content here.
### Sub-heading (part of main content)
Content under sub-heading.
## Exercises
1. Do this.
2. Do that.
"""
    sections = textbook_generation_service._extract_sections_from_content(content)
    
    assert len(sections) == 3
    assert sections[0]['title'] == "Introduction"
    assert sections[0]['type'] == SectionType.TEXT
    assert "Some intro content" in sections[0]['content']
    
    assert sections[1]['title'] == "Main Content"
    assert "More content here" in sections[1]['content']
    
    assert sections[2]['title'] == "Exercises"
    assert sections[2]['type'] == SectionType.EXERCISE
    assert "1. Do this." in sections[2]['content']

@pytest.mark.asyncio
@patch('backend.database.repositories.TextbookRepository')
async def test_generate_textbook_failure_on_chapter_gen(
    MockTextbookRepo, textbook_generation_service, mock_llm_service
):
    """Test that textbook status is set to FAILED if chapter generation fails."""
    # Arrange
    mock_textbook = MagicMock()
    mock_textbook.id = "failed-textbook-id"
    MockTextbookRepo.create.return_value = mock_textbook
    
    mock_llm_service.generate_chapter_content.side_effect = Exception("LLM is down")
    
    request = GenerateTextbookRequest(
        subject_area="History",
        target_audience="High School",
        chapter_topics=["The Renaissance"]
    )
    
    # Act & Assert
    with pytest.raises(Exception, match="LLM is down"):
        await textbook_generation_service.generate_textbook(request)
        
    # Verify status was updated to FAILED
    update_call_args = MockTextbookRepo.update.call_args_list
    assert any(
        call.kwargs.get('update_data').status == TextbookStatus.FAILED
        for call in update_call_args if call.kwargs.get('update_data')
    )
