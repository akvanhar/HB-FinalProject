"""Make Less Mush"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from datetime import datetime

from sqlalchemy import desc

from model import connect_to_db, User, Friendship, Food, Message

app = Flask(__name__)

#Required to use Flask sessions and the debug toolbar:
app.secret_key = "abc123"

#Set this in order to raise Jinja errors.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def home():
	"""homepage"""

	recent_listings = Food.query.order_by(desc('post_date')).limit(5).all()

	print recent_listings

	return render_template('index.html', recent_listings=recent_listings)

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

@app.route('/logbutton')
def logbutton():
    """You get here if you click the login/logout button from any page other than login/signup"""
    if 'user_id' in session:
        del session['user_id']
        flash("Logout successful!") 
    return redirect("/login")

@app.route('/signup')
def signup():
	"""Allows a user to signup for Make Less Mush"""

	return render_template('signup.html')

@app.route('/signup_portal', methods=['POST'])
def signup_portal():
	"""Handles the signup form"""

	email = request.form.get('email')
	password = request.form.get('password')
	fname = request.form.get('fname')
	lname = request.form.get('lname')

	User.add_user(email, password, fname, lname)

	#automatically sign in user after account creation
	user = User.query.filter_by(email=email, password=password).first()
	user_id = user.user_id
	session['user_id'] = user_id
	flash('Account successfully created. Welcome to Make Less Mush!')

	return redirect('/')

@app.route('/postlisting', methods=['POST'])
def postlisting():
	"""Handles a new listing being submitted"""

	flash('Your listing has been successfully posted!')

	title = request.form.get('title')
	description = request.form.get('description')
	user_id = session['user_id']

	Food.add_food(title, description, user_id)

	return redirect('/')

@app.route('/listings')
def listings():
	"""Lists all the food listings"""

	foods = Food.query.order_by(desc('post_date')).all()
	
	return render_template('listings.html', foods=foods)

@app.route('/listings/<int:food_id>')
def food_info(food_id):
    """Display information about a specific food listing"""

    food_listing = Food.query.get(food_id)
    print food_listing

    return render_template('food_info.html', food_listing=food_listing)

@app.route('/messages')
def messages():
	"""Displays messages for that specific user"""

	current_user_id = session['user_id']
	current_user = User.query.get(current_user_id)
	user_messages = Message.query.filter_by(receiver_id=current_user_id).all()

	return render_template('messages.html', user_messages=user_messages)

@app.route('/send_message', methods=['POST'])
def send_message():
	"""Handles sending a message to a specific user"""

	message = request.form.get('message')
	current_user_id = session['user_id']
	posting_user = request.form.get('posting_user')

	Message.add_message(current_user_id, posting_user, message)

	flash('Your message has been sent.')

	return redirect('/')

################################################################################

if __name__ == "__main__":
	#Set debug to true to have the toolbar extension run.
	app.debug = True

	connect_to_db(app)

	#Use the debug toolbar.
	# DebugToolbarExtension(app)

	app.run()