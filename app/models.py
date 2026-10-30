import hashlib
import re
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    """
    User model for authentication, profile management, and blog authoring.
    Inherits UserMixin from Flask-Login for standard authentication properties.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.String(300), default="Passionate writer and reader on BlogSphere.")
    avatar = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship linking User to their authored blog posts
    posts = db.relationship('BlogPost', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and store the user's password securely using Werkzeug."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password against the stored secure hash."""
        return check_password_hash(self.password_hash, password)

    def get_avatar(self, size=128):
        """
        Return the custom avatar or generate a Gravatar URL from the user's email.
        """
        if self.avatar:
            return self.avatar
        digest = hashlib.md5(self.email.lower().strip().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    @property
    def posts_list(self):
        """Return the user's authored posts ordered newest first."""
        return self.posts.order_by(BlogPost.created_at.desc()).all()

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login user loader callback.
    Loads user from database by ID for active session management.
    """
    return User.query.get(int(user_id))


class BlogPost(db.Model):
    """
    BlogPost database model representing published articles.
    Contains title, content, category, author foreign key, and timestamps.
    """
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='General', index=True)
    featured_image = db.Column(db.String(255), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def snippet(self, length=160):
        """Extract a clean text snippet without HTML tags for card previews."""
        # Strip HTML tags using regex
        clean_text = re.sub('<[^<]+?>', '', self.content or '')
        clean_text = ' '.join(clean_text.split())
        if len(clean_text) <= length:
            return clean_text
        return clean_text[:length].rsplit(' ', 1)[0] + '...'

    def read_time(self):
        """Estimate reading time assuming an average speed of 200 words per minute."""
        clean_text = re.sub('<[^<]+?>', '', self.content or '')
        word_count = len(clean_text.split())
        minutes = max(1, round(word_count / 200))
        return f"{minutes} min read"

    def default_image(self):
        """Return featured image or a curated category fallback."""
        if self.featured_image:
            return self.featured_image
        # Curated aesthetic images by category
        category_images = {
            'Python': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=900&auto=format&fit=crop&q=80',
            'Architecture': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=900&auto=format&fit=crop&q=80',
            'UI/UX Design': 'https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=900&auto=format&fit=crop&q=80',
            'Security': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=900&auto=format&fit=crop&q=80',
            'AI & ML': 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=900&auto=format&fit=crop&q=80',
            'Career': 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=900&auto=format&fit=crop&q=80'
        }
        return category_images.get(self.category, 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=900&auto=format&fit=crop&q=80')

    @property
    def image(self):
        """Image URL accessor for template cards."""
        return self.default_image()

    @property
    def summary(self):
        """Summary snippet accessor for template cards."""
        return self.snippet(160)

    @property
    def date(self):
        """Formatted publication date string."""
        if self.created_at:
            return self.created_at.strftime('%b %d, %Y')
        return 'Recently'

    @property
    def author_name(self):
        """Name of the author."""
        return self.author.username if self.author else 'Unknown Author'

    @property
    def author_role(self):
        """Author designation/role."""
        return 'Verified Author'

    @property
    def avatar(self):
        """Author avatar URL."""
        if self.author:
            return self.author.get_avatar(80)
        return 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=80&auto=format&fit=crop&q=80'

    def __repr__(self):
        return f'<BlogPost {self.title}>'


class ContactMessage(db.Model):
    """
    Model to store contact form inquiries submitted by users.
    Demonstrates Flask-SQLAlchemy setup and database connectivity in Week 1.
    """
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<ContactMessage {self.name} - {self.subject}>'
