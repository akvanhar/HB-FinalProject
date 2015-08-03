"""Make Less Mush"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

#Required to use Flask sessions and the debug toolbar:
app.secret_key = "abc123"

#Set this in order to raise Jinja errors.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def home():
	"""homepage"""

	return render_template('home.html')

###########################

if __name__ == "__main__":
	#Set debug to true to have the toolbar extension run.
	app.debug = true

	connect_to_db(app)

	#Use the debug toolbar.
	DebugToolbarExtension(app)

	app.run