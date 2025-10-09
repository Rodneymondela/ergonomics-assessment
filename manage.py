import click
from flask.cli import AppGroup
from app import create_app, db

app = create_app()
seed = AppGroup("seed")

@seed.command("demo")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def demo(password):
    """Creates a demo user."""
    from app.models.user import User
    from werkzeug.security import generate_password_hash
    u = User(name="Demo", email="demo@example.com", password_hash=generate_password_hash(password))
    db.session.add(u)
    db.session.commit()
    print("Demo user created: demo@example.com")

app.cli.add_command(seed)
