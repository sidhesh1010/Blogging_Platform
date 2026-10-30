import os
import pytest
from app import create_app, db
from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig, get_database_url

@pytest.fixture
def app_instance():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

def test_health_check_endpoint(client):
    """Health check endpoint returns 200 OK with operational metadata and database connection status."""
    res = client.get('/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data is not None
    assert data['status'] == 'healthy'
    assert data['database'] == 'connected'
    assert data['app'] == 'BlogSphere'
    assert 'version' in data

def test_config_environments_hierarchy():
    """Verify distinct configuration classes for development, testing, and production."""
    # Development
    assert DevelopmentConfig.DEBUG is True
    assert DevelopmentConfig.ENV == 'development'

    # Testing
    assert TestingConfig.TESTING is True
    assert TestingConfig.WTF_CSRF_ENABLED is False
    assert TestingConfig.SQLALCHEMY_DATABASE_URI == 'sqlite:///:memory:'

    # Production
    assert ProductionConfig.DEBUG is False
    assert ProductionConfig.TESTING is False
    assert ProductionConfig.ENV == 'production'

def test_production_security_settings():
    """ProductionConfig enforces HTTPS secure cookies and XSS/CSRF hardened headers."""
    assert ProductionConfig.SESSION_COOKIE_SECURE is True
    assert ProductionConfig.SESSION_COOKIE_HTTPONLY is True
    assert ProductionConfig.REMEMBER_COOKIE_HTTPONLY is True
    assert ProductionConfig.SESSION_COOKIE_SAMESITE == 'Lax'

def test_postgres_url_normalization(monkeypatch):
    """Cloud providers like Render/Heroku provide legacy postgres:// URIs; must be rewritten for SQLAlchemy 2.0+."""
    legacy_url = "postgres://user:secret@ec2-host.compute.amazonaws.com:5432/blogsphere_prod"
    monkeypatch.setenv("DATABASE_URL", legacy_url)
    
    normalized = get_database_url()
    assert normalized.startswith("postgresql://")
    assert "user:secret@ec2-host" in normalized

def test_standard_db_url_passthrough(monkeypatch):
    """Standard postgresql:// and sqlite:/// URIs pass through without unwanted alteration."""
    pg_url = "postgresql://user:pass@localhost:5432/testdb"
    monkeypatch.setenv("DATABASE_URL", pg_url)
    assert get_database_url() == pg_url

    sqlite_url = "sqlite:///custom_path.db"
    monkeypatch.setenv("DATABASE_URL", sqlite_url)
    assert get_database_url() == sqlite_url

def test_create_app_environment_string_factory():
    """Factory handles string environment names ('production', 'development', 'testing')."""
    prod_app = create_app('production')
    assert prod_app.config['ENV'] == 'production'
    assert prod_app.config['DEBUG'] is False
    assert prod_app.config['SESSION_COOKIE_SECURE'] is True

    dev_app = create_app('development')
    assert dev_app.config['ENV'] == 'development'
    assert dev_app.config['DEBUG'] is True

    test_app = create_app('testing')
    assert test_app.config['TESTING'] is True
    assert test_app.config['WTF_CSRF_ENABLED'] is False

def test_wsgi_app_callable():
    """Verify run.py exports WSGI-compatible 'app' callable for Gunicorn/Waitress."""
    import run
    assert hasattr(run, 'app')
    assert run.app is not None
    assert hasattr(run.app, 'wsgi_app')
