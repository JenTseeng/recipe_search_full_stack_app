import unittest
from flask import session
from server import app
from model import connect_to_db, db
from utilities import userInteraction


class TestDatabaseInteractions(unittest.TestCase):
    """Test tracking of API calls"""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        connect_to_db(app, 'test_db')

        # Key for sessions access
        app.config['SECRET_KEY'] = 'ABC'
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        with app.app_context():
            db.init_app(app)


    def test_get_diets(self):
        """Test user diet info retrieval"""

        diet, health = userInteraction.get_diet_preferences(1)
        
        assert diet == 'balanced' and health == 'vegan'


    def test_diet_addition(self):
        """Test addition of diet to user profile"""

        result = self.client.post("/update_diet", data={'diet':1, 'health':5},
                                    follow_redirects = True)

        self.assertIn(b'updated', result.data)