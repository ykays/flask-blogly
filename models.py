"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False, default='/static/default_profile_pic.jpeg')

    @property
    def full_name(self):
        return self.first_name +" "+self.last_name
    
class Post(db.Model):

    __tablename__= 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id') )

    user = db.relationship('User', backref=backref('posts', cascade="all, delete-orphan"))
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')

class Tag(db.Model):

    __tablename__= 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

class PostTag(db.Model):

    __tablename__= 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True )
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True)