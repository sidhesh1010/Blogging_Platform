import os
from dotenv import load_dotenv

# Get the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file if it exists
load_dotenv(os.path.join(basedir, '.env'))

def get_database_url():
    """Normalize database URI with PostgreSQL compatibility (e.g. Render/Heroku postgres:// rewrite)."""
    raw_url = os.environ.get('DATABASE_URL')
    if raw_url:
        if raw_url.startswith('postgres://'):
            return raw_url.replace('postgres://', 'postgresql://', 1)
        return raw_url
    return 'sqlite:///' + os.path.join(basedir, 'instance', 'blogsphere.db')

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'blogsphere-dev-super-secret-key-2026'
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_NAME = "BlogSphere"
    POSTS_PER_PAGE = 6

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    ENV = 'development'

class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True
    ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production environment configuration with hardened cookie and session security."""
    DEBUG = False
    TESTING = False
    ENV = 'production'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
