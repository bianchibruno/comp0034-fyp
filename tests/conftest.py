import pytest
from app import create_app, db
import os

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
