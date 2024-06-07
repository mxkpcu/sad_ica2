from app.models import User, db

def test_register(test_client, init_database):
    with test_client.session_transaction() as sess:
        sess['captcha_answer'] = 0  # Set the expected CAPTCHA answer

    response = test_client.post('/register', data=dict(
        username='testuser',
        email='testuser@example.com',
        password='Password123!',
        phone='1234567890',
        captcha='0'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'A confirmation email has been sent to your email address.' in response.data

def test_login(test_client, init_database):
    with test_client.session_transaction() as sess:
        sess['captcha_answer'] = 0  # Set the expected CAPTCHA answer

    # Ensure user is confirmed before testing login
    user = User.query.filter_by(email='testuser@example.com').first()
    if user:
        user.email_confirmed = True
        db.session.commit()

    response = test_client.post('/login', data=dict(
        email='testuser@example.com',
        password='Password123!',
        captcha='0'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Profile' in response.data