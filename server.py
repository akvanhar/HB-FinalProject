"""Make Less Mush"""
import os
import json

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from datetime import datetime

from sqlalchemy import desc

from model import db, connect_to_db, User, Friendship, Food, Message, Allergen

from titlecase import titlecase

app = Flask(__name__)

#Required to use Flask sessions and the debug toolbar:
app.secret_key = os.environ['FLASK_SECRET_KEY']

#Set this in order to raise Jinja errors.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def home():
	"""homepage"""
	if 'user_id' in session:
		user_id = session['user_id']

		user = User.query.get(user_id)
		user_friends = user.friendships

	if user_friends:
		friend_ids = [friend.friend_id for friend in user_friends] #get this user's friend ids

		#get all their friend's listings
		friends_listings = Food.query.filter_by(active=1).filter(Food.user_id.in_(friend_ids)).order_by(desc('post_date')).all() 

		#get the food ids so they can be filtered out
		friends_food_ids = [food.food_id for food in friends_listings]

		#get all the other active listings
		other_listings = Food.query.filter_by(active=1).filter(~Food.food_id.in_(friends_food_ids)).order_by(desc('post_date')).all()

		#combine listings so that the friends listings come first
		this_users_listings = friends_listings + other_listings
		short_list = this_users_listings[:5]

	else:
		short_list = Food.query.filter_by(active=1).order_by(desc('post_date')).limit(5).all()

	current_date = datetime.now()
	current_date = current_date.strftime("%Y-%m-%d")
	print current_date

	return render_template('index.html', user_listings=short_list, current_date = current_date)

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

	print 'user: ', user

	if user:
		user_id = user.user_id
		session['user_id'] = user_id
		flash('Login successful!')
		return redirect('/')
	else:
		flash('Login unsuccessful. Please try again')
		return redirect('/login')

@app.route('/facebook_login_portal', methods=['POST'])
def facebook_login():
	"""Handles the login from the facebook login button)"""
	
	fb_user_id = request.form.get('fbUserId')
	fb_fname = request.form.get('fbFname')
	fb_lname = request.form.get('fbLname')
	fb_email = request.form.get('fbEmail')
	current_acces_token = request.form.get('accessToken')
	fb_friends = json.loads(request.form.get('fbFriends'))
	print "fb_friends_list: ", fb_friends

	fb_user = User.query.filter_by(fb_id=fb_user_id).first()


	if fb_user:
		# User has previously logged into MLM
		user_id = fb_user.user_id
		session['user_id'] = user_id
		session['current_acces_token'] = current_acces_token

		#check friends list in friends table. If friendship not there, add it.
		if fb_friends:
			friends_user_ids = []
			#turn the fb_ids into user_ids.
			for friend_fb_id in fb_friends:
				friend_user_id = db.session.query(User.user_id).filter_by(fb_id=friend_fb_id).first()
				friends_user_ids.append(friend_user_id)
			friends_user_ids = [x[0] for x in friends_user_ids]

			#now see if those friends are in the friendship table.
			for friend in friends_user_ids:
				friend_exists = db.session.query(Friendship.friend_id).filter_by(friend_id=friend).first()
				#if they're not, add them in! Yay friendship!
				if friend_exists is None:
					Friendship.add_friendship(user_id, friend)

		flash('Login successful!')

		return redirect('/')
	else:
		# First time for user logging into MLM
		# add the user to the database
		User.add_user(email=fb_email, fname=fb_fname, lname=fb_lname, fb_id=fb_user_id)
		#access that user's information, add it to the session
		fb_user = User.query.filter_by(fb_id=fb_user_id).first()
		user_id = fb_user.user_id
		
		session['user_id'] = user_id
		session['current_acces_token'] = current_acces_token
		
		flash('Thanks for creating an account with Make Less Mush')
		
		return redirect('/')

@app.route('/logbutton')
def logbutton():
    """You get here if you click the login/logout button from any page other than login/signup"""
    
    if 'user_id' in session:
        del session['user_id']
        flash("Logout successful!")
    if 'current_acces_token' in session:
    	del session['current_acces_token']
    	flash("You have logged out of Facebook")
     
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
	fname = titlecase(fname)
	lname = request.form.get('lname')
	lname = titlecase(lname)

	User.add_user(email, fname, lname, password)

	#automatically sign in user after account creation
	user = User.query.filter_by(email=email, password=password).first()
	user_id = user.user_id
	session['user_id'] = user_id
	flash('Account successfully created. Welcome to Make Less Mush!')

	return redirect('/')

@app.route('/fblogout_portal')
def logout_portal():
	"""Handles logout of MLM"""
	# FIXTHIS

	return redirect('/login')

@app.route('/postlisting', methods=['POST'])
def postlisting():
	"""Handles a new listing being submitted"""

	if 'user_id' not in session:
		#users who are not logged in cannot post a new listing
		flash('Please login to post a Make Less Mush listing')
		return redirect('/login')
	else:
		title = request.form.get('title')
		title = titlecase(title)
		texture = request.form.get('texture')
		datemade = request.form.get('datemade')
		quantity = request.form.get('quantity')
		freshfrozen = request.form.get('freshfrozen')
		description = request.form.get('description')
		allergens = request.form.getlist('allergens')
		user_id = session['user_id']

		allergen = Allergen.add_allergen(allergens)
		allergen_id = allergen.allergen_id

		Food.add_food(title, texture, datemade, quantity, freshfrozen, description, allergen_id, user_id)

		flash('Your listing has been successfully posted!')

		return redirect('/')

