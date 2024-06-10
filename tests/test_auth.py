from app.models import User, db
from werkzeug.security import generate_password_hash

def test_register(client, init_database, captcha):
    """Test user registration."""
    response = client.post('/register', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='Password123!',
        phone='1234567890',
        captcha='0'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'A confirmation email has been sent to your email address.' in response.data

def test_login(client, init_database, captcha):
    """Test user login."""
    with client.application.app_context():
        # Ensure the user exists and is confirmed
        user = User.query.filter_by(email='testuser@example.com').first()
        if not user:
            user = User(username='testuser', email='testuser@example.com', password=generate_password_hash('Password123!'))
            db.session.add(user)
            db.session.commit()
        user.email_confirmed = True
        db.session.commit()

    response = client.post('/login', data=dict(
        email='testuser@example.com',
        password='Password123!',
        captcha='0'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Profile' in response.data
