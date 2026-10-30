import os
from dotenv import load_dotenv

# Get the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file if it exists
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base application configuration."""
    # Secret key for signing session cookies and CSRF tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'blogsphere-dev-super-secret-key-2026'

    # Database configuration - defaults to SQLite in instance folder
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'blogsphere.db')
    
    # Disable SQLAlchemy event system modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Application settings
    APP_NAME = "BlogSphere"
    POSTS_PER_PAGE = 6
