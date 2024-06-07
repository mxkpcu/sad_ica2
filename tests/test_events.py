from app.models import User, db

def test_create_event(test_client, init_database):
    with test_client.session_transaction() as sess:
        sess['captcha_answer'] = 0  # Set the expected CAPTCHA answer

    # Ensure user is logged in and confirmed
    user = User.query.filter_by(email='testuser@example.com').first()
    if user:
        user.email_confirmed = True
        db.session.commit()

    test_client.post('/login', data=dict(
        email='testuser@example.com',
        password='Password123!',
        captcha='0'
    ), follow_redirects=True)
    
    response = test_client.post('/create_event', data=dict(
        name='Test Event',
        description='This is a test event.',
        date='2024-12-31'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Event' in response.data