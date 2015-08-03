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
	user_fname = db.Column(db.String(64), nullable=False)
	user_lname = db.Column(db.String(64), nullable=True)

	def __repr__(self):
		"""A helpful representation of the user"""

		return "<User user_id: %s email: %s>" % (self.user_id, self.email)

class Relationship(db.Model):
	"""Keep track of relationship between users"""

	__tablename__ = 'relationships'

	relationship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)