"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import connect_to_db, User, Friendship, Food, Message, Allergen
from server import app
from datetime import datetime


def load_users():
    """Load users from sampleusers into database."""

    user_file = open('sampledata/sampleusers')
    
    for line in user_file:
        email, password, fname, lname, fbid = line.split("|")
        User.add_user(email, fname, lname, password, fbid)

def load_listings():
    """Load listings from samplelistings into database"""

    listings_file = open('sampledata/samplelistings')

    for line in listings_file:
        title, texture, datemade, quantity, freshfrozen, description, allergen_list, user_id = line.split("|")
        allergen = Allergen.add_allergen(allergen_list)
        Food.add_food(title, texture, datemade, quantity,
                 freshfrozen, description, allergen.allergen_id, user_id)
        
if __name__ == "__main__":
    connect_to_db(app)

    # load_users()
    load_listings()
