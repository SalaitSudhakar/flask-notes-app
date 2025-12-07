"""Application factory and extensions for the Notes App.

This module centralizes the creation and configuration of the
Flask application. It defines the SQLAlchemy `db` object and the
`create_app` factory which sets up config, database, blueprints,
and login management.

Beginners: Using an application factory allows tests and tools to
create the app with different settings, and avoids side-effects at
import time.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Create the SQLAlchemy object here so models can import it:
# `from . import db`
db = SQLAlchemy()

# The filename for the SQLite database used by the app.
DB_NAME = "database.db"


def create_app():
    """Create and configure the Flask application.

    Steps performed:
    - Create the Flask app instance
    - Set secret key (used for sessions and flash messages)
    - Configure SQLAlchemy to use a local SQLite file
    - Initialize extensions (db, login manager)
    - Register blueprints (views and auth)
    - Ensure the database file exists
    """
    app = Flask(__name__)

    # SECRET_KEY is required for sessions and flash messages. In a real
    # project you should keep this secret and load it from environment
    # variables or a config file, not hard-coded.
    app.config["SECRET_KEY"] = "KAJFAKJFAKFJAU382942"

    # Build an absolute path to the database file (website/database.db)
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, DB_NAME)

    # Tell SQLAlchemy where the database lives. The three slashes mean
    # "absolute path" for SQLite: sqlite:////absolute/path
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    # Initialize SQLAlchemy with this app
    db.init_app(app)

    # Register blueprints (separate modules handling routes)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Import models so that db.create_all() knows about them.
    # Models import `db` from this package, so they must be imported
    # after `db` is defined.
    from .models import User, Note

    # Ensure the database file exists and tables are created.
    create_database(app, db_path)

    # Setup Flask-Login: tells Flask how to load a user from an id
    login_manager = LoginManager()
    # If a route is protected with @login_required, unauthenticated
    # users will be redirected to this endpoint name.
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # Flask-Login will call this with the stored user id (string).
        # We convert to int and query the User model.
        return User.query.get(int(id))

    return app


def create_database(app, db_path):
    """Create the SQLite database file and tables if missing.

    This function uses `app.app_context()` so SQLAlchemy can access
    the application configuration when creating tables.
    """
    if not os.path.exists(db_path):
        with app.app_context():
            # Create all tables that are defined by SQLAlchemy models
            db.create_all()
        print(f"✔ Database created at: {db_path}")
    else:
        print(f"✔ Database already exists at: {db_path}")
