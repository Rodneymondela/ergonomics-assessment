from flask.cli import AppGroup
from app import create_app, db

app = create_app()
seed = AppGroup("seed")

@seed.command("demo"):
    from app.models.user import User
    from werkzeug.security import generate_password_hash
    u = User(name="Demo", email="demo@example.com", password_hash=generate_password_hash("demo"))
    db.session.add(u)
    db.session.commit()
    print("Demo user: demo@example.com / demo")

app.cli.add_command(seed)
