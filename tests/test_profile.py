from app.models import User, db

def test_edit_profile(test_client, init_database):
    with test_client.session_transaction() as sess:
        sess['captcha_answer'] = 0

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
    
    response = test_client.post('/edit_profile', data=dict(
        username='newusername',
        email='newemail@example.com',
        password='NewPassword123!',
        phone='0987654321'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'newusername' in response.data