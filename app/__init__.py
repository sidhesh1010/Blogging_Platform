import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Initialize extensions outside the factory
db = SQLAlchemy()
migrate = Migrate()

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

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Import models so SQLAlchemy is aware of them
    from app import models

    return app
