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

@app.route('/login')
def login():
	"""Login page."""

	return render_template("login.html")

@app.route('/login_portal', methods=['POST'])
def login_portal():
	"""Handles the login form"""

	email = request.form.get('email')
	password = request.form.get('password')
	user = User.query.filter_by(email=email, password=password).first()

	if user:
		user_id = user.user_id
		session['user_id'] = user_id
		flash('Login successful!')
		return redirect('/')
	else:
		flash('Login unsuccessful. Please try again')
		return redirect('/login')

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

@app.route('/listings/<int:food_id>')
def food_info(food_id):
    """Display information about a specific food listing"""

    food_listing = Food.query.get(food_id)
    print food_listing

    return render_template('food_info.html', food_listing=food_listing)

###########################

if __name__ == "__main__":
	#Set debug to true to have the toolbar extension run.
	app.debug = True

	connect_to_db(app)

	#Use the debug toolbar.
	DebugToolbarExtension(app)

	app.run()