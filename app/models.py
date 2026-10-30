import hashlib
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

    # NOTE: Week 3 will attach the relationship to BlogPost:
    # posts = db.relationship('BlogPost', backref='author', lazy='dynamic', cascade='all, delete-orphan')

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

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login user loader callback.
    Loads user from database by ID for active session management.
    """
    return User.query.get(int(user_id))


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
