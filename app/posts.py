from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import BlogPost, Comment
from app.forms import PostForm, CommentForm

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
            tags=form.tags.data.strip() if form.tags.data else '',
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

    comment_form = CommentForm()
    return render_template('post_detail.html', post=post, related_posts=related_posts, comment_form=comment_form)


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
        post.tags = form.tags.data.strip() if form.tags.data else ''
        post.featured_image = form.featured_image.data.strip() if form.featured_image.data else None
        post.content = form.content.data.strip()

        db.session.commit()
        flash('Your article has been updated successfully!', 'success')
        return redirect(url_for('posts.post_detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.category.data = post.category
        form.tags.data = post.tags or ''
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


@posts.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """
    Publish a reader response to a blog post.
    Requires user authentication (@login_required).
    """
    post = BlogPost.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data.strip(),
            author=current_user,
            post=post
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your response has been published successfully!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'danger')

    return redirect(url_for('posts.post_detail', post_id=post.id) + '#comments-section')


@posts.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """
    Delete a comment.
    Authorization: Allowed for the comment author OR the blog post author (moderation).
    """
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post_id

    # Moderation Check: Allowed for comment author OR article author
    if comment.author != current_user and comment.post.author != current_user:
        abort(403)

    db.session.delete(comment)
    db.session.commit()

    flash('The response has been removed.', 'info')
    return redirect(url_for('posts.post_detail', post_id=post_id) + '#comments-section')
