import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture(scope="module")
def client():
    """Fixture to create a TestClient instance for the module."""
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}
