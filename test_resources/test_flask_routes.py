import unittest, pickle
from server import app
from utilities import recipeTools, ingredientTools
from model import connect_to_db, User

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

            return fake_data            


        # circumvent API request w/ mock functions
        recipeTools.call_recipe_api = _mock_call_recipe_api
        ingredientTools.call_ingred_api = _mock_call_ingred_api


    def test_user_registration(self):
        """Test existing users cannot register twice"""

        email = 'sara@sara.com'
        # delete user in db if exists
        User.query.filter(User.email==email).delete()
        result = self.client.post("/confirm_registration", data={
                                    'email':email, 'pw':'hello'}, 
                                    follow_redirects = True)

        self.assertIn(b'Successfully registered!', result.data)


    def test_existing_user_registration(self):
        """Test existing users cannot register twice"""

        result = self.client.post("/confirm_registration", data={
                                    'email':'sara@sara.com', 'pw':'hello'}, 
                                    follow_redirects = True)

        self.assertIn(b'User already exists', result.data)
        

    def test_incorrect_credentials(self):
        """Test existing users cannot register twice"""

        result = self.client.post("/check_login", data={
                                    'email':'sara@sara.com', 'pw':'wrongpw'}, 
                                    follow_redirects = True)

        self.assertIn(b'Credentials incorrect', result.data)


    def test_login(self):
        """Test user login"""

        result = self.client.post("/check_login", data={'email':'sara@sara.com', 
                                    'pw':'hello'}, follow_redirects = True)
        self.assertIn(b'Welcome to your user page!!', result.data)


    def test_basic_recipe_search(self):
        """Test basic edamame recipe search without querying API"""

        result = self.client.get("/standard_results", 
                                    query_string={'search_field':'test'}, 
                                    follow_redirects = True)
        self.assertIn(b'Almond Flour Muffins', result.data)


    def test_ingredient_search(self):
        """Test recipe search ingredient limits"""

        result = self.client.get("/ingredient_results", 
                                    query_string={'search_field':'almond flour', 
                                    'min_qty':'0.25','max_qty':'2', 
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