from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models import ContactMessage, BlogPost, User, Comment

# Define the main blueprint for core application routes
main = Blueprint('main', __name__)

# Sample featured articles fallback if no articles have been published yet
SAMPLE_POSTS = [
    {
        'id': 1,
        'title': 'Getting Started with Flask 3: Modern Web Development in Python',
        'summary': 'Learn the fundamentals of building scalable, production-grade web applications using the latest Flask 3 architecture and SQLAlchemy.',
        'category': 'Python',
        'author': 'Sidhesh (Lead Dev)',
        'author_name': 'Sidhesh (Lead Dev)',
        'author_role': 'Software Intern',
        'avatar': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80',
        'date': 'Oct 28, 2026',
        'read_time': '5 min read',
        'featured': True,
        'image': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=900&auto=format&fit=crop&q=80',
        'is_sample': True
    },
    {
        'id': 2,
        'title': 'Mastering Clean Architecture & Database Design in Flask',
        'summary': 'A practical deep dive into the Application Factory pattern, database migrations, and clean separation of concerns.',
        'category': 'Architecture',
        'author': 'Alex Rivers',
        'author_name': 'Alex Rivers',
        'author_role': 'Backend Engineer',
        'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80',
        'date': 'Oct 29, 2026',
        'read_time': '8 min read',
        'featured': False,
        'image': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=900&auto=format&fit=crop&q=80',
        'is_sample': True
    },
    {
        'id': 3,
        'title': 'UI/UX Best Practices for Content-Heavy Web Platforms',
        'summary': 'How modern typography, generous whitespace, and responsive grids elevate the reading experience for high-traffic blogs.',
        'category': 'UI/UX Design',
        'author': 'Elena Rostova',
        'author_name': 'Elena Rostova',
        'author_role': 'Product Designer',
        'avatar': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&auto=format&fit=crop&q=80',
        'date': 'Oct 29, 2026',
        'read_time': '4 min read',
        'featured': False,
        'image': 'https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=900&auto=format&fit=crop&q=80',
        'is_sample': True
    },
    {
        'id': 4,
        'title': 'Demystifying Full-Stack Authentication: Security First',
        'summary': 'Session cookies, Werkzeug password hashing, and CSRF protection explained simply for beginners and professional developers.',
        'category': 'Security',
        'author': 'Marcus Vance',
        'author_name': 'Marcus Vance',
        'author_role': 'Security Specialist',
        'avatar': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80',
        'date': 'Oct 30, 2026',
        'read_time': '6 min read',
        'featured': False,
        'image': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=900&auto=format&fit=crop&q=80',
        'is_sample': True
    }
]

@main.route('/')
def index():
    """
    Home page route with full-text search, category and tag filtering,
    sorting, and server-side pagination (Week 6 Milestone).
    """
    q = request.args.get('q', '').strip()
    category = request.args.get('category', 'All').strip()
    tag = request.args.get('tag', '').strip()
    sort = request.args.get('sort', 'newest').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 6

    has_real_posts = (BlogPost.query.count() > 0)
    categories = ['All', 'Python', 'Architecture', 'UI/UX Design', 'Security', 'AI & ML', 'Career', 'General']

    if has_real_posts:
        query = BlogPost.query

        # Multi-field search across title, content, tags, category, and author username
        if q:
            term = f"%{q}%"
            query = query.outerjoin(User, BlogPost.author_id == User.id).filter(
                db.or_(
                    BlogPost.title.ilike(term),
                    BlogPost.content.ilike(term),
                    BlogPost.tags.ilike(term),
                    BlogPost.category.ilike(term),
                    User.username.ilike(term)
                )
            )

        # Category filter
        if category and category.lower() != 'all':
            query = query.filter(BlogPost.category.ilike(category))

        # Tag filter
        if tag:
            clean_tag = tag.lstrip('#').strip()
            query = query.filter(BlogPost.tags.ilike(f"%{clean_tag}%"))

        # Sorting
        if sort == 'oldest':
            query = query.order_by(BlogPost.created_at.asc())
        elif sort == 'popular':
            query = query.outerjoin(Comment).group_by(BlogPost.id).order_by(
                db.func.count(Comment.id).desc(),
                BlogPost.created_at.desc()
            )
        else:  # newest default
            query = query.order_by(BlogPost.created_at.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        posts = pagination.items
        total_results = pagination.total

        is_filtered = bool(q or (category and category.lower() != 'all') or tag or (sort and sort != 'newest') or page > 1)
        if not is_filtered and posts:
            featured_post = posts[0]
            display_posts = posts[1:]
        else:
            featured_post = None
            display_posts = posts

    else:
        # Fallback to SAMPLE_POSTS with in-memory filtering and mock pagination
        filtered_samples = list(SAMPLE_POSTS)
        if q:
            q_lower = q.lower()
            filtered_samples = [
                p for p in filtered_samples
                if q_lower in p['title'].lower() or q_lower in p['summary'].lower() or q_lower in p['category'].lower() or q_lower in p['author'].lower()
            ]
        if category and category.lower() != 'all':
            filtered_samples = [p for p in filtered_samples if p['category'].lower() == category.lower()]

        total_results = len(filtered_samples)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        display_posts = filtered_samples[start_idx:end_idx]

        class MockPagination:
            def __init__(self, page, per_page, total, items):
                self.page = page
                self.per_page = per_page
                self.total = total
                self.items = items
                self.pages = max(1, (total + per_page - 1) // per_page)
                self.has_prev = page > 1
                self.has_next = page < self.pages
                self.prev_num = page - 1
                self.next_num = page + 1

            def iter_pages(self, left_edge=1, right_edge=1, left_current=2, right_current=2):
                return list(range(1, self.pages + 1))

        pagination = MockPagination(page, per_page, total_results, display_posts)
        is_filtered = bool(q or (category and category.lower() != 'all') or tag or page > 1)
        if not is_filtered and display_posts:
            featured_post = display_posts[0]
            display_posts = display_posts[1:]
        else:
            featured_post = None

    return render_template(
        'index.html',
        featured_post=featured_post,
        recent_posts=display_posts,
        pagination=pagination,
        categories=categories,
        has_real_posts=has_real_posts,
        q=q,
        selected_category=category,
        tag=tag,
        sort=sort,
        total_results=total_results,
        is_filtered=is_filtered
    )

@main.route('/about')
def about():
    """
    About page route.
    Presents the BlogSphere mission, architecture, and 8-week internship roadmap.
    """
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Contact page route.
    Handles GET for showing form and POST for saving inquiries to SQLite.
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        # Simple validation
        if not name or not email or not subject or not message:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('main.contact'))

        try:
            # Store in SQLite database
            contact_msg = ContactMessage(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            db.session.add(contact_msg)
            db.session.commit()

            flash(f'Thank you, {name}! Your message has been received. We will get back to you soon.', 'success')
            return redirect(url_for('main.contact'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while saving your message. Please try again.', 'danger')
            return redirect(url_for('main.contact'))

    return render_template('contact.html')

# =========================================================================
# Custom Application Error Handlers (Week 4 UX Polish)
# =========================================================================
@main.app_errorhandler(404)
def not_found_error(error):
    """Render custom 404 Page Not Found error view."""
    return render_template('errors/404.html'), 404

@main.app_errorhandler(403)
def forbidden_error(error):
    """Render custom 403 Forbidden Access error view."""
    return render_template('errors/403.html'), 403

@main.app_errorhandler(500)
def internal_error(error):
    """Render custom 500 Internal Server error view and rollback session."""
    db.session.rollback()
    return render_template('errors/500.html'), 500
