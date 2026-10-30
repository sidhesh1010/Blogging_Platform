import pytest
from app import create_app, db
from app.models import User
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

def test_password_hashing():
    """Verify password hashing with Werkzeug and check_password verification."""
    user = User(username='security_test', email='security@test.com')
    user.set_password('SecretPassword123')
    assert user.password_hash != 'SecretPassword123'
    assert user.check_password('SecretPassword123') is True
    assert user.check_password('WrongPassword') is False

def test_user_registration(client, app_instance):
    """Test successful user registration and database creation."""
    response = client.post('/register', data={
        'username': 'john_doe',
        'email': 'john@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Your account has been created successfully' in response.data

    with app_instance.app_context():
        user = User.query.filter_by(username='john_doe').first()
        assert user is not None
        assert user.email == 'john@example.com'
        assert user.check_password('password123') is True

def test_duplicate_registration_prevention(client, app_instance):
    """Ensure duplicate usernames and emails cannot be registered."""
    with app_instance.app_context():
        u = User(username='existing_user', email='existing@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

    # Attempt duplicate username
    res_dup_username = client.post('/register', data={
        'username': 'existing_user',
        'email': 'other@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert b'This username is already taken' in res_dup_username.data

    # Attempt duplicate email
    res_dup_email = client.post('/register', data={
        'username': 'new_user',
        'email': 'existing@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert b'An account with this email already exists' in res_dup_email.data

def test_login_and_logout(client, app_instance):
    """Test login via email and username, and logout functionality."""
    with app_instance.app_context():
        u = User(username='alice', email='alice@example.com')
        u.set_password('alicepassword')
        db.session.add(u)
        db.session.commit()

    # Login with username
    res = client.post('/login', data={
        'email_or_username': 'alice',
        'password': 'alicepassword'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Welcome back, alice!' in res.data
    assert b'Sign Out' in res.data

    # Logout
    res_logout = client.get('/logout', follow_redirects=True)
    assert res_logout.status_code == 200
    assert b'You have been logged out securely' in res_logout.data
    assert b'Sign In' in res_logout.data

def test_login_invalid_credentials(client, app_instance):
    """Test login with wrong password."""
    with app_instance.app_context():
        u = User(username='bob', email='bob@example.com')
        u.set_password('correctpass')
        db.session.add(u)
        db.session.commit()

    res = client.post('/login', data={
        'email_or_username': 'bob',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert b'Invalid email/username or password' in res.data

def test_protected_route_and_profile_update(client, app_instance):
    """Test that /profile requires login and allows updating info."""
    # Unauthenticated access to /profile should redirect to /login
    res_unauth = client.get('/profile')
    assert res_unauth.status_code == 302
    assert '/login' in res_unauth.headers['Location']

    # Create and login user
    with app_instance.app_context():
        u = User(username='carol', email='carol@example.com', bio='Old bio')
        u.set_password('carolpass')
        db.session.add(u)
        db.session.commit()

    client.post('/login', data={
        'email_or_username': 'carol',
        'password': 'carolpass'
    })

    # Access /profile as logged-in user
    res_profile = client.get('/profile')
    assert res_profile.status_code == 200
    assert b'Edit Account Profile' in res_profile.data
    assert b'carol@example.com' in res_profile.data

    # Update profile
    res_update = client.post('/profile', data={
        'username': 'carol_updated',
        'bio': 'New updated bio for BlogSphere'
    }, follow_redirects=True)
    assert res_update.status_code == 200
    assert b'Your profile has been updated successfully' in res_update.data

    with app_instance.app_context():
        updated_user = User.query.filter_by(email='carol@example.com').first()
        assert updated_user.username == 'carol_updated'
        assert updated_user.bio == 'New updated bio for BlogSphere'
