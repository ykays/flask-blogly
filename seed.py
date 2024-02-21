from models import User, db, Post
from app import app

#Create all tables
db.drop_all()
db.create_all()

#If table isn't empty, empty it
User.query.delete()

# Add new users

anna = User(first_name='Anna', last_name='Smith')
mike = User(first_name='Mike', last_name='Brown')
kevin = User(first_name='Kevin', last_name='Blue')

# Add new objects to the session
db.session.add(anna)
db.session.add(mike)
db.session.add(kevin)

# Commit changes
db.session.commit()

p1 = Post(title='First Post', content='My Very first post', user_id=1)
p2 = Post(title='Second Post', content='My second post, hopefully better than the first one', user_id=1)
p3 = Post(title='Outdoors', content='Like running, hiking, biking, skiing', user_id=2)
p4 = Post(title='Mountains', content='These are the best mountains in the world', user_id=3)

db.session.add_all([p1, p2, p3, p4])
db.session.commit()