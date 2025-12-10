import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from backend.main import app
from backend.models.textbook import Textbook, TextbookStatus
from backend.models.chapter import Chapter
from backend.services.export_service import ExportService
from backend.database.repositories import TextbookRepository, ChapterRepository
import json

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    """Mocks the database session for testing."""
    return MagicMock()

@pytest.fixture
def mock_textbook_repository(mock_db_session):
    """Mocks the TextbookRepository."""
    mock_repo = MagicMock(spec=TextbookRepository)
    # Mocking the get method to return a completed textbook
    mock_textbook = MagicMock(spec=Textbook)
    mock_textbook.id = "test_textbook_id"
    mock_textbook.title = "Test Textbook"
    mock_textbook.subject_area = "Physics"
    mock_textbook.status = TextbookStatus.COMPLETED
    mock_textbook.generation_params = json.dumps( # Example of generation_params structure
        {
            "subject_area": "Physics",
            "target_audience": "High School",
            "chapter_topics": ["Introduction"],
            "style_preferences": {"include_exercises": True},
            "format_preferences": {"font_size": "medium", "layout": "standard"}
        }
    )
    mock_repo.get.return_value = mock_textbook
    return mock_repo

@pytest.fixture
def mock_chapter_repository(mock_db_session):
    """Mocks the ChapterRepository."""
    mock_repo = MagicMock(spec=ChapterRepository)
    # Mocking the get_by_textbook_id method
    mock_chapter = MagicMock(spec=Chapter)
    mock_chapter.id = "test_chapter_id"
    mock_chapter.title = "Chapter 1"
    mock_chapter.content = "# Chapter 1: Introduction\nThis is the content of chapter 1."
    mock_repo.get_by_textbook_id.return_value = [mock_chapter]
    return mock_repo

@pytest.fixture
def mock_export_service():
    """Mocks the ExportService."""
    mock_service = MagicMock(spec=ExportService)
    mock_service.export_to_pdf.return_value = b"%PDF-1.4\n%Test PDF Content"
    mock_service.export_to_epub.return_value = b"PK\x03\x04\x14\x00\x06\x00\x08\x00\x00\x00!\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" # Placeholder for EPUB bytes
    return mock_service

# Patch repositories and services for all tests in this file
@pytest.fixture(autouse=True)
def setup_mocks(mocker, mock_db_session, mock_textbook_repository, mock_chapter_repository, mock_export_service):
    mocker.patch("backend.database.database.get_db", return_value=mock_db_session)
    mocker.patch("backend.database.repositories.TextbookRepository", new=mock_textbook_repository)
    mocker.patch("backend.database.repositories.ChapterRepository", new=mock_chapter_repository)
    mocker.patch("backend.services.export_service.ExportService", return_value=mock_export_service)

def test_pdf_export_acceptance_scenario(mock_textbook_repository, mock_chapter_repository, mock_export_service):
    """
    Given a generated textbook exists,
    When a user selects PDF export,
    Then the system creates a properly formatted PDF document with the textbook content.
    """
    textbook_id = "test_textbook_id"
    response = client.post(f"/v1/textbooks/{textbook_id}/export?format=pdf")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment; filename=\"Test_Textbook.pdf\"" in response.headers["content-disposition"]
    assert response.content == mock_export_service.export_to_pdf.return_value

    # Verify that the textbook and chapters were fetched
    mock_textbook_repository.get.assert_called_once_with(mock_db_session, textbook_id)
    mock_chapter_repository.get_by_textbook_id.assert_called_once_with(mock_db_session, textbook_id)

    # Verify that export_to_pdf was called with the correct content and format preferences
    expected_full_markdown = "# Chapter 1: Introduction\nThis is the content of chapter 1."
    # Extract format_preferences from the mocked textbook's generation_params
    expected_format_preferences = json.loads(mock_textbook_repository.get.return_value.generation_params).get("format_preferences")
    mock_export_service.export_to_pdf.assert_called_once_with(
        expected_full_markdown,
        format_preferences=expected_format_preferences
    )

def test_epub_export_acceptance_scenario(mock_textbook_repository, mock_chapter_repository, mock_export_service):
    """
    Given a generated textbook exists,
    When a user selects ePub export,
    Then the system creates a properly formatted ePub document with the textbook content.
    """
    textbook_id = "test_textbook_id"
    response = client.post(f"/v1/textbooks/{textbook_id}/export?format=epub")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/epub+zip"
    assert "attachment; filename=\"Test_Textbook.epub\"" in response.headers["content-disposition"]
    assert response.content == mock_export_service.export_to_epub.return_value

    # Verify that the textbook and chapters were fetched
    mock_textbook_repository.get.assert_called_once_with(mock_db_session, textbook_id)
    mock_chapter_repository.get_by_textbook_id.assert_called_once_with(mock_db_session, textbook_id)

    # Verify that export_to_epub was called with the correct content and format preferences
    expected_chapter_data = [("Chapter 1", "# Chapter 1: Introduction\nThis is the content of chapter 1.")]
    # Extract format_preferences from the mocked textbook's generation_params
    expected_format_preferences = json.loads(mock_textbook_repository.get.return_value.generation_params).get("format_preferences")
    mock_export_service.export_to_epub.assert_called_once_with(
        mock_textbook_repository.get.return_value.title,
        mock_textbook_repository.get.return_value.subject_area, # Assuming subject_area is used as author
        expected_chapter_data,
        format_preferences=expected_format_preferences
    )

def test_export_textbook_not_found():
    """
    Given a textbook does not exist,
    When a user requests export,
    Then the system returns a 404 error.
    """
    textbook_id = "non_existent_id"
    response = client.post(f"/v1/textbooks/{textbook_id}/export?format=pdf")

    assert response.status_code == 404
    assert response.json() == {"detail": "Textbook not found"}

def test_export_textbook_not_completed(mock_textbook_repository):
    """
    Given a textbook exists but generation is not completed,
    When a user requests export,
    Then the system returns a 400 error.
    """
    mock_textbook_repository.get.return_value.status = TextbookStatus.GENERATING
    textbook_id = "test_textbook_id"
    response = client.post(f"/v1/textbooks/{textbook_id}/export?format=pdf")

    assert response.status_code == 400
    assert response.json() == {"detail": "Textbook generation is not yet completed."}

def test_export_no_chapters_found(mock_textbook_repository, mock_chapter_repository):
    """
    Given a completed textbook exists but has no chapters,
    When a user requests export,
    Then the system returns a 404 error.
    """
    mock_chapter_repository.get_by_textbook_id.return_value = []
    textbook_id = "test_textbook_id"
    response = client.post(f"/v1/textbooks/{textbook_id}/export?format=pdf")

    assert response.status_code == 404
    assert response.json() == {"detail": "No chapters found for this textbook."}

def test_export_invalid_format():
    """
    Given a valid textbook exists,
    When a user requests export with an invalid format,
    Then the system returns a 400 error.
    """
    textbook_id = "test_textbook_id" # This ID will trigger the mock_textbook_repository.get to return a valid textbook
    response = client.post(f"/v1/textbooks/{textbook_id}/export?format=xyz")

    assert response.status_code == 422 # FastAPI's validation error for enum mismatch
