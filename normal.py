from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from models import Blogpost, Comment

normal = Blueprint('normal', __name__)

@normal.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@normal.route('/profile')
@login_required
def profile():
    name = current_user.name
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('profile.html', name = current_user.name, posts=posts)

@normal.route('/post/<int:post_id>')
@login_required
def post(post_id):
    name = current_user.name
    post = Blogpost.query.filter_by(id=post_id).one()
    post_author = post.author
    comments = Comment.query.filter_by(post_author=post_author).all()
    return render_template('post.html', post=post, name=current_user.name, comments=comments)

@normal.route('/public/<int:post_id>')
def public(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('public.html', post=post)

@normal.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post_to_delete = Blogpost.query.get_or_404(post_id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting this post"

@normal.route('/update/<int:post_id>', methods=['POST', 'GET'])
@login_required
def update(post_id):
    name = current_user.name
    post_to_update = Blogpost.query.get_or_404(post_id)
    if request.method == 'POST':
        post_to_update.title = request.form['title']
        post_to_update.subtitle = request.form['subtitle']
        post_to_update.author = request.form['author']
        post_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect(url_for('normal.profile'))
        except:
            return 'There was an issue updating your post.'
    else:
        return render_template('update.html', post=post_to_update, name=current_user.name)

@normal.route('/add')
@login_required
def add():
    name = current_user.name
    return render_template('add.html', name=current_user.name)

@normal.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = current_user.name
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('normal.profile'))

@normal.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    post = Blogpost.query.get_or_404(post_id)
    post_id = post.id
    post_author = post.author
    author = current_user.name
    comment = request.form['comment']
    comment_post = Comment(text=comment, post_author=post_author, author=current_user.name, timestamp=datetime.now())

    try:
        db.session.add(comment_post)
        db.session.commit()
        return redirect(url_for('normal.post', post_id=post_id, comments=comment_post))
    except:
        return "There was an issue placing your comment."

    return render_template('public.html', post=post)


