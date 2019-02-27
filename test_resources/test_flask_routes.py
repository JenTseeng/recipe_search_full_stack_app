import unittest, pickle
from server import app
from utilities import recipeTools, ingredientTools
from model import connect_to_db

class FlaskTestsWithoutLogin(unittest.TestCase):
    """Test Operations Not Requiring Logged In User"""

    def setUp(self):
        """Setup before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        
        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        connect_to_db(app, 'test_db')

        def _mock_call_recipe_api(query, diet, health, num_recipes, 
                                    excluded=None):
            """Mock function to circumvent API"""

            file = open('test_resources/static_edamam_data.pickle', 'rb')
            fake_data = pickle.load(file)
            file.close()

            return fake_data

        def _mock_call_ingred_api(ingredients):
            file = open('test_resources/static_parsed_ingredients.pickle', 'rb')
            fake_data = pickle.load(file)
            file.close()            


        # circumvent API request w/ mock functions
        recipeTools.call_recipe_api = _mock_call_recipe_api
        ingredientTools.call_ingred_api = _mock_call_ingred_api

    # def tearDown(self):
    #     """Tear down for recipes"""


    def test_existing_user_registration(self):
        """Test existing users cannot register twice"""

        result = self.client.post("/confirm_registration", data={
                                    'email':'ann@ann.com', 'pw':'hello'}, 
                                    follow_redirects = True)

        self.assertIn(b'User already exists', result.data)


    def test_incorrect_credentials(self):
        """Test existing users cannot register twice"""

        result = self.client.post("/check_login", data={
                                    'email':'ann@ann.com', 'pw':'wrongpw'}, 
                                    follow_redirects = True)

        self.assertIn(b'Credentials incorrect', result.data)


    def test_login(self):
        """Test user login"""

        result = self.client.post("/check_login", data={'email':'ann@ann.com', 
                                    'pw':'hello'}, follow_redirects = True)
        self.assertIn(b'Welcome to your user page!!', result.data)


    def test_basic_recipe_search(self):
        """Test basic edamame recipe search without querying API"""

        result = self.client.get("/standard_results", 
                                    data={'search_field':'test'}, 
                                    follow_redirects = True)
        self.assertIn(b'Almond Flour Muffins', result.data)


    def test_ingredient_search(self):
        """Test recipe search ingredient limits"""

        result = self.client.get("/ingredient_results", 
                                    data={'search_field':'almond flour', 
                                    'min_qty':'1','max_qty':'2', 
                                    'unit':'cup'}, 
                                    follow_redirects = True)
        self.assertIn(b'Almond Flour Fudge Brownies', result.data)
        self.assertNotIn(b'Almond-Flour Crab Cakes With Lemon Aioli', result.data)


class FlaskTestsWithLogin(unittest.TestCase):
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


    def test_logout(self):
        """Test user logout"""

        result = self.client.get("/logout", follow_redirects = True)
        self.assertIn(b'You are now logged out', result.data)



if __name__ == "__main__":

    unittest.main()