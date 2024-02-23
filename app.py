"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post, Tag, PostTag

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
    recent_posts = Post.query.order_by(Post.created_at.desc()).all()
    
    return render_template('home.html', recent_posts = recent_posts)

@app.route('/users')
def get_all_users():
    """Page showing all users ordered by their first and last names"""
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('users.html', users=users)

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
    user = User.query.filter(User.id == user_id).one()
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/post/new')
def add_post(user_id):
    """Adding new post form"""
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user = user, tags=tags)

@app.route('/users/<int:user_id>/post/new', methods=['POST'])
def add_post_form(user_id):
    """Handling adding new post by the user"""
    title = request.form['title']
    content = request.form['content']
    user_id = user_id
    tags = request.form.getlist('tag')
    
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    post_id = new_post.id

    for tag in tags:
        new_tag_posts = PostTag(tag_id=int(tag) , post_id=post_id)
        db.session.add(new_tag_posts)
        db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    """Page showing post details"""
    post = Post.query.get(post_id)
    tags = post.tags
    return render_template('post_detail.html', post = post, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def edit_form(post_id):
    """Show form to edit a post"""
    post = Post.query.get(post_id)
    checked_tags = post.tags
    all_tags = Tag.query.all()
    return render_template('edit_post.html', post=post, checked_tags=checked_tags, all_tags=all_tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_form_submit(post_id):
    """Handling editing a post"""
    post = Post.query.get(post_id)
    edit_title = request.form['title']
    edit_content = request.form['content']
    tags = request.form.getlist('tag')
 
    post.title = edit_title
    post.content = edit_content
    post.user_id = post.user_id
    db.session.add(post)
    db.session.commit()

    existing_tags = PostTag.query.filter_by(post_id = post_id).all()
    for existing_tag in existing_tags:
        db.session.delete(existing_tag)
        db.session.commit()
    for tag in tags:
        new_tag_posts = PostTag(tag_id=int(tag) , post_id=post_id)
        db.session.add(new_tag_posts)
        db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deleting post"""
    post = Post.query.filter(Post.id == post_id).one()
    db.session.delete(post)
    db.session.commit()
    return redirect('/users') 

@app.route('/tags')
def show_all_tags():
    """Show all available tags"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show details of an individual tag"""
    tag = Tag.query.get(tag_id)
    posts = tag.posts 
    return render_template('tags_details.html', tag=tag, posts = posts)

@app.route('/tags/new')
def add_new_tag():
    """Form to add a new tag"""
    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def submit_new_tag():
    """Handling adding a new tag"""
    name = request.form['tag']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect ('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Showing form to edit a tag"""
    tag = Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def submit_edit_tag(tag_id):
    """Handling editing tag"""
    tag = Tag.query.get(tag_id)
    edit_name = request.form['tag']
    tag.name = edit_name
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Deleting tag"""
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
