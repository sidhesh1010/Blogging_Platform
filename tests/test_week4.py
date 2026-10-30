import pytest
from app import create_app, db
from app.models import User, BlogPost
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app_instance():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

def create_author(app_instance, username='reader_fan', email='fan@example.com'):
    with app_instance.app_context():
        user = User(username=username, email=email)
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user.id

def test_reading_interface_components(client, app_instance):
    """Verify that Medium-inspired reading interface components are present in article view."""
    author_id = create_author(app_instance, 'tech_author', 'tech@example.com')
    with app_instance.app_context():
        post = BlogPost(
            title='Engineering High-Resilience Microservices',
            category='Architecture',
            content='## System Design\n\n> Architecture represents significant design decisions.\n\n```python\ndef handler(): pass\n```',
            author_id=author_id
        )
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    res = client.get(f'/post/{post_id}')
    assert res.status_code == 200

    # Reading progress bar
    assert b'readingProgressBar' in res.data
    assert b'reading-progress-container' in res.data

    # Reader Mode customization toolbar
    assert b'readerFontFamilyBtn' in res.data
    assert b'readerFontSmBtn' in res.data
    assert b'readerFontMdBtn' in res.data
    assert b'readerFontLgBtn' in res.data
    assert b'readerWidthBtn' in res.data
    assert b'articleReaderContainer' in res.data

    # Engagement and Bookmark components
    assert b'btn-bookmark-story' in res.data
    assert b'btnClap' in res.data
    assert b'btnCopyShareLink' in res.data

def test_theme_toggle_and_base_assets(client):
    """Verify Dark/Light theme switcher and floating back-to-top button in master layout."""
    res = client.get('/')
    assert res.status_code == 200

    # Theme toggle switcher
    assert b'themeToggleBtn' in res.data
    assert b'themeIcon' in res.data

    # Back to Top floating button
    assert b'backToTopBtn' in res.data

    # Static CSS and JS assets
    assert b'style.css' in res.data
    assert b'main.js' in res.data

def test_homepage_search_and_category_markup(client):
    """Verify homepage contains live real-time search input and empty results container."""
    res = client.get('/')
    assert res.status_code == 200

    # Search bar & empty result container
    assert b'articleSearchInput' in res.data
    assert b'noSearchResults' in res.data
    assert b'category-pill' in res.data

def test_custom_404_error_page(client):
    """Verify friendly custom 404 error page is returned for unknown URLs."""
    res = client.get('/this-route-does-not-exist-at-all-404')
    assert res.status_code == 404
    assert b'404' in res.data
    assert b'Lost in the Sphere' in res.data
    assert b'Return to Homepage' in res.data

def test_custom_403_error_page(client, app_instance):
    """Verify friendly custom 403 error page is returned when author authorization fails."""
    author_id = create_author(app_instance, 'legit_writer', 'legit@test.com')
    create_author(app_instance, 'unauth_user', 'unauth@test.com')

    with app_instance.app_context():
        post = BlogPost(
            title='Owner Protected Article',
            category='Security',
            content='Only author can edit.',
            author_id=author_id
        )
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    # Log in as unauthorized user
    client.post('/login', data={
        'email_or_username': 'unauth_user',
        'password': 'password123'
    })

    # Attempt to edit post
    res = client.get(f'/post/{post_id}/edit')
    assert res.status_code == 403
    assert b'403' in res.data
    assert b'Author Privileges Required' in res.data
    assert b'Restricted Area' in res.data

def test_responsive_viewport_and_semantic_html(client):
    """Verify mobile-friendly viewport meta tag and HTML5 semantic elements."""
    res = client.get('/')
    assert res.status_code == 200
    assert b'viewport' in res.data
    assert b'width=device-width' in res.data
    assert b'<header>' in res.data
    assert b'<nav' in res.data
