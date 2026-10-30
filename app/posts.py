from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import BlogPost
from app.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """
    Create a new blog post.
    Requires user authentication (@login_required).
    """
    form = PostForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            category=form.category.data,
            featured_image=form.featured_image.data.strip() if form.featured_image.data else None,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()

        flash('Your article has been published successfully!', 'success')
        return redirect(url_for('posts.post_detail', post_id=post.id))

    return render_template('create_post.html', form=form, title='Write a Story')


@posts.route('/post/<int:post_id>')
def post_detail(post_id):
    """
    View an individual blog post by ID.
    Accessible to all visitors.
    """
    post = BlogPost.query.get_or_404(post_id)
    # Fetch related articles from same category for reading recommendation
    related_posts = BlogPost.query.filter(
        BlogPost.category == post.category,
        BlogPost.id != post.id
    ).order_by(BlogPost.created_at.desc()).limit(3).all()

    return render_template('post_detail.html', post=post, related_posts=related_posts)


@posts.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """
    Edit an existing blog post.
    Strictly restricted to the author of the post.
    """
    post = BlogPost.query.get_or_404(post_id)

    # Authorization Check: Only post author can edit
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.category = form.category.data
        post.featured_image = form.featured_image.data.strip() if form.featured_image.data else None
        post.content = form.content.data.strip()

        db.session.commit()
        flash('Your article has been updated successfully!', 'success')
        return redirect(url_for('posts.post_detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.category.data = post.category
        form.featured_image.data = post.featured_image or ''
        form.content.data = post.content
        form.submit.label.text = 'Update Story'

    return render_template('edit_post.html', form=form, post=post, title='Edit Story')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """
    Delete a blog post.
    Strictly restricted to the author of the post.
    """
    post = BlogPost.query.get_or_404(post_id)

    # Authorization Check: Only post author can delete
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash('Your article has been deleted successfully.', 'info')
    return redirect(url_for('main.index'))
