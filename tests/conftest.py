import pytest
import string
import secrets
import os

from app import create_app, db
from app.models import Request, User
from app.schemas import RequestSchema
from werkzeug.security import generate_password_hash
from secrets import token_urlsafe
from sqlalchemy import exists
from faker import Faker


@pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for each test."""
    # Create a test app using the Flask application factory
    app = create_app({
        'TESTING': True,  # Enable test mode
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Use in-memory SQLite database for tests
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    # Other app configuration settings specific for testing can be set here

    # Create the database and load test data
    with app.app_context():
        db.create_all()
        # You can load test data here if necessary

    yield app

    # Cleanup after tests
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def new_request(app):
    """Fixture to add a new request to the database."""
    with app.app_context():
        new_request = Request(
            case_type='FOIA Case',
            status='Open',
            request_received_year=2023,
            request_received_quarter='Q1',
            request_received_month='January',
            case_active_days_grouped='Up to 20 days used'
        )
        db.session.add(new_request)
        db.session.commit()
        yield new_request

        # Cleanup code: remove the request if it still exists
        db.session.delete(new_request)
        db.session.commit()

@pytest.fixture(scope='function')
def new_user(app):
    """Create a new user and add to the database.

    Adds a new User to the database and also returns the JSON for a new user.

    The scope is session as we need the user to be there throughout for testing the logged in functions.

    """
    user_json = {
            'email': 'testuser@example.com',
            'password': 'ExamplePassword'
        }
    with app.app_context():
        user = User(email=user_json['email'])
        user.password = user_json['password']
        db.session.add(user)
        db.session.commit()

    yield user_json

    # Remove the region from the database at the end of the test if it still exists
    with app.app_context():
        user_exists = db.session.query(exists().where(User.email == user_json['email'])).scalar()
        if user_exists:
            db.session.delete(user)
            db.session.commit()


@pytest.fixture(scope='function')
def random_user_json():
    """Generates a random email and password for testing and returns as JSON."""
    dummy = Faker()
    dummy_email = dummy.email()
    # Generate an eight-character alphanumeric password
    alphabet = string.ascii_letters + string.digits
    dummy_password = ''.join(secrets.choice(alphabet) for i in range(8))
    return {'email': dummy_email, 'password': dummy_password}


@pytest.fixture(scope="function")
def login(client, new_user, app):
    """Returns login response"""
    # Login
    # If login fails then the fixture fails. It may be possible to 'mock' this instead if you want to investigate it.
    response = client.post('/login', json=new_user, content_type="application/json")
    # Get returned json data from the login function
    data = response.json
    yield data
