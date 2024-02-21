"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User

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
    return render_template('user_detail.html', user=user)

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
    """Deleting user"""
    user = User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('/users')

    

