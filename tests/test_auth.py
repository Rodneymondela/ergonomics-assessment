from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash

def test_register_and_login(client):
    rv = client.post('/register', data=dict(name='T', email='t@e.co', password='x'), follow_redirects=True)
    assert rv.status_code == 200
    u = User(name='A', email='a@e.co', password_hash=generate_password_hash('x'))
    db.session.add(u); db.session.commit()
    rv = client.post('/login', data=dict(email='a@e.co', password='x'), follow_redirects=True)
    assert rv.status_code == 200
