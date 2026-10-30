import pytest
from app import create_app, db
from app.models import ContactMessage
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.session.remove()
        db.drop_all()

def test_home_page(client):
    """Test that the homepage loads successfully with status code 200."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'BlogSphere' in response.data
    assert b'Where Ideas Connect' in response.data

def test_about_page(client):
    """Test that the about page loads successfully with status code 200."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About BlogSphere' in response.data
    assert b'8-Week Internship Development Roadmap' in response.data

def test_contact_page_get(client):
    """Test that the contact page GET request returns the form."""
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'Send an Inquiry' in response.data

def test_contact_page_post(client):
    """Test that submitting the contact form saves the message in the database."""
    response = client.post('/contact', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'subject': 'Week 1 Verification',
        'message': 'Testing database connectivity and form submission.'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Your message has been received' in response.data

    # Verify message in database
    msg = ContactMessage.query.filter_by(email='test@example.com').first()
    assert msg is not None
    assert msg.name == 'Test User'
    assert msg.subject == 'Week 1 Verification'
