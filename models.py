from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(200))
    password = db.Column(db.String(200))

class Blogpost(db.Model):
    __bind_key__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(100))
    author = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    comment = db.Column(db.Text)

class Comment(db.Model):
    __bind_key__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    author = db.Column(db.String(100))
    post_author = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
