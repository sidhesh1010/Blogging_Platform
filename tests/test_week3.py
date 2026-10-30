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

def create_test_user(app_instance, username='author1', email='author1@example.com'):
    with app_instance.app_context():
        user = User(username=username, email=email)
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user.id

def login(client, identifier='author1', password='password123'):
    return client.post('/login', data={
        'email_or_username': identifier,
        'password': password
    }, follow_redirects=True)

def test_create_post_requires_auth(client):
    """Anonymous visitors must be redirected to login when attempting to write a post."""
    res = client.get('/post/create')
    assert res.status_code == 302
    assert '/login' in res.headers['Location']

def test_create_post_success(client, app_instance):
    """Authenticated user can successfully create and publish a blog post."""
    user_id = create_test_user(app_instance, 'writer', 'writer@example.com')
    login(client, 'writer', 'password123')

    res = client.post('/post/create', data={
        'title': 'Deep Dive into Python Web Frameworks',
        'category': 'Python',
        'featured_image': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5',
        'content': 'This article covers Flask, FastAPI, and Django architectural trade-offs.'
    }, follow_redirects=True)

    assert res.status_code == 200
    assert b'Your article has been published successfully!' in res.data
    assert b'Deep Dive into Python Web Frameworks' in res.data
    assert b'writer' in res.data

    with app_instance.app_context():
        post = BlogPost.query.filter_by(title='Deep Dive into Python Web Frameworks').first()
        assert post is not None
        assert post.author_id == user_id
        assert post.category == 'Python'
        assert post.read_time() == '1 min read'

def test_view_post_detail(client, app_instance):
    """Public can view post details; 404 is returned for non-existent posts."""
    user_id = create_test_user(app_instance, 'reader_author', 'reader@example.com')
    with app_instance.app_context():
        post = BlogPost(
            title='Publicly Accessible Story',
            category='Architecture',
            content='Everyone can read this architectural insight without logging in.',
            author_id=user_id
        )
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    # View existing post
    res = client.get(f'/post/{post_id}')
    assert res.status_code == 200
    assert b'Publicly Accessible Story' in res.data
    assert b'Architecture' in res.data

    # View non-existent post
    res_404 = client.get('/post/99999')
    assert res_404.status_code == 404

def test_edit_post_by_author(client, app_instance):
    """Author can successfully edit and update their own post."""
    user_id = create_test_user(app_instance, 'editor', 'editor@example.com')
    with app_instance.app_context():
        post = BlogPost(
            title='Initial Draft Title',
            category='Security',
            content='Original content draft.',
            author_id=user_id
        )
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    # Log in as author
    login(client, 'editor', 'password123')

    # Access edit form
    res_get = client.get(f'/post/{post_id}/edit')
    assert res_get.status_code == 200
    assert b'Initial Draft Title' in res_get.data

    # Submit update
    res_post = client.post(f'/post/{post_id}/edit', data={
        'title': 'Revised and Polished Title',
        'category': 'Security',
        'featured_image': '',
        'content': 'Updated and expanded article content with security recommendations.'
    }, follow_redirects=True)

    assert res_post.status_code == 200
    assert b'Your article has been updated successfully!' in res_post.data
    assert b'Revised and Polished Title' in res_post.data

    with app_instance.app_context():
        updated = BlogPost.query.get(post_id)
        assert updated.title == 'Revised and Polished Title'
        assert updated.content == 'Updated and expanded article content with security recommendations.'

def test_edit_post_unauthorized_user(client, app_instance):
    """Non-authors receive 403 Forbidden when attempting to edit another user's post."""
    author_id = create_test_user(app_instance, 'original_author', 'orig@example.com')
    create_test_user(app_instance, 'intruder', 'intruder@example.com')

    with app_instance.app_context():
        post = BlogPost(
            title='Protected Story',
            category='General',
            content='Strictly private to the author for editing.',
            author_id=author_id
        )
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    # Log in as intruder
    login(client, 'intruder', 'password123')

    # Attempt to GET edit form
    res_get = client.get(f'/post/{post_id}/edit')
    assert res_get.status_code == 403

    # Attempt to POST update
    res_post = client.post(f'/post/{post_id}/edit', data={
        'title': 'Hacked Title',
        'category': 'General',
        'content': 'Malicious modification.'
    })
    assert res_post.status_code == 403

    # Verify content was NOT altered
    with app_instance.app_context():
        p = BlogPost.query.get(post_id)
        assert p.title == 'Protected Story'

def test_delete_post_by_author(client, app_instance):
    """Author can successfully delete their own post."""
    author_id = create_test_user(app_instance, 'deleter', 'deleter@example.com')
    with app_instance.app_context():
        post = BlogPost(
            title='Post To Delete',
            category='Career',
            content='Content soon to be removed.',
            author_id=author_id
        )
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    # Log in as author
    login(client, 'deleter', 'password123')

    # Delete post
    res = client.post(f'/post/{post_id}/delete', follow_redirects=True)
    assert res.status_code == 200
    assert b'Your article has been deleted successfully.' in res.data

    with app_instance.app_context():
        assert BlogPost.query.get(post_id) is None

def test_delete_post_unauthorized_user(client, app_instance):
    """Non-authors receive 403 Forbidden when attempting to delete another author's post."""
    author_id = create_test_user(app_instance, 'legit_author', 'legit@example.com')
    create_test_user(app_instance, 'bad_actor', 'bad@example.com')

    with app_instance.app_context():
        post = BlogPost(
            title='Safe Story',
            category='Python',
            content='Must survive unauthorized deletion attempts.',
            author_id=author_id
        )
        db.session.add(post)
        db.session.commit()
        post_id = post.id

    # Log in as bad actor
    login(client, 'bad_actor', 'password123')

    # Attempt delete
    res = client.post(f'/post/{post_id}/delete')
    assert res.status_code == 403

    # Verify post still exists in DB
    with app_instance.app_context():
        assert BlogPost.query.get(post_id) is not None

def test_user_post_relationship_and_cascade(app_instance):
    """Verify SQLAlchemy relationship and cascade deletion when user is removed."""
    with app_instance.app_context():
        user = User(username='cascadetest', email='cascade@example.com')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        post1 = BlogPost(title='Article 1', category='Python', content='Content 1', author=user)
        post2 = BlogPost(title='Article 2', category='Security', content='Content 2', author=user)
        db.session.add_all([post1, post2])
        db.session.commit()

        assert user.posts.count() == 2
        assert post1.author.username == 'cascadetest'

        # Delete user
        db.session.delete(user)
        db.session.commit()

        # Posts should be cascade deleted
        assert BlogPost.query.filter_by(title='Article 1').first() is None
        assert BlogPost.query.filter_by(title='Article 2').first() is None
