# tests/conftest.py
import sys
import pathlib
import pytest
from sqlalchemy.pool import StaticPool

# Make "import app" resolve to ./app
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app
from app.extensions import db as _db  # your SQLAlchemy() instance

@pytest.fixture(scope="session")
def app(tmp_path_factory):
    # temp upload dir so tests don't write into your repo
    uploads_dir = tmp_path_factory.mktemp("uploads")

    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        UPLOAD_FOLDER=str(uploads_dir),
        # single in-memory DB shared by the session
        SQLALCHEMY_DATABASE_URI="sqlite://",
        SQLALCHEMY_ENGINE_OPTIONS={
            "connect_args": {"check_same_thread": False},
            "poolclass": StaticPool,
        },
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # create tables once for the session
    with app.app_context():
        _db.drop_all()
        _db.create_all()

    return app

@pytest.fixture(autouse=True)
def _push_app_ctx(app):
    """Bind db.session by pushing an app context for every test."""
    ctx = app.app_context()
    ctx.push()
    try:
        yield
        _db.session.rollback()   # keep tests isolated
    finally:
        ctx.pop()

@pytest.fixture()
def client(app):
    return app.test_client()
