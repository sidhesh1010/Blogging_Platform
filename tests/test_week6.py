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

def create_author(app, username, email):
    with app.app_context():
        user = User(username=username, email=email)
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user.id

def create_post(app, author_id, title, content, category='Python', tags=''):
    with app.app_context():
        post = BlogPost(
            title=title,
            content=content,
            category=category,
            tags=tags,
            author_id=author_id
        )
        db.session.add(post)
        db.session.commit()
        return post.id

def create_comment(app, user_id, post_id, content):
    with app.app_context():
        c = Comment(user_id=user_id, post_id=post_id, content=content)
        db.session.add(c)
        db.session.commit()
        return c.id

def test_search_by_title(client, app_instance):
    """Search query matching post title returns expected result and excludes non-matches."""
    author_id = create_author(app_instance, 'search_writer', 'search1@test.com')
    create_post(app_instance, author_id, 'Deep Dive into FastAPI Architecture', 'FastAPI is an async framework.', 'Python')
    create_post(app_instance, author_id, 'Mastering CSS Grid Layouts', 'CSS Grid simplifies web interfaces.', 'UI/UX Design')

    res = client.get('/?q=FastAPI')
    assert res.status_code == 200
    assert b'Deep Dive into FastAPI Architecture' in res.data
    assert b'Mastering CSS Grid Layouts' not in res.data

def test_search_by_content(client, app_instance):
    """Search query matching article content returns the post even if title differs."""
    author_id = create_author(app_instance, 'content_writer', 'search2@test.com')
    create_post(app_instance, author_id, 'Modern Cloud Patterns', 'We break down microservices orchestrations and kubernetes.', 'Architecture')
    create_post(app_instance, author_id, 'Cooking with Python', 'A culinary journey using computer recipes.', 'General')

    res = client.get('/?q=microservices')
    assert res.status_code == 200
    assert b'Modern Cloud Patterns' in res.data
    assert b'Cooking with Python' not in res.data

def test_search_by_author_username(client, app_instance):
    """Search query matching author username discovers stories written by that author."""
    author1_id = create_author(app_instance, 'guido_fan', 'guido@test.com')
    author2_id = create_author(app_instance, 'brendan_fan', 'brendan@test.com')

    create_post(app_instance, author1_id, 'Python 3.13 Innovations', 'Discussing GIL-free python.', 'Python')
    create_post(app_instance, author2_id, 'JavaScript Engine Internals', 'V8 engine optimization secrets.', 'Architecture')

    res = client.get('/?q=guido_fan')
    assert res.status_code == 200
    assert b'Python 3.13 Innovations' in res.data
    assert b'JavaScript Engine Internals' not in res.data

def test_search_case_insensitivity(client, app_instance):
    """Search query is strictly case-insensitive."""
    author_id = create_author(app_instance, 'case_writer', 'case@test.com')
    create_post(app_instance, author_id, 'PostgreSQL Indexing Tricks', 'B-Tree vs GIN indexes in SQL databases.', 'Architecture')

    res = client.get('/?q=postgresql')
    assert res.status_code == 200
    assert b'PostgreSQL Indexing Tricks' in res.data

    res_upper = client.get('/?q=POSTGRESQL')
    assert res_upper.status_code == 200
    assert b'PostgreSQL Indexing Tricks' in res_upper.data

def test_category_filter(client, app_instance):
    """Category filter returns only stories belonging to selected category."""
    author_id = create_author(app_instance, 'cat_writer', 'cat@test.com')
    create_post(app_instance, author_id, 'Security Checklist 2026', 'Zero trust architecture guidance.', 'Security')
    create_post(app_instance, author_id, 'Figma to Code Pipeline', 'Design token automation in web development.', 'UI/UX Design')

    res = client.get('/?category=Security')
    assert res.status_code == 200
    assert b'Security Checklist 2026' in res.data
    assert b'Figma to Code Pipeline' not in res.data

def test_tag_filtering(client, app_instance):
    """Tag filter returns only posts matching the requested tag."""
    author_id = create_author(app_instance, 'tag_writer', 'tag@test.com')
    create_post(app_instance, author_id, 'Containerizing Flask Applications', 'Docker tutorial.', 'Python', tags='docker, devops, flask')
    create_post(app_instance, author_id, 'Vanilla JavaScript DOM Tricks', 'Zero dependency web design.', 'UI/UX Design', tags='javascript, frontend')

    res = client.get('/?tag=docker')
    assert res.status_code == 200
    assert b'Containerizing Flask Applications' in res.data
    assert b'Vanilla JavaScript DOM Tricks' not in res.data

def test_sorting_options(client, app_instance):
    """Sorting by popular orders by comment count descending."""
    author_id = create_author(app_instance, 'sort_writer', 'sort@test.com')
    p1 = create_post(app_instance, author_id, 'Post Without Comments', 'Content A', 'Python')
    p2 = create_post(app_instance, author_id, 'Post With Many Comments', 'Content B', 'Python')

    # Add 3 comments to p2
    create_comment(app_instance, author_id, p2, 'First reaction')
    create_comment(app_instance, author_id, p2, 'Second opinion')
    create_comment(app_instance, author_id, p2, 'Third insight')

    res = client.get('/?sort=popular')
    assert res.status_code == 200
    # In popular sort, post with most comments should appear before post with no comments
    p2_pos = res.data.find(b'Post With Many Comments')
    p1_pos = res.data.find(b'Post Without Comments')
    assert p2_pos != -1
    assert p1_pos != -1
    assert p2_pos < p1_pos

def test_server_side_pagination_and_query_preservation(client, app_instance):
    """Server-side pagination divides 13 posts across pages (per_page=6) and preserves query params."""
    author_id = create_author(app_instance, 'page_writer', 'page@test.com')

    # Create 13 posts tagged with 'scalability'
    for i in range(1, 14):
        create_post(app_instance, author_id, f'Scalability Lesson #{i:02d}', f'Content for item {i}', 'Architecture', tags='scalability')

    # Page 1 with tag filter
    res_p1 = client.get('/?tag=scalability&page=1')
    assert res_p1.status_code == 200
    assert b'Page 1 of 3' in res_p1.data
    assert b'page=2' in res_p1.data
    assert b'tag=scalability' in res_p1.data

    # Page 2
    res_p2 = client.get('/?tag=scalability&page=2')
    assert res_p2.status_code == 200
    assert b'Page 2 of 3' in res_p2.data
    assert b'page=1' in res_p2.data
    assert b'page=3' in res_p2.data

    # Page 3 (final 1 post)
    res_p3 = client.get('/?tag=scalability&page=3')
    assert res_p3.status_code == 200
    assert b'Page 3 of 3' in res_p3.data

def test_empty_search_feedback(client, app_instance):
    """Searching for a non-existent keyword displays the empty search alert and reset button."""
    author_id = create_author(app_instance, 'empty_writer', 'empty@test.com')
    create_post(app_instance, author_id, 'Standard Article', 'Simple content', 'General')

    res = client.get('/?q=UnmatchedKeywordZyx123')
    assert res.status_code == 200
    assert b'No Matching Stories Found' in res.data
    assert b'UnmatchedKeywordZyx123' in res.data
    assert b'Reset Filters' in res.data
