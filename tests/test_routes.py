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

def test_get_requests_json(client):
    """
    Test that GET /requests returns a list of requests in JSON format
    and includes specific FOIA case details.
    """
    # Perform the GET request
    response = client.get("/requests")
    
    # Assert the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert the Content-Type is application/json
    assert response.headers["Content-Type"] == "application/json"
    
    # Convert the response data to JSON
    response_data = json.loads(response.data)
    first_request = {
  "case_active_days_grouped": "More than 60 days used",
  "case_type": "FOIA Case",
  "id": 1,
  "request_received_month": "November",
  "request_received_quarter": "Quarter 4",
  "request_received_year": "2018",
  "status": "Closed"
}
    # Check that the response is a list
    assert first_request in response_data

def test_get_request_not_found(client):
    """Test GET /requests/<id> for a non-existing request."""
    response = client.get('/requests/999999')  # Assuming 999 is an id that doesn't exist
    assert response.status_code == 404

# this is now in test_auth.py

# def test_add_foia_request(client):
#     """
#     GIVEN a Flask test client
#     AND valid JSON for a new FOIA request
#     WHEN a POST request is made to /requests
#     THEN the response status_code should be 201
#     """
#     # JSON to create a new FOIA request
#     new_foia_data = {
#     "case_active_days_grouped": "More than 60 days used",
#     "case_type": "FOIA Case",
#     "id": 1,
#     "request_received_month": "November",
#     "request_received_quarter": "Quarter 4",
#     "request_received_year": "2018",
#     "status": "Closed"
# }
    
#     # Pass the JSON in the HTTP POST request
#     response = client.post(
#         "/requests",
#         json=new_foia_data,
#         content_type="application/json"
#     )
    
#     # Assert the HTTP status code for a successful POST or PUT request
#     assert response.status_code == 201, "Expected status code 201, got {}".format(response.status_code)
#     assert "application/json" in response.headers['Content-Type'], "Expected content-type 'application/json'"


# def test_add_foia_request_error(client):
#     """
#     GIVEN a Flask test client
#     AND JSON for a new FOIA request that is missing a required field ("case_type")
#     WHEN a POST request is made to /requests
#     THEN the response status_code should be 400
#     """
#     # Incomplete JSON for creating a new FOIA request
#     incomplete_foia_data = {
#         "status": "Open",
#         "request_received_year": 2023
#     }
    
#     # Pass the incomplete JSON in the HTTP POST request
#     response = client.post(
#         "/requests",
#         json=incomplete_foia_data,
#         content_type="application/json"
#     )
    
#     # Assert the HTTP status code for a bad request
#     assert response.status_code == 400, "Expected status code 400, got {}".format(response.status_code)
#     assert "application/json" in response.headers['Content-Type'], "Expected content-type 'application/json'"

# this is now in test_auth.py
# def test_patch_request(client, new_request):
#     """
#     GIVEN an existing request
#     WHEN a PATCH request is made to update its status
#     THEN the response should confirm the update and the status should be changed
#     """
#     patch_data = {'status': 'Closed'}
#     response = client.patch(f'/requests/{new_request.id}', json=patch_data)
#     assert response.status_code == 200
#     assert response.json['message'] == 'Request updated.'

# this is now in test_auth.py

# def test_delete_region(client, new_request):
#     """
#     GIVEN an existing region
#     WHEN a DELETE request is made for that region
#     THEN the response should indicate the region has been deleted
#     """
#     # First verify that the region exists
#     response = client.get(f'/requests/{new_request.id}')
#     assert response.status_code == 200

#     # Now, delete the region
#     delete_response = client.delete(f'/requests/{new_request.id}')
#     assert delete_response.status_code == 202
#     assert delete_response.json['message'] == 'Request deleted'

#     # Verify that the region is no longer in the database
#     response_after_delete = client.get(f'/requests/{new_request.id}')
#     assert response_after_delete.status_code == 404