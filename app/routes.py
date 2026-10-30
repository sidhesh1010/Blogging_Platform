from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models import ContactMessage

# Define the main blueprint for core application routes
main = Blueprint('main', __name__)

# Sample featured articles for Week 1 demonstration of layout and UI
SAMPLE_POSTS = [
    {
        'id': 1,
        'title': 'Getting Started with Flask 3: Modern Web Development in Python',
        'summary': 'Learn the fundamentals of building scalable, production-grade web applications using the latest Flask 3 architecture and SQLAlchemy.',
        'category': 'Python',
        'author': 'Sidhesh (Lead Dev)',
        'author_role': 'Software Intern',
        'avatar': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80',
        'date': 'Oct 28, 2026',
        'read_time': '5 min read',
        'featured': True,
        'image': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=900&auto=format&fit=crop&q=80'
    },
    {
        'id': 2,
        'title': 'Mastering Clean Architecture & Database Design in Flask',
        'summary': 'A practical deep dive into the Application Factory pattern, database migrations, and clean separation of concerns.',
        'category': 'Architecture',
        'author': 'Alex Rivers',
        'author_role': 'Backend Engineer',
        'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80',
        'date': 'Oct 29, 2026',
        'read_time': '8 min read',
        'featured': False,
        'image': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=900&auto=format&fit=crop&q=80'
    },
    {
        'id': 3,
        'title': 'UI/UX Best Practices for Content-Heavy Web Platforms',
        'summary': 'How modern typography, generous whitespace, and responsive grids elevate the reading experience for high-traffic blogs.',
        'category': 'UI/UX Design',
        'author': 'Elena Rostova',
        'author_role': 'Product Designer',
        'avatar': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&auto=format&fit=crop&q=80',
        'date': 'Oct 29, 2026',
        'read_time': '4 min read',
        'featured': False,
        'image': 'https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=900&auto=format&fit=crop&q=80'
    },
    {
        'id': 4,
        'title': 'Demystifying Full-Stack Authentication: Security First',
        'summary': 'Session cookies, Werkzeug password hashing, and CSRF protection explained simply for beginners and professional developers.',
        'category': 'Security',
        'author': 'Marcus Vance',
        'author_role': 'Security Specialist',
        'avatar': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80',
        'date': 'Oct 30, 2026',
        'read_time': '6 min read',
        'featured': False,
        'image': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=900&auto=format&fit=crop&q=80'
    }
]

@main.route('/')
def index():
    """
    Home page route.
    Renders the hero section, featured blog posts, and platform statistics.
    """
    featured_post = SAMPLE_POSTS[0]
    recent_posts = SAMPLE_POSTS[1:]
    categories = ['All', 'Python', 'Architecture', 'UI/UX Design', 'Security', 'Career']
    return render_template(
        'index.html',
        featured_post=featured_post,
        recent_posts=recent_posts,
        categories=categories
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
