"""Make Less Mush"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, User, Friendship, Food, Message

app = Flask(__name__)

#Required to use Flask sessions and the debug toolbar:
app.secret_key = "abc123"

#Set this in order to raise Jinja errors.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def home():
	"""homepage"""

	return render_template('index.html')

@app.route('/postlisting', methods=['POST'])
def postlisting():
	"""Handles a new listing being submitted"""

	flash('Your listing has been successfully posted!')

	title = request.form.get('title')
	description = request.form.get('description')

	Food.add_food(title, description)

	return redirect('/')

@app.route('/listings')
def listings():
	"""Lists all the food listings"""

	foods = Food.query.all()

	return render_template('listings.html', foods=foods)

###########################

if __name__ == "__main__":
	#Set debug to true to have the toolbar extension run.
	app.debug = True

	connect_to_db(app)

	#Use the debug toolbar.
	DebugToolbarExtension(app)

	app.run()