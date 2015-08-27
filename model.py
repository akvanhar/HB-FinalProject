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
	admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

	user = db.relationship("User",
							primaryjoin="User.user_id == Friendship.admin_id",
						    backref=db.backref("friendships", order_by=friendship_id))

	def __repr__(self):
		"""A helpful representation of the relationship"""

		return "Friendship between admin_id: %s and friend_id: %s>" % (self.admin_id, self.friend_id)

	@classmethod
	def add_friendship(cls, admin_id, friend_id):
		"""Insert a new friendship into the friendships table"""
		friendship = cls(admin_id=admin_id, friend_id=friend_id)
		db.session.add(friendship)
		db.session.commit()

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
	shared_with = db.Column(db.String, nullable=False)
	phone_number = db.Column(db.String, nullable=True)
	location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=True)

	allergen = db.relationship("Allergen",
								backref=db.backref("foods", order_by=food_id))

	user = db.relationship("User", 
						   backref=db.backref("foods", order_by=food_id))

	location = db.relationship("Location", 
						   backref=db.backref("foods", order_by=food_id))

	def __repr__(self):
		"""A helpful representation of the food"""

		return "<Food food_id: %s title: %s>" % (self.food_id, self.title)

	@classmethod
	def add_food(cls, title, texture, datemade, quantity,
				 freshfrozen, description, allergen_id, user_id, phone_number, location, shared_with=""):
		"""Insert a new food listing into the foods table"""

		datemade = datetime.strptime(datemade, "%Y-%m-%d")

		food = cls(title=title, texture=texture, 
				   datemade=datemade, quantity=quantity, 
				   freshfrozen=freshfrozen, description=description, 
				   allergen_id=allergen_id, user_id=user_id, 
				   phone_number=phone_number, location=location, shared_with=shared_with)

		db.session.add(food)
		db.session.commit()

	def update_food(self, food_id, title, texture, datemade, quantity,
				 freshfrozen, description, active, shared_with):
		"""updates a listing in the foods table"""

		datemade = datetime.strptime(datemade, "%Y-%m-%d")

		this_food = Food.query.get(food_id)
		this_food.title = title
		this_food.texture = texture
		this_food.datemade = datemade
		if this_food.quantity:
			this_food.quantity = int(quantity)
		this_food.freshfrozen = freshfrozen
		this_food.description = description
		this_food.active = active
		this_food.shared_with = shared_with

		db.session.commit()

	def share_food(self, food_id, user_id, friend_id):
		"""adds a friendship reference to the food table"""

		this_food = Food.query.get(food_id)

		this_friendship = Friendship.query.filter_by(admin_id=user_id, friend_id=friend_id).first()
		this_friendship_id = this_friendship.friendship_id

		this_food.shared_with = this_friendship_id
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

		return "<Allergens allergen_id: %s>" % (self.allergen_id)

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

	def delete_message(self):
		"""deletes a message from the messages table"""

		db.session.delete(self)
		db.session.commit()

	def toggle_read(self):
		if self.read_status == 0:
			self.read_status = 1
		else:
			self.read_status = 0

		db.session.commit()

class Location(db.Model):
	"""Locations where food listings where posted from"""

	__tablename__ = 'locations'

	location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	latitude = db.Column(db.Integer, nullable=False)
	longitude = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		"""A helpful representation of the location"""

		return "<location: latitude: %s longitude: %s>" % (self.latitude, self.longitude)

	@classmethod
	def add_location(cls, lat, lng):
		"""Insert a new location into the locations table"""
		location = cls(latitude=lat, 
					  longitude=lng)
		db.session.add(location)
		db.session.commit()

		return location

	def update_location(self, lat, lng):
		"""update a location"""

		self.lat = lat
		self.lng = lng
		db.session.commit()

	def test_no_route(self):
		"""test that a user gets a 404 error when trying to access a nonexistant route."""

		response = self.test_client.get('/thisdoesntexist')
		assert response.status_code == 404

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(self.db_filename)

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
