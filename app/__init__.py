import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Initialize extensions outside the factory
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Configure Flask-Login defaults
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please sign in to access your profile.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    """
    Application Factory Pattern for BlogSphere.
    Allows easy configuration for development, testing, and production.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure the instance folder exists for SQLite database storage
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize extensions with the application instance
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.posts import posts as posts_blueprint
    app.register_blueprint(posts_blueprint)

    # Import models so SQLAlchemy and Flask-Login are aware of them
    from app import models

    return app
