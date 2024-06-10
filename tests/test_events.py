from app.models import User, db
from werkzeug.security import generate_password_hash

def test_create_event(client):
    """Test event creation."""
    with client.application.app_context():
        # Ensure the user exists and is confirmed
        user = User.query.filter_by(email='testuser@example.com').first()
        if not user:
            user = User(username='testuser', email='testuser@example.com', password=generate_password_hash('Password123!'))
            db.session.add(user)
            db.session.commit()
        user.email_confirmed = True
        db.session.commit()

    response = client.post('/create_event', data=dict(
        name='Test Event',
        description='This is a test event.',
        date='2023-12-31',
        captcha='0' 
    ), follow_redirects=True)
    assert response.status_code == 200