@app.route('/listings')
def listings():
	"""Lists all the food listings, putting the user's friends' listings first"""

	if 'user_id' not in session:
		#users who are not logged in cannot view complete list of listings
		flash('Please login to view the complete list of Make Less Mush listings.')
		return redirect('/login')
	else:
		user_id = session['user_id']

		user = User.query.get(user_id)
		user_friends = user.friendships

		if user_friends:
			friend_ids = [friend.friend_id for friend in user_friends] #get this user's friend ids

			#get all their friend's listings
			friends_listings = Food.query.filter_by(active=1).filter(Food.user_id.in_(friend_ids)).order_by(desc('post_date')).all() 

			#get the food ids so they can be filtered out
			friends_food_ids = [food.food_id for food in friends_listings]

			#get all the other active listings
			other_listings = Food.query.filter_by(active=1).filter(~Food.food_id.in_(friends_food_ids)).order_by(desc('post_date')).all()

			#combine listings so that the friends listings come first
			foods = friends_listings + other_listings

		else:
			foods = Food.query.filter_by(active=1).order_by(desc('post_date')).all()

		return render_template('listings.html', foods=foods)

@app.route('/listings/<int:food_id>')
def food_info(food_id):
    """Display information about a specific food listing"""

    if 'user_id' not in session:
    	#users who are not logged in cannot view listings details
    	flash('Please login to view the details of that particular listing')
    	return redirect('/login')
    else:
    	#get specific listing from db.
    	food_listing = Food.query.get(food_id)

    	return render_template('food_info.html', food_listing=food_listing)

@app.route('/mylistings')
def user_listings():
	"""Shows a list of all of that particular user's listings"""

	if 'user_id' not in session:
		#users who are not logged in cannot view their own listings
		flash('Please login to view your listings')
		return redirect('/login')
	else:
		#show user's listings.
		user_id = session['user_id']
		user_listings = Food.query.filter_by(user_id=user_id).order_by(desc('post_date')).all()
		user = User.query.get(user_id)

		return render_template('mylistings.html', user_listings=user_listings, user=user)

@app.route('/listings/edit/<int:food_id>')
def edit_food(food_id):
	"""Display information about a specific food listing and allows the user to edit it."""

	if 'user_id' not in session:
		#user must be logged in to edit listings
		flash('Please login to edit your listings')
		return redirect('/login')
	else:
		#show user listing and allow them to make changes.
		food_listing = Food.query.get(food_id)

		return render_template('editfood.html', food_listing=food_listing)

@app.route('/updatelisting', methods=['POST'])
def update_listing():
	"""Update an existing listing in the database"""

	if 'user_id' not in session:
		#users who are not logged in cannot post a new listing
		flash('Please login to update a Make Less Mush listing')
		return redirect('/login')
	else:
		title = request.form.get('title')
		title = titlecase(title)
		texture = request.form.get('texture')
		datemade = request.form.get('datemade')
		quantity = request.form.get('quantity')
		freshfrozen = request.form.get('freshfrozen')
		description = request.form.get('description')
		allergen_list = request.form.getlist('allergens')
		user_id = session['user_id']
		food_id = request.form.get('food_id')
		deactivate = request.form.get('deactivate')
		allergen_id = request.form.get('allergen_id')

		if deactivate:
			active = 0
		else:
			active = 1

		this_allergen = Allergen.query.get(allergen_id)
		this_allergen.update_allergen(allergen_id, allergen_list)

		this_food = Food.query.get(food_id)
		this_food.update_food(food_id, title, texture, datemade, quantity,
				 freshfrozen, description, active)
	
		flash('Your listing has been successfully updated!')

	return redirect('/mylistings')

@app.route('/messages')
def messages():
	"""Displays messages for that specific user"""

	if 'user_id' not in session:
		#users who are not logged in cannot view their messages.
		flash('Please login to view your messages.')
		return redirect('/login')
	else:
		#Get the messages for that particular user.
		current_user_id = session['user_id']
		user_messages = Message.query.filter_by(receiver_id=current_user_id)
		user_messages_by_date = user_messages.order_by(desc('datetime_sent'))
		user_messages_by_status = user_messages.order_by('read_status').all()

		return render_template('messages.html', user_messages=user_messages_by_status)

@app.route('/send_message', methods=['POST'])
def send_message():
	"""Handles sending a message to a specific user"""

	if 'user_id' not in session:
		#users who are not logged in cannot send messages.
		flash('Please login to send a message.')
		return redirect('/login')
	else:
		#create a message field in the db.
		message = request.form.get('message')
		current_user_id = session['user_id']
		posting_user = request.form.get('posting_user')

		Message.add_message(current_user_id, posting_user, message)

		flash('Your message has been sent.')

		return redirect('/')

@app.route('/change-read-status', methods=['POST'])
def change_read_status():
	"""change read status of a message"""
	#FIXTHIS

	return 'Hi Alyson'

################################################################################

if __name__ == "__main__":
	#Set debug to true to have the toolbar extension run.
	app.debug = True

	connect_to_db(app)

	#Use the debug toolbar.
	# DebugToolbarExtension(app)

	app.run()