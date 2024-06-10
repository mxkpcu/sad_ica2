import pytest
from app import create_app
from app import db

@pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('config.TestConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='module')
def init_database(app):
    """Initialize the database."""
    with app.app_context():
        db.reflect()
        yield db
        db.drop_all()

@pytest.fixture
def captcha(client):
    """Set up the correct CAPTCHA value in the session."""
    with client.session_transaction() as sess:
        sess['captcha_answer'] = 0