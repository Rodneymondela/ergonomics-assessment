import pytest
from app import create_app, db as _db
@pytest.fixture()
def app(tmp_path):
    class TestConfig:
        SECRET_KEY = 'test'
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path/'test.db'}"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        UPLOAD_FOLDER = tmp_path.as_posix()
        TESTING = True
    app = create_app(TestConfig)
    with app.app_context():
        _db.create_all()
    yield app
@pytest.fixture()
def client(app):
    return app.test_client()
