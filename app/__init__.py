import os
import click
from flask import Flask
from .extensions import db, login_manager
from .config import Config

from .blueprints.auth import bp as auth_bp
from .blueprints.org import bp as org_bp
from .blueprints.jobs import bp as jobs_bp
from .blueprints.assessments import bp as assess_bp
from .blueprints.media import bp as media_bp
from .blueprints.api import bp as api_bp

from .models import user, org, ergo, media  # noqa


def create_app(config_object: type | None = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object or Config())

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(org_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(assess_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # ---- CLI Commands ----
    @app.cli.command("db-init")
    def db_init():
        with app.app_context():
            db.create_all()
            print("Database initialized")

    from .models.user import User

    @app.cli.command("db-ensure-roles")
    def db_ensure_roles():
        """Try to add 'role' column to user table (SQLite). Safe to run multiple times."""
        from sqlalchemy import text
        try:
            with app.app_context():
                db.session.execute(text("ALTER TABLE user ADD COLUMN role VARCHAR(20)"))
                db.session.commit()
                print("Added role column to user table.")
        except Exception as e:
            print("Skipping role column add (likely exists):", e)

    @app.cli.command("promote-admin")
    @click.argument("email")
    def promote_admin(email):
        with app.app_context():
            u = User.query.filter_by(email=email.lower()).first()
            if not u:
                print("User not found:", email)
                return
            u.role = "Admin"
            db.session.commit()
            print("Promoted to Admin:", u.email)

    @app.cli.command("create-user")
    @click.argument("name")
    @click.argument("email")
    @click.argument("password")
    @click.option("--role", default="Assessor", type=click.Choice(["Admin", "Assessor", "Viewer"]))
    def create_user(name, email, password, role):
        from werkzeug.security import generate_password_hash
        with app.app_context():
            if User.query.filter_by(email=email.lower()).first():
                print("Email already exists.")
                return
            u = User(
                name=name,
                email=email.lower(),
                password_hash=generate_password_hash(password),
                role=role,
            )
            db.session.add(u)
            db.session.commit()
            print("Created user:", email, "role:", role)

    # ---- Error handlers (INSIDE create_app) ----
    @app.errorhandler(403)
    def forbidden(e):
        from flask import render_template
        return render_template('errors/403.html'), 403

    return app
