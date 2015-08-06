"""Models and database functions for Make Less Mush"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
	fb_id = db.Column(db.String(64), nullable=True, default=None)

	def __repr__(self):
		"""A helpful representation of the user"""

		return "<User user_id: %s email: %s>" % (self.user_id, self.email)

	@classmethod
	def add_user(cls, email, password, fname, lname, fb_id=None):
		"""Insert a new user into the users table"""
		user = cls(email=email, password=password, fname=fname, lname=lname, fb_id=fb_id)
		db.session.add(user)
		db.session.commit()

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
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	post_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

	user = db.relationship("User", 
						   backref=db.backref("foods", order_by=food_id))

	def __repr__(self):
		"""A helpful representation of the food"""

		return "<Food food_id: %s title: %s>" % (self.food_id, self.title)

	@classmethod
	def add_food(cls, title, description, user_id):
		"""Insert a new food listing into the foods table"""
		food = cls(title=title, description=description, user_id=user_id)
		db.session.add(food)
		db.session.commit()

class Message(db.Model):
	"""Messages sent within Make Less Mush"""

	__tablename__ = 'messages'

	message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	receiver_id = db.Column(db.Integer, nullable=False)
	message_sent = db.Column(db.Text, nullable=False)
	read_status = db.Column(db.Boolean, default=0, nullable=False) #0 = not read.
	datetime_sent = db.Column(db.DateTime, nullable=False, default=datetime.now)

	user = db.relationship("User", 
						    backref=db.backref("messages", order_by=message_id))

	def __repr__(self):
		"""A helpful representation of the message"""

		return "Message id: %s sender_id: %s, receiver_id: %s>" % (self.message_id, self.sender_id, 
															self.receiver_id)

	@classmethod
	def add_message(cls, sender_id, receiver_id, message_sent):
		"""Insert a new message into the messages table"""
		message = cls(sender_id=sender_id, 
					  receiver_id=receiver_id, 
					  message_sent=message_sent)
		db.session.add(message)
		db.session.commit()
	

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
