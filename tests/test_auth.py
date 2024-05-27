from flask import jsonify
import time

def test_register_success(client, random_user_json):
    user_register = client.post('/register', json=random_user_json, content_type="application/json")
    assert user_register.status_code == 201

def test_login_success(client, new_user):
    user_register = client.post('/login', json=new_user, content_type="application/json")
    assert user_register.status_code == 201

def test_user_not_logged_in_cannot_edit_request(client, new_user, new_request):
    """
    GIVEN a registered user that is not logged in
    AND a route that is protected by login
    AND a new Region that can be edited
    WHEN a PATCH request to /requests/<id> is made
    THEN the HTTP response status code should be 401 with message 'Authentication token missing
    """
    patch_data = {'status': 'Closed'}
    response = client.patch(f'/requests/{new_request.id}', json=patch_data)
    assert response.status_code == 401

def test_user_logged_in_can_edit_request(app, client, new_user, login, new_request):
    """
    GIVEN a registered user that is successfully logged in
    AND a route that is protected by login
    AND a new Region that can be edited
    WHEN a PATCH request to /requests/<id> is made
    THEN the HTTP status code should be 200
    AND the response content should include the message 'Region <NOC_code> updated'
    """
    token = login['token']
    headers = {
        'content-type': 'application/json',
        'Authorization': token
        }
    patch_data = {'status': 'Closed'}
    response = client.patch(f'/requests/{new_request.id}', json=patch_data, headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == 'Request updated.'

def test_user_logged_in_can_delete_request(app, client, new_user, login, new_request):
    """
    GIVEN a registered user that is successfully logged in
    AND a route that is protected by login
    AND a new Region that can be deleted
    WHEN a DELETE request to /requests/<id> is made
    THEN the HTTP status code should be 202
    AND the response content should include the message 'Request deleted'
    """
    token = login['token']
    headers = {
        'content-type': 'application/json',
        'Authorization': token
        }
    response = client.delete(f'/requests/{new_request.id}', headers=headers)
    assert response.status_code == 202
    assert response.json['message'] == 'Request deleted'

def test_user_not_logged_in_cannot_delete_request(client, new_user, new_request):
    """
    GIVEN a registered user that is not logged in
    AND a route that is protected by login
    AND a new Region that can be deleted
    WHEN a DELETE request to /requests/<id> is made
    THEN the HTTP response status code should be 401 with message 'Authentication token missing
    """
    response = client.delete(f'/requests/{new_request.id}')
    assert response.status_code == 401
    assert response.json['message'] == 'Authentication Token missing'

def test_user_logged_in_can_add_request(app, client, new_user, login):
    """
    GIVEN a registered user that is successfully logged in
    AND a route that is protected by login
    WHEN a POST request to /requests is made
    THEN the HTTP status code should be 201
    AND the response content should include the message 'Request added'
    """
    token = login['token']
    headers = {
        'content-type': 'application/json',
        'Authorization': token
        }
    new_foia_data = {
    "case_active_days_grouped": "More than 60 days used",
    "case_type": "FOIA Case",
    "request_received_month": "November",
    "request_received_quarter": "Quarter 4",
    "request_received_year": "2018",
    "status": "Closed"
}
    response = client.post('/requests', json=new_foia_data, headers=headers)
    assert response.status_code == 201
    # assert response.json['message'] == 'Request added'

def test_user_not_logged_in_cannot_add_request(client):
    """
    GIVEN a registered user that is not logged in
    AND a route that is protected by login
    WHEN a POST request to /requests is made
    THEN the HTTP response status code should be 401 with message 'Authentication token missing
    """
    new_foia_data = {
    "case_active_days_grouped": "More than 60 days used",
    "case_type": "FOIA Case",
    "request_received_month": "November",
    "request_received_quarter": "Quarter 4",
    "request_received_year": "2018",
    "status": "Closed"
}
    response = client.post('/requests', json=new_foia_data)
    assert response.status_code == 401
    assert response.json['message'] == 'Authentication Token missing'

def test_register_missing_fields(client):
    """
    GIVEN incomplete data is sent to the register endpoint
    WHEN the data is missing an email or password
    THEN the status code should be 400 Bad Request
    """
    # Test with missing email
    missing_email = {
        'password': 'ExamplePassword'
    }
    response = client.post('/register', json=missing_email, content_type="application/json")
    assert response.status_code == 400
    assert 'email' in response.json['message'], "Missing email should trigger an error message"

    # Test with missing password
    missing_password = {
        'email': 'testuser@example.com'
    }
    response = client.post('/register', json=missing_password, content_type="application/json")
    assert response.status_code == 400
    assert 'password' in response.json['message'], "Missing password should trigger an error message"

    # Test with both fields missing
    missing_both = {}
    response = client.post('/register', json=missing_both, content_type="application/json")
    assert response.status_code == 400
    assert 'email' in response.json['message'] or 'password' in response.json['message'], "Missing both fields should trigger an error message"

def test_login_missing_fields(client):
    """
    GIVEN incomplete data is sent to the login endpoint
    WHEN the data is missing an email or password
    THEN the status code should be 401 Unauthorized and provide an appropriate error message
    """
    # Test with missing email
    missing_email = {'password': 'ExamplePassword'}
    response_missing_email = client.post('/login', json=missing_email, content_type="application/json")
    assert response_missing_email.status_code == 401
    assert 'Missing email or password' in response_missing_email.json['message']

    # Test with missing password
    missing_password = {'email': 'testuser@example.com'}
    response_missing_password = client.post('/login', json=missing_password, content_type="application/json")
    assert response_missing_password.status_code == 401
    assert 'Missing email or password' in response_missing_password.json['message']
def test_token_expiry(client, new_user):
    """
    GIVEN a user is logged in and receives a token
    WHEN the token expires
    THEN access to a protected route should be denied
    """
    # Log in to get a token
    login_response = client.post('/login', json={
        'email': new_user['email'],
        'password': new_user['password']
    }, content_type="application/json")
    token = login_response.json['token']
    
    # Wait for the token to expire
    time.sleep(35)  # Wait longer than the token expiry time set in the JWT
    
    # Attempt to access a protected route
    protected_response = client.get('/secure-data', headers={
        'Authorization': f'Bearer {token}'
    })
    
    # Check if access is denied due to token expiry
    assert protected_response.status_code == 401
    assert 'Token has expired' in protected_response.json['message']