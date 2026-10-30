from urllib.parse import urlparse
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle new user account creation.
    If already logged in, redirect to home.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower()
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login via email or username with remember-me support.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.email_or_username.data.strip()
        # Look up by email (lowercased) or by username
        user = User.query.filter(
            (User.email == identifier.lower()) | (User.username == identifier)
        ).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email/username or password. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

        # Log user in
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome back, {user.username}!', 'success')

        # Handle 'next' page redirect securely to avoid open redirect vulnerabilities
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('auth.profile')
        return redirect(next_page)

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Log out the current user and clear the session.
    """
    logout_user()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Display and update current user's profile information.
    Protected by @login_required decorator.
    """
    form = UpdateProfileForm(original_username=current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data.strip()
        current_user.bio = form.bio.data.strip()
        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.bio.data = current_user.bio

    return render_template('profile.html', user=current_user, form=form)
