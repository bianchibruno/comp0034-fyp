import pytest
from flask import json

def test_get_all_requests(client):
    """Test GET /requests to retrieve all requests."""
    response = client.get('/requests')
    assert response.status_code == 200
    # Check if the response is application/json
    assert response.headers["Content-Type"] == 'application/json'
    # Decode the JSON response
    data = json.loads(response.data)
    # Ensure the data is a list (even if it's empty)
    assert isinstance(data, list)

def test_get_single_request(client):
    """Test GET /requests/<id> to retrieve a specific request."""
    # Assuming there's at least one request with id 1 for testing purposes
    response = client.get('/requests/1')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == 'application/json'
    data = json.loads(response.data)
    # Check that the data includes keys you expect in a Request object
    assert 'id' in data
    assert 'case_type' in data  # Assuming 'case_type' is a field in your Request model
