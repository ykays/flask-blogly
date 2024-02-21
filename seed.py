from models import User, db
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