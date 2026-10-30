import pytest
from app import create_app, db
from app.models import User, BlogPost, Comment
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

def create_user(app_instance, username='testuser', email='test@example.com'):
    with app_instance.app_context():
        user = User(username=username, email=email)
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user.id

def login(client, username='testuser', password='password123'):
    return client.post('/login', data={
        'email_or_username': username,
        'password': password
    }, follow_redirects=True)

def create_post(app_instance, author_id, title='Discussion Article'):
    with app_instance.app_context():
        post = BlogPost(
            title=title,
            category='Python',
            content='Let us discuss modern web frameworks and architecture patterns.',
            author_id=author_id
        )
        db.session.add(post)
        db.session.commit()
        return post.id

def test_anonymous_user_cannot_comment(client, app_instance):
    """Anonymous visitors must be redirected to login when trying to post a comment."""
    author_id = create_user(app_instance, 'author_user', 'author@test.com')
    post_id = create_post(app_instance, author_id)

    res = client.post(f'/post/{post_id}/comment', data={
        'content': 'Great insights on Flask architecture!'
    })
    assert res.status_code == 302
    assert '/login' in res.headers['Location']

def test_authenticated_user_can_comment(client, app_instance):
    """Authenticated user can successfully post a comment to an article."""
    author_id = create_user(app_instance, 'author_user', 'author@test.com')
    reader_id = create_user(app_instance, 'reader_user', 'reader@test.com')
    post_id = create_post(app_instance, author_id)

    login(client, 'reader_user', 'password123')

    res = client.post(f'/post/{post_id}/comment', data={
        'content': 'This architectural breakdown was very clear and actionable.'
    }, follow_redirects=True)

    assert res.status_code == 200
    assert b'Your response has been published successfully!' in res.data
    assert b'This architectural breakdown was very clear and actionable.' in res.data
    assert b'reader_user' in res.data

    with app_instance.app_context():
        comment = Comment.query.filter_by(content='This architectural breakdown was very clear and actionable.').first()
        assert comment is not None
        assert comment.user_id == reader_id
        assert comment.post_id == post_id
        assert comment.author_name == 'reader_user'
        assert comment.post.comments.count() == 1

def test_comment_validation_empty_or_short(client, app_instance):
    """Comments shorter than 3 characters or empty must fail validation."""
    author_id = create_user(app_instance, 'author_user', 'author@test.com')
    reader_id = create_user(app_instance, 'reader_user', 'reader@test.com')
    post_id = create_post(app_instance, author_id)

    login(client, 'reader_user', 'password123')

    # Attempt to post comment with only 2 characters
    res = client.post(f'/post/{post_id}/comment', data={
        'content': 'hi'
    }, follow_redirects=True)

    assert res.status_code == 200
    assert b'Response must be between 3 and 1000 characters.' in res.data

    with app_instance.app_context():
        assert Comment.query.count() == 0

def test_comment_author_can_delete_own_comment(client, app_instance):
    """Author of a comment can delete their own response."""
    author_id = create_user(app_instance, 'author_user', 'author@test.com')
    reader_id = create_user(app_instance, 'commenter', 'commenter@test.com')
    post_id = create_post(app_instance, author_id)

    with app_instance.app_context():
        comment = Comment(
            content='I want to delete this comment.',
            user_id=reader_id,
            post_id=post_id
        )
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id

    # Log in as comment author
    login(client, 'commenter', 'password123')

    # Delete comment
    res = client.post(f'/comment/{comment_id}/delete', follow_redirects=True)
    assert res.status_code == 200
    assert b'The response has been removed.' in res.data

    with app_instance.app_context():
        assert Comment.query.get(comment_id) is None

def test_post_author_can_moderate_any_comment(client, app_instance):
    """Article author can moderate and delete any reader comment on their article."""
    author_id = create_user(app_instance, 'post_author', 'postauthor@test.com')
    spammer_id = create_user(app_instance, 'spammer', 'spammer@test.com')
    post_id = create_post(app_instance, author_id)

    with app_instance.app_context():
        comment = Comment(
            content='Spam message that violates community guidelines.',
            user_id=spammer_id,
            post_id=post_id
        )
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id

    # Log in as post author (moderator)
    login(client, 'post_author', 'password123')

    # Moderate/delete comment
    res = client.post(f'/comment/{comment_id}/delete', follow_redirects=True)
    assert res.status_code == 200
    assert b'The response has been removed.' in res.data

    with app_instance.app_context():
        assert Comment.query.get(comment_id) is None

def test_unauthorized_user_cannot_delete_comment(client, app_instance):
    """Third-party users cannot delete comments they did not author on posts they do not own."""
    author_id = create_user(app_instance, 'author_user', 'author@test.com')
    commenter_id = create_user(app_instance, 'commenter', 'commenter@test.com')
    bystander_id = create_user(app_instance, 'bystander', 'bystander@test.com')
    post_id = create_post(app_instance, author_id)

    with app_instance.app_context():
        comment = Comment(
            content='Legitimate discussion comment.',
            user_id=commenter_id,
            post_id=post_id
        )
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id

    # Log in as bystander
    login(client, 'bystander', 'password123')

    # Attempt delete
    res = client.post(f'/comment/{comment_id}/delete')
    assert res.status_code == 403

    with app_instance.app_context():
        assert Comment.query.get(comment_id) is not None

def test_cascade_delete_post_removes_comments(app_instance):
    """Deleting a blog post cascades and removes all of its associated comments."""
    with app_instance.app_context():
        user = User(username='cascadetest', email='cascade@test.com')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        post = BlogPost(title='Cascade Post', category='AI & ML', content='Content', author=user)
        db.session.add(post)
        db.session.commit()

        c1 = Comment(content='Comment 1', author=user, post=post)
        c2 = Comment(content='Comment 2', author=user, post=post)
        db.session.add_all([c1, c2])
        db.session.commit()

        assert post.comments.count() == 2

        # Delete post
        db.session.delete(post)
        db.session.commit()

        # Comments should be cascade deleted
        assert Comment.query.count() == 0

def test_user_comments_counter_in_profile(client, app_instance):
    """User profile displays accurate comment counter."""
    user_id = create_user(app_instance, 'active_debater', 'debater@test.com')
    post_id = create_post(app_instance, user_id)

    with app_instance.app_context():
        c = Comment(content='Constructive feedback.', user_id=user_id, post_id=post_id)
        db.session.add(c)
        db.session.commit()

    login(client, 'active_debater', 'password123')
    res = client.get('/profile')
    assert res.status_code == 200
    assert b'Reader Responses' in res.data
    assert b'1' in res.data
