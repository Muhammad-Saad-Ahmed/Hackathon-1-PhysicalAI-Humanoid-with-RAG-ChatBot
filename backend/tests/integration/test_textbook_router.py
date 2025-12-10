import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, AsyncMock

from backend.main import app 
from backend.database.database import Base, get_db
from backend.models.textbook import TextbookStatus

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Dependency override to use the test database."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def test_db():
    """Fixture to set up and tear down the test database for each test function."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    """Fixture to create a TestClient instance for the module."""
    with TestClient(app) as c:
        yield c

# --- Integration Tests ---

def test_create_textbook(client, test_db):
    """Test creating a new textbook."""
    response = client.post(
        "/api/v1/textbooks/",
        json={"title": "Integration Test Book", "subject_area": "Pytest", "target_audience": "Developers"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Integration Test Book"
    assert "id" in data

@patch('backend.services.textbook_generation.TextbookGenerationService.generate_textbook', new_callable=AsyncMock)
def test_generate_textbook_endpoint(mock_generate_textbook, client, test_db):
    """Test the /generate endpoint, mocking the service layer."""
    # Arrange
    mock_generate_textbook.return_value = {
        "textbook_id": "mock-generated-id",
        "status": "success"
    }
    
    request_payload = {
        "subject_area": "Computer Science",
        "target_audience": "Beginner",
        "chapter_topics": ["Introduction", "Algorithms"]
    }
    
    # Act
    response = client.post("/api/v1/textbooks/generate", json=request_payload)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["textbook_id"] == "mock-generated-id"
    assert data["status"] == "success"
    mock_generate_textbook.assert_awaited_once()

def test_get_textbook(client, test_db):
    """Test retrieving a single textbook."""
    # First, create a textbook to retrieve
    create_response = client.post(
        "/api/v1/textbooks/",
        json={"title": "A Book to Get", "subject_area": "Reading", "target_audience": "Everyone"},
    )
    textbook_id = create_response.json()["id"]
    
    # Now, get it
    get_response = client.get(f"/api/v1/textbooks/{textbook_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["title"] == "A Book to Get"

def test_get_textbooks_list(client, test_db):
    """Test retrieving a list of textbooks."""
    # Create a couple of textbooks
    client.post("/api/v1/textbooks/", json={"title": "Book 1", "subject_area": "List", "target_audience": "Test"})
    client.post("/api/v1/textbooks/", json={"title": "Book 2", "subject_area": "List", "target_audience": "Test"})
    
    response = client.get("/api/v1/textbooks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert "Book 1" in [t["title"] for t in data]

def test_update_textbook(client, test_db):
    """Test updating a textbook's status."""
    create_response = client.post(
        "/api/v1/textbooks/",
        json={"title": "Book to Update", "subject_area": "Updating", "target_audience": "Test"},
    )
    textbook_id = create_response.json()["id"]
    
    update_payload = {
        "status": TextbookStatus.COMPLETED.value
    }
    
    response = client.put(f"/api/v1/textbooks/{textbook_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == TextbookStatus.COMPLETED.value

def test_delete_textbook(client, test_db):
    """Test deleting a textbook."""
    create_response = client.post(
        "/api/v1/textbooks/",
        json={"title": "Book to Delete", "subject_area": "Deleting", "target_audience": "Test"},
    )
    textbook_id = create_response.json()["id"]
    
    # Delete the textbook
    delete_response = client.delete(f"/api/v1/textbooks/{textbook_id}")
    assert delete_response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f"/api/v1/textbooks/{textbook_id}")
    assert get_response.status_code == 404
