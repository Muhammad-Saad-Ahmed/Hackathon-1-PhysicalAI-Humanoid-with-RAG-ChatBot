import pytest
import yaml
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture(scope="module")
def client():
    """Fixture to create a TestClient instance for the module."""
    with TestClient(app) as c:
        yield c

def test_api_contract_matches_specification(client):
    """
    Tests that the live OpenAPI schema from the app matches the committed api-contract.yaml file.
    """
    # 1. Load the committed YAML contract
    # Note: This assumes the test is run from the root of the project.
    # A more robust solution might use absolute paths or path helpers.
    try:
        with open("specs/001-textbook-generation/contracts/api-contract.yaml", 'r') as f:
            committed_contract = yaml.safe_load(f)
    except FileNotFoundError:
        pytest.fail("Could not find the api-contract.yaml file. Ensure the path is correct.")

    # 2. Get the live OpenAPI schema from the application
    response = client.get("/openapi.json")
    assert response.status_code == 200
    live_schema = response.json()

    # 3. Compare the two.
    # We are interested in the paths and components, as 'info' and 'servers' might differ
    # between the static file and the live app.
    
    committed_paths = committed_contract.get("paths", {})
    live_paths = live_schema.get("paths", {})
    
    committed_components = committed_contract.get("components", {})
    live_components = live_schema.get("components", {})
    
    # A simple but effective way to compare is to check if one is a "subset" of the other,
    # ignoring minor differences in description or order.
    # For a true contract test, you would iterate through each path and method.
    
    # Check that all documented paths are present in the live schema
    for path, methods in committed_paths.items():
        assert path in live_paths, f"Path '{path}' from contract not found in live API."
        for method in methods:
            assert method in live_paths[path], f"Method '{method}' for path '{path}' not found in live API."

    # Check that all documented components (schemas) are present
    for component_name, schema in committed_components.get("schemas", {}).items():
        assert component_name in live_components.get("schemas", {}), f"Component schema '{component_name}' not found in live API."
        
        # You could add a more detailed property-level comparison here if needed
        live_schema_props = live_components["schemas"][component_name].get("properties", {}).keys()
        committed_schema_props = schema.get("properties", {}).keys()
        assert committed_schema_props == live_schema_props, \
            f"Properties for schema '{component_name}' do not match between contract and live API."

    # A full comparison is complex, but this gives good coverage that the major parts of the contract are met.
    # This acts as a "smoke test" for the contract.
    assert committed_paths.keys() == live_paths.keys(), "API paths do not match the contract."
    assert committed_components["schemas"].keys() == live_components["schemas"].keys(), "API component schemas do not match the contract."

