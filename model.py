"""Models and database functions for Make Less Mush"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##################################################################
#Model definintions

class User(db.Model):
	"""User of Make Less Mush website"""

	__tablename__ = 'users'

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(64), nullable=False)
	password = db.Column(db.String(64), nullable=False)
	fname = db.Column(db.String(64), nullable=False)
	lname = db.Column(db.String(64), nullable=True)

	def __repr__(self):
		"""A helpful representation of the user"""

		return "<User user_id: %s email: %s>" % (self.user_id, self.email)

class Friendship(db.Model):
	"""Keep track of relationship between users"""

	__tablename__ = 'friendships'

	friendship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user1_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	friends_user_id = db.Column(db.Integer, nullable=False)
	food_shared = db.Column(db.Integer, db.ForeignKey('foods.food_id'), nullable=True)

	user = db.relationship("User",
						    backref=db.backref("friendships", order_by=friendship_id))

	food = db.relationship("Food",
						    backref=db.backref("friendships", order_by=friendship_id))

	def __repr__(self):
		"""A helpful representation of the relationship"""

		return "Friendship between User1_id: %s and User2_id: %s>" % (self.user1_id, 
																	    self.friends_with_user2_id)

class Food(db.Model):
	"""Food shared on Make Less Mush"""

	__tablename__ = 'foods'

	food_id  = db.Column(db.Integer, autoincrement=True, primary_key=True)
	title = db.Column(db.String(64), nullable=False)
	description = db.Column(db.Text, nullable=True)
	#include user_id once loggin is being tracked.

	def __repr__(self):
		"""A helpful representation of the food"""

		return "<Food food_id: %s title: %s>" % (self.food_id, self.title)

	@classmethod
	def add_food(cls, title, description):
		"""Insert a new food listing into the database"""
		food = cls(title=title, description=description)
		print food
		db.session.add(food)
		db.session.commit()

class Message(db.Model):
	"""Messages sent within Make Less Mush"""

	__tablename__ = 'messages'

	message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	sender_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	receiver_user_id = db.Column(db.Integer, nullable=False)
	message_sent = db.Column(db.Text, nullable=False)

	user = db.relationship("User", 
						    backref=db.backref("messages", order_by=message_id))

	def __repr__(self):
		"""A helpful representation of the message"""

		return "Message id: %s User1_id: %s, User2_id>" % (self.message_id, self.user1_id, self.user2_id)
	

################################################################################
#Helper functions

def connect_to_db(app):
	"""Connect the database to the Flask app."""

	#Configure to use our SQLite database
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mush.db'
	db.app = app
	db.init_app(app)

if __name__ == "__main__":
	#If run in interactive mode, this will leave you in a state
	#of being able to work with the database directly.

	from server import app
	connect_to_db(app)
	print "Connected to DB."