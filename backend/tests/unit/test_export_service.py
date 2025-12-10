import pytest
from backend.services.export_service import ExportService

@pytest.fixture
def export_service():
    """Fixture to create an ExportService instance."""
    return ExportService()

def test_export_to_pdf_returns_bytes(export_service):
    """Test that export_to_pdf returns a bytes object."""
    # Arrange
    markdown_content = "# Chapter 1\n\nThis is some content."
    
    # Act
    pdf_bytes = export_service.export_to_pdf(markdown_content)
    
    # Assert
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0 # Should not be empty

def test_export_to_pdf_with_format_preferences(export_service):
    """Test that export_to_pdf runs without error when format preferences are provided."""
    # Arrange
    markdown_content = "## A Big Title\n\nSome spacious content."
    format_preferences = {"font_size": "large", "layout": "spacious"}
    
    # Act
    try:
        pdf_bytes = export_service.export_to_pdf(
            content_markdown=markdown_content,
            format_preferences=format_preferences
        )
        # Assert
        assert isinstance(pdf_bytes, bytes)
    except Exception as e:
        pytest.fail(f"export_to_pdf raised an exception with format preferences: {e}")

def test_export_to_epub_returns_bytes(export_service):
    """Test that export_to_epub returns a bytes object."""
    # Arrange
    title = "My First Ebook"
    author = "Test Author"
    chapters = [
        ("Chapter 1", "# Chapter 1\n\nContent for chapter 1."),
        ("Chapter 2", "## Chapter 2\n\nMore content here."),
    ]
    
    # Act
    epub_bytes = export_service.export_to_epub(title, author, chapters)
    
    # Assert
    assert isinstance(epub_bytes, bytes)
    assert len(epub_bytes) > 0

def test_export_to_epub_with_format_preferences(export_service):
    """Test that export_to_epub runs without error when format preferences are given."""
    # Arrange
    title = "Formatted Ebook"
    author = "Pref Author"
    chapters = [("Intro", "Small font intro.")]
    format_preferences = {"font_size": "small"}
    
    # Act
    try:
        epub_bytes = export_service.export_to_epub(
            title=title,
            author=author,
            chapter_markdown=chapters,
            format_preferences=format_preferences
        )
        # Assert
        assert isinstance(epub_bytes, bytes)
    except Exception as e:
        pytest.fail(f"export_to_epub raised an exception with format preferences: {e}")

def test_export_to_epub_structure(export_service):
    """A slightly more in-depth test to check for content presence in EPUB."""
    # We can't easily parse the EPUB, but we can check if it's a zip file (which EPUBs are)
    # and if it contains the expected file names.
    import zipfile
    import io

    # Arrange
    title = "Structured Book"
    author = "Structo"
    chapters = [("First Chapter", "Content one."), ("Second Chapter", "Content two.")]

    # Act
    epub_bytes = export_service.export_to_epub(title, author, chapters)

    # Assert
    assert zipfile.is_zipfile(io.BytesIO(epub_bytes))
    
    with zipfile.ZipFile(io.BytesIO(epub_bytes), 'r') as zf:
        # Check for standard EPUB files
        assert 'mimetype' in zf.namelist()
        assert 'META-INF/container.xml' in zf.namelist()
        
        # Check for chapter files
        assert any('chap_1.xhtml' in s for s in zf.namelist())
        assert any('chap_2.xhtml' in s for s in zf.namelist())
