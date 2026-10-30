from datetime import datetime, timezone
from app import db

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

# NOTE: Week 2 will introduce the User model with password hashing and Flask-Login.
# NOTE: Week 3 will introduce the BlogPost model with categories and CRUD operations.
# NOTE: Week 5 will introduce the Comment model.
