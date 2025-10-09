from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash

def test_register_and_login(client, app):
    # Test successful registration with valid data
    valid_password = "Password123!"
    rv = client.post('/register', data=dict(
        name='Test User',
        email='test@example.com',
        password=valid_password,
        password2=valid_password
    ), follow_redirects=True)
    assert rv.status_code == 200
    assert b'Account created. Please log in.' in rv.data

    # Test that the user can now log in
    rv = client.post('/login', data=dict(
        email='test@example.com',
        password=valid_password
    ), follow_redirects=True)
    assert rv.status_code == 200
    assert b'Dashboard' in rv.data  # Assuming 'Dashboard' is on the destination page
