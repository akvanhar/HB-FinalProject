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
	password = db.Column(db.String(64), nullable=True)
	fname = db.Column(db.String(64), nullable=False)
	lname = db.Column(db.String(64), nullable=True)
	fb_id = db.Column(db.String(64), nullable=True, default=None)

	def __repr__(self):
		"""A helpful representation of the user"""

		return "<User user_id: %s email: %s>" % (self.user_id, self.email)

	@classmethod
	def add_user(cls, email, fname, lname, password=None, fb_id=None):
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
	texture = db.Column(db.String(64), nullable=True)
	datemade = db.Column(db.DateTime, nullable=True)
	quantity = db.Column(db.Integer, nullable=True)
	freshfrozen = db.Column(db.String(64), nullable=True)
	description = db.Column(db.Text, nullable=True)
	allergen_id = db.Column(db.Integer, db.ForeignKey('allergens.allergen_id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	post_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
	active = db.Column(db.Boolean, nullable=False, default=1) #1 indicates that the item is active

	allergen = db.relationship("Allergen",
								backref=db.backref("foods", order_by=food_id))
	user = db.relationship("User", 
						   backref=db.backref("foods", order_by=food_id))

	def __repr__(self):
		"""A helpful representation of the food"""

		return "<Food food_id: %s title: %s>" % (self.food_id, self.title)

		# title, texture, datemade, quantity, freshfrozen, description, allergens, user_id

	@classmethod
	def add_food(cls, title, texture, datemade, quantity,
				 freshfrozen, description, allergen_id, user_id):
		"""Insert a new food listing into the foods table"""

		datemade = datetime.strptime(datemade, "%Y-%m-%d")

		food = cls(title=title, texture=texture, 
				   datemade=datemade, quantity=quantity, 
				   freshfrozen=freshfrozen, description=description, 
				   allergen_id=allergen_id, user_id=user_id)
		db.session.add(food)
		db.session.commit()

	def update_food(self, food_id, title, texture, datemade, quantity,
				 freshfrozen, description, active=1):
		"""updates a listing in the foods table"""

		datemade = datetime.strptime(datemade, "%Y-%m-%d")

		this_food = Food.query.get(food_id)
		this_food.title = title
		this_food.texture = texture
		this_food.datemade = datemade
		this_food.quantity = quantity
		this_food.freshfrozen = freshfrozen
		this_food.description = description
		this_food.active = active

		db.session.commit()

class Allergen(db.Model):
	"""Allergens for a specific food listing. All are boolean values. 0 is not present."""

	__tablename__ = 'allergens'

	allergen_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	eggs = db.Column(db.Boolean, default=0, nullable=False)
	dairy = db.Column(db.Boolean, default=0, nullable=False)
	wheat = db.Column(db.Boolean, default=0, nullable=False)
	peanuts = db.Column(db.Boolean, default=0, nullable=False)
	treenuts = db.Column(db.Boolean, default=0, nullable=False)
	soy = db.Column(db.Boolean, default=0, nullable=False)
	fish = db.Column(db.Boolean, default=0, nullable=False)
	shellfish = db.Column(db.Boolean, default=0, nullable=False)

	def __repr__(self):
		"""A helpful representation of the Allergens"""

		return "<Allergens allergen_id: %s" % (self.allergen_id)

	@classmethod
	def add_allergen(cls, allergen_list):
		"""Takes a list of specified allergens, inserts a new allergen listing 
			into the allergens table, returns an allergens obejct"""
		if "eggs" in allergen_list:
				eggs = 1
		else:
			eggs = 0
		if "dairy" in allergen_list:
				dairy = 1
		else:
			dairy = 0
		if "wheat" in allergen_list:
				wheat = 1
		else:
			wheat = 0
		if "peanuts" in allergen_list:
				peanuts = 1
		else:
			peanuts = 0
		if "soy" in allergen_list:
				soy = 1
		else:
			soy = 0
		if "treenuts" in allergen_list:
				treenuts = 1
		else:
			treenuts = 0
		if "fish" in allergen_list:
				fish = 1
		else:
			fish = 0
		if "shellfish" in allergen_list:
				shellfish = 1
		else:
			shellfish = 0

		allergen = cls(eggs=eggs,
					   dairy=dairy,
					   wheat=wheat,
					   peanuts=peanuts,
					   treenuts=treenuts,
					   soy=soy,
					   fish=fish,
					   shellfish=shellfish)
		db.session.add(allergen)
		db.session.commit()

		return allergen

	def update_allergen(self, allergen_id, allergen_list):
		"""updates an allergen"""
		if "eggs" in allergen_list:
			eggs = 1
		else:
			eggs = 0
		if "dairy" in allergen_list:
			dairy = 1
		else:
			dairy = 0
		if "wheat" in allergen_list:
			wheat = 1
		else:
			wheat = 0
		if "peanuts" in allergen_list:
			peanuts = 1
		else:
			peanuts = 0
		if "soy" in allergen_list:
			soy = 1
		else:
			soy = 0
		if "treenuts" in allergen_list:
			treenuts = 1
		else:
			treenuts = 0
		if "fish" in allergen_list:
			fish = 1
		else:
			fish = 0
		if "shellfish" in allergen_list:
			shellfish = 1
		else:
			shellfish = 0

		this_allergen = Allergen.query.get(allergen_id)
		this_allergen.eggs = eggs
		this_allergen.dairy = dairy
		this_allergen.wheat = wheat
		this_allergen.peanuts = peanuts
		this_allergen.soy = soy
		this_allergen.treenuts = treenuts
		this_allergen.fish = fish
		this_allergen.shellfish = shellfish

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

	# create all tables on running this file.
	db.create_all()
