import pytest
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, AsyncMock

from backend.main import app 
from backend.database.database import Base, get_db
from backend.models.textbook import Textbook

# --- Test Database Setup (similar to test_textbook_router) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_chat_integration.db"
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
def mock_rag_service():
    with patch('backend.api.v1.chat_router.RAGService') as mock:
        service_instance = mock.return_value
        service_instance.search.return_value = [
            {"text": "mock context", "content_id": "c1", "metadata": {"title": "Section 1"}, "score": 0.95}
        ]
        yield service_instance

@pytest.fixture
def mock_llm_service():
    with patch('backend.api.v1.chat_router.LLMService') as mock:
        service_instance = mock.return_value
        # For non-streaming
        service_instance.generate_chat_response = AsyncMock(return_value="This is a mock LLM answer.")
        
        # For streaming
        async def mock_stream_gen(*args, **kwargs):
            yield "This "
            yield "is "
            yield "a stream."
        service_instance.generate_chat_response.return_value = mock_stream_gen()
        yield service_instance


# --- Integration Tests ---

def test_chat_query_success_new_session(client, test_db, mock_rag_service, mock_llm_service):
    """Test successful chat query that creates a new session."""
    # Arrange: Create a textbook to chat with
    db = TestingSessionLocal()
    book = Textbook(id="book-for-chat", title="Chat Book", subject_area="Chatting", target_audience="All")
    db.add(book)
    db.commit()
    db.refresh(book)
    db.close()

    request_payload = {
        "query": "Tell me about chatting.",
        "textbook_id": "book-for-chat"
    }

    # Re-mock the non-streaming response for this specific test
    mock_llm_service.generate_chat_response = AsyncMock(return_value="This is a mock LLM answer.")

    # Act
    response = client.post("/api/v1/chat/", json=request_payload)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "This is a mock LLM answer."
    assert "session_id" in data
    assert len(data["sources"]) == 1
    assert data["sources"][0]["content_id"] == "c1"
    
    mock_rag_service.search.assert_called_once_with(query="Tell me about chatting.", textbook_id="book-for-chat")
    mock_llm_service.generate_chat_response.assert_awaited_once()

def test_chat_query_missing_textbook_id(client, test_db):
    """Test chat query fails if textbook_id is missing."""
    response = client.post("/api/v1/chat/", json={"query": "A question."})
    assert response.status_code == 400
    assert "textbook_id is required" in response.json()["detail"]

def test_get_chat_sessions_not_implemented(client, test_db):
    """Test that the get_chat_sessions endpoint is not implemented."""
    response = client.get("/api/v1/chat/sessions")
    assert response.status_code == 501
    assert "Not implemented yet" in response.json()["detail"]
