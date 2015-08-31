from flask import session, flash

from model import (db,
                   connect_to_db,
                   User,
                   Friendship,
                   Food,
                   Message,
                   Allergen,
                   Location)
from sqlalchemy import desc


def get_user():
    # Preps new_messages count, user object, and session for base.html.

    user_id = session['user_id']
    user = User.query.get(user_id)

    return user


def get_new_messages(user_id):
    # gets a new_message count from db

    new_messages = Message.query.filter_by(receiver_id=user_id,
                                           read_status=0).count()
    return new_messages


def check_login(message):
    # Checks if the user is logged in, redirects to home page
    # displays an error message if not.

    if not session.get('user_id'):
        flash(message)
        return "not_logged_in"
    else:
        return "logged_in"


def get_messages(user_id, read_status):
    # Takes the desired read status and user_id 
    # returns a list of messages of that status

    messages = Message.query.filter_by(receiver_id=user_id, read_status=read_status)
    messages = messages.order_by(desc('datetime_sent')).all()

    return messages