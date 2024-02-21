"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SECRET_KEY'] = 'abc123'
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.app_context().__enter__()
db.create_all()

@app.route('/')
def home():
    """Home page that will be redirected to show all users"""
    return redirect('/users')

@app.route('/users')
def get_all_users():
    """Page showing all users ordered by their first and last names"""
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('home.html', users=users)

@app.route('/users/new')
def add_new_user():
    """Form to add a new user"""
    return render_template('new.html')

@app.route('/users/new', methods=["POST"])
def add_new_user_form():
    """Handling adding new user form"""
    user_dict = {}
    user_dict['first_name'] = request.form.get('first_name')
    user_dict['last_name'] = request.form.get('last_name')
    if image_url :=request.form.get('image'):
        user_dict['image_url'] = image_url
        
    new_user = User(**user_dict)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Displaying the details of a single user"""
    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id = user_id)
    return render_template('user_detail.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Displaying the form to edit details of an individual user"""
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def submit_edit(user_id):
    """Handling edit form"""
    user = User.query.get(user_id)
    edit_first_name = request.form['first_name']
    edit_last_name = request.form['last_name']
    edit_image_url = request.form['image']
    
    user.first_name = edit_first_name
    user.last_name = edit_last_name
    user.image_url = edit_image_url
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Deleting user and all their posts"""
    post = Post.query.filter(Post.user_id == user_id).delete()
    db.session.commit()
    user = User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/post/new')
def add_post(user_id):
    """Adding new post form"""
    user = User.query.get(user_id)
    return render_template('new_post.html', user = user)

@app.route('/users/<int:user_id>/post/new', methods=['POST'])
def add_post_form(user_id):
    """Handling adding new post by the user"""
    title = request.form['title']
    content = request.form['content']
    user_id = user_id

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    """Page showing post details"""
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post = post)

@app.route('/posts/<int:post_id>/edit')
def edit_form(post_id):
    """Show form to edit a post"""
    post = Post.query.get(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_form_submit(post_id):
    """Handling editing a post"""
    post = Post.query.get(post_id)
    edit_title = request.form['title']
    edit_content = request.form['content']

    post.title = edit_title
    post.content = edit_content
    post.user_id = post.user_id
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deleting post"""
    post = Post.query.filter(Post.id == post_id).delete()
    db.session.commit()
    return redirect('/users') 

