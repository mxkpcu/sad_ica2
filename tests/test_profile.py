from app.models import User, db
from werkzeug.security import generate_password_hash

def test_edit_profile(client):
    """Test profile editing."""
    with client.application.app_context():
        # Ensure the user exists and is confirmed
        user = User.query.filter_by(email='testuser@example.com').first()
        if not user:
            user = User(username='testuser', email='testuser@example.com', password=generate_password_hash('Password123!'))
            db.session.add(user)
            db.session.commit()
        user.email_confirmed = True
        db.session.commit()

    response = client.post('/edit_profile', data=dict(
        username='newusername',
        email='newemail@example.com',
        phone='0987654321',
        captcha='0'
    ), follow_redirects=True)
    assert response.status_code == 200
