import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from app.models import User

class RegistrationForm(FlaskForm):
    """
    User registration form with strict input validation,
    email format validation, and duplicate account prevention.
    """
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=64, message="Username must be between 3 and 64 characters."),
        Regexp('^[A-Za-z0-9_.]+$', message="Username can only contain letters, numbers, dots, and underscores.")
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message="Email address is required."),
        Email(message="Please enter a valid email address."),
        Length(max=120, message="Email must not exceed 120 characters.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=6, max=128, message="Password must be at least 6 characters long.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        """Ensure username is unique."""
        user = User.query.filter_by(username=username.data.strip()).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        """Ensure email is unique."""
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user:
            raise ValidationError('An account with this email already exists. Please log in instead.')


class LoginForm(FlaskForm):
    """
    User login form supporting login via email or username.
    """
    email_or_username = StringField('Email or Username', validators=[
        DataRequired(message="Please enter your email or username.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Please enter your password.")
    ])
    remember_me = BooleanField('Keep me signed in')
    submit = SubmitField('Sign In')


class UpdateProfileForm(FlaskForm):
    """
    Form for updating user profile information.
    """
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=64, message="Username must be between 3 and 64 characters."),
        Regexp('^[A-Za-z0-9_.]+$', message="Username can only contain letters, numbers, dots, and underscores.")
    ])
    bio = TextAreaField('About You / Bio', validators=[
        Length(max=300, message="Bio must not exceed 300 characters.")
    ])
    submit = SubmitField('Save Changes')

    def __init__(self, original_username, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """Prevent changing to a username that is already taken by another user."""
        if username.data.strip() != self.original_username:
            user = User.query.filter_by(username=username.data.strip()).first()
            if user:
                raise ValidationError('This username is already in use by another author.')
