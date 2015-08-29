import types
import seed
import datetime
import unittest
import tempfile
import json
import os
import flask
from model import (db, connect_to_db, User, Friendship,
                   Food, Message, Allergen, Location)
from server import app, db, get_new_messages
import seed


class MLMUnitTestCase(unittest.TestCase):
    # Tests that new_messages returns an int type

    def test_get_new_messages(self):
        self.assertIs(type(get_new_messages(1)), types.IntType)


class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_filename = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:////' +
                                                 self.db_filename)
        app.config['TESTING'] = True
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.test_client = app.test_client()
        db.app = app
        db.init_app(app)
        with app.app_context():
            db.create_all()
        seed.load_users()
        seed.load_listings()
        seed.load_messages()

    def login(self, client):
        # submit login info

        return client.post('/login_portal', data=dict(
                email="avanhardenberg@gmail.com",
                password="alyson"
                ), follow_redirects=True)

    def test_login(self):
        # login adds user_id to session

        with app.test_client() as c:
            self.login(c)
            assert flask.session['user_id'] == 1

    def test_database_seed(self):
        # Ensure that the database seed file functions as expected

        user = User.query.get(1)
        food = Food.query.get(1)
        message = Message.query.get(1)
        assert user.email == "avanhardenberg@gmail.com"
        assert food.title == "Peas And Carrots"
        assert message.message_sent == "I would like your mush."

    def test_add_user(self):
        # Ensures that a food object is created in the database
        # when the mush form is submitted

        User.add_user("test@user.com", "test", "test", "test")

        assert User.query.filter_by(email="test@user.com").one()

    def test_add_friendship(self):
        # Ensure function adds friendship to database

        Friendship.add_friendship(1, 2)

        assert Friendship.query.filter_by(admin_id=1, friend_id=2).one()

    def test_add_allergen(self):
        # Ensure function adds allergen to database

        this_allergen = Allergen.add_allergen(['eggs', 'wheat', 'dairy'])
        this_id = this_allergen.allergen_id

        assert Allergen.query.filter_by(allergen_id=this_id).one()

    def test_add_message(self):
        # Ensure function adds message to the database

        Message.add_message(1, 2, "Hello test user")
        assert Message.query.filter_by(message_sent="Hello test user").one()

    def test_no_route(self):
        # test that a user gets a 404 error when trying
        # to access a nonexistant route

        response = self.test_client.get('/thisdoesntexist')
        assert response.status_code == 404

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_filename)

if __name__ == '__main__':
    from server import app
    from model import connect_to_db
    connect_to_db(app)
    unittest.main()
