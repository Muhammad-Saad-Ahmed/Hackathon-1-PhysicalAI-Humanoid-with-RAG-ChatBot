import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.main import app 
from backend.database.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.database import get_db
from backend.config.settings import settings

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_index_integration.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# --- Mocks for Services ---
@pytest.fixture
def mock_content_indexing_service():
    with patch('backend.api.v1.index_router.ContentIndexingService') as mock:
        yield mock.return_value

# --- Integration Tests ---

def test_trigger_indexing_success(client, test_db, mock_content_indexing_service):
    """Test successful indexing trigger with a valid API key."""
    # Arrange
    settings.ADMIN_API_KEY = "test-admin-key"
    headers = {"X-API-KEY": "test-admin-key"}
    request_payload = {"textbook_id": "book-to-index"}
    
    # Act
    response = client.post("/api/v1/index/", json=request_payload, headers=headers)
    
    # Assert
    assert response.status_code == 200
    assert "triggered successfully" in response.json()["message"]
    mock_content_indexing_service.index_textbook.assert_called_once_with("book-to-index")

def test_trigger_indexing_invalid_api_key(client, test_db):
    """Test indexing trigger with an invalid API key."""
    settings.ADMIN_API_KEY = "test-admin-key"
    headers = {"X-API-KEY": "wrong-key"}
    response = client.post("/api/v1/index/", json={"textbook_id": "any-id"}, headers=headers)
    assert response.status_code == 401
    assert "Invalid API Key" in response.json()["detail"]

def test_trigger_indexing_missing_api_key(client, test_db):
    """Test indexing trigger with a missing API key header."""
    response = client.post("/api/v1/index/", json={"textbook_id": "any-id"})
    # FastAPI returns a 422 Unprocessable Entity for missing headers
    assert response.status_code == 422 

def test_trigger_indexing_service_value_error(client, test_db, mock_content_indexing_service):
    """Test error handling when the indexing service raises a ValueError."""
    # Arrange
    settings.ADMIN_API_KEY = "test-admin-key"
    headers = {"X-API-KEY": "test-admin-key"}
    request_payload = {"textbook_id": "not-found-book"}
    
    mock_content_indexing_service.index_textbook.side_effect = ValueError("Textbook not found")
    
    # Act
    response = client.post("/api/v1/index/", json=request_payload, headers=headers)
    
    # Assert
    assert response.status_code == 400
    assert "Textbook not found" in response.json()["detail"]
