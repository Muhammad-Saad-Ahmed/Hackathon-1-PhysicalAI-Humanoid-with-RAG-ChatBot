import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app 
from backend.database.database import Base, get_db
from backend.models.generation_params import SavedGenerationParameterSet

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_param_integration.db"
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

# --- Test Data ---
@pytest.fixture
def sample_param_set_payload():
    return {
        "name": "My Test Parameters",
        "parameters": {
            "subject_area": "Advanced Testing",
            "target_audience": "QA Engineers",
            "chapter_topics": ["Fixtures", "Mocks"],
        }
    }

# --- Integration Tests ---

def test_save_parameter_set_success(client, test_db, sample_param_set_payload):
    """Test successfully saving a new parameter set."""
    response = client.post("/api/v1/parameters/", json=sample_param_set_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "My Test Parameters"
    assert "id" in data
    assert data["parameters"]["subject_area"] == "Advanced Testing"

def test_save_parameter_set_duplicate_name(client, test_db, sample_param_set_payload):
    """Test that saving a parameter set with a duplicate name fails."""
    # First, create the set
    client.post("/api/v1/parameters/", json=sample_param_set_payload)
    
    # Then, try to create it again
    response = client.post("/api/v1/parameters/", json=sample_param_set_payload)
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_get_parameter_set_by_id(client, test_db, sample_param_set_payload):
    """Test retrieving a parameter set by its ID."""
    # Create the set
    create_response = client.post("/api/v1/parameters/", json=sample_param_set_payload)
    set_id = create_response.json()["id"]
    
    # Retrieve it
    response = client.get(f"/api/v1/parameters/{set_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == set_id
    assert data["name"] == "My Test Parameters"

def test_get_parameter_set_by_id_not_found(client, test_db):
    """Test retrieving a non-existent parameter set by ID."""
    response = client.get("/api/v1/parameters/non-existent-id")
    assert response.status_code == 404

def test_get_parameter_set_by_name(client, test_db, sample_param_set_payload):
    """Test retrieving a parameter set by its name."""
    client.post("/api/v1/parameters/", json=sample_param_set_payload)
    
    set_name = "My Test Parameters"
    response = client.get(f"/api/v1/parameters/name/{set_name}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == set_name

def test_list_parameter_sets(client, test_db, sample_param_set_payload):
    """Test listing all saved parameter sets."""
    # Create two sets
    client.post("/api/v1/parameters/", json=sample_param_set_payload)
    
    payload2 = sample_param_set_payload.copy()
    payload2["name"] = "My Other Parameters"
    client.post("/api/v1/parameters/", json=payload2)
    
    # List them
    response = client.get("/api/v1/parameters/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert "My Test Parameters" in [s["name"] for s in data]
    assert "My Other Parameters" in [s["name"] for s in data]
