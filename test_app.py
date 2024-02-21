from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False


app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""
        Post.query.delete()
        User.query.delete()
        

        user = User(first_name='Anna', last_name='Smith')
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        post = Post(title='First Post', content='My Very first post', user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

        
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
    
    def test_list_users(self):
        """Test the list of all users"""
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Anna', html)

    def test_show_user(self):
        """Test the single user's details"""
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Anna Smith', html)
            self.assertIn('First Post', html)
    
    def test_add_new_user(self):
        """Test adding new user"""
        with app.test_client() as client:
            d = {'first_name': 'John', 'last_name': 'Brown'}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Brown', html)

    def test_delete_user(self):
        """Test deleting user"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Anna Smith', html)
    
    def test_edit_user(self):
        """Test editing user"""
        with app.test_client() as client:
            d = {'first_name': 'Anna', 'last_name': 'Smith Jr', 'image': '/static/default_profile_pic.jpeg'}
            resp = client.post(f'/users/{self.user_id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Anna Smith Jr', html)
    
    def test_add_new_post(self):
        """Testing adding a new post"""
        with app.test_client() as client:
            d = {'title': 'My second post', 'content': 'My second post content'}
            resp = client.post(f'/users/{self.user_id}/post/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('My second post', html)
    
    def test_post_details(self):
        """Testing post details"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('My Very first post', html)
            self.assertIn('First Post', html)
            self.assertIn('Anna Smith', html)
    
    def test_post_delete(self):
        """Testing deleting post"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Anna Smith', html) 

    def test_post_edit(self):
        """Testing editing post"""
        with app.test_client() as client:
            d = {'title': 'My edited post','content': 'Content of edited post'}
            resp = client.post(f'/posts/{self.post_id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('My edited post', html)
            self.assertIn('Content of edited post', html)     

