import sys
import os
import pytest

# Add the root directory of the project to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db as _db
from app.models import User

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('config.TestConfig')  # Use the TestConfig class

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            _db.create_all()  # Create all tables
        yield testing_client  # this is where the testing happens

@pytest.fixture(scope='module')
def init_database():
    # Initialize the database
    flask_app = create_app('config.TestConfig')
    with flask_app.app_context():
        _db.create_all()
        yield _db  # this is where the testing happens
        _db.drop_all()
