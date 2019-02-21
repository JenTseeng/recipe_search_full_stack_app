import unittest, pickle
from datetime import datetime
from flask import session
from server import app
from model import *
from resources import recipeProcessing, requestTracking, ingredientProcessing

class FlaskTestsWithoutLogin(unittest.TestCase):
    """Test Operations Not Requiring Logged In User"""

    def setUp(self):
        """Setup before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        
        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        connect_to_db(app)

        def _mock_query_recipe_api(query, diet, health, num_recipes, 
                                    excluded=None):
            """Mock function to circumvent API"""

            file = open('test_resources/fake_data.pickle', 'rb')
            fake_data = pickle.load(file)
            file.close()

            return fake_data


        # circumvent API request w/ mock function
        recipeProcessing.query_recipe_api = _mock_query_recipe_api


    def test_existing_user_registration(self):
        """Test existing users cannot register twice"""

        result = self.client.post("/confirm_registration", data={
                                    'email':'bob@bob.com', 'pw':'hello'}, 
                                    follow_redirects = True)

        self.assertIn(b'User already exists', result.data)


    def test_login(self):
        """Test user login"""

        result = self.client.post("/check_login", data={'email':'bob@bob.com', 
                                    'pw':'hello'}, follow_redirects = True)
        self.assertIn(b'Welcome to your user page!!', result.data)


    def test_basic_recipe_search(self):
        """Test basic edamame recipe search without querying API"""

        result = self.client.get("/standard_results", 
                                    data={'search_field':'test'}, 
                                    follow_redirects = True)
        self.assertIn(b'Smoked Turkey', result.data)


class FlaskTestsWithLogin(unittest.TestCase):
    """Test tracking of API calls"""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Key for sessions access
        app.config['SECRET_KEY'] = 'ABC'
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
    

    def test_logout(self):
        """Test user logout"""

        result = self.client.get("/logout", follow_redirects = True)
        self.assertIn(b'You are now logged out', result.data)


class RequestTrackingUnitTests(unittest.TestCase):
    """Test tracking of Spoonacular API calls"""

    def test_allow_api_call(self):
        """Test that API call allowed when API call limits not exhausted"""
        assert requestTracking.check_api_call_budget('test_resources/api_limits_reset.pickle',
                                    'test_resources/dummy.pickle')==True


    def test_refresh_api_call(self):
        """Test that daily API call count reset on next day"""
        assert requestTracking.check_api_call_budget('test_resources/new_day_check.pickle',
                                    'test_resources/dummy.pickle')==True


    def test_prevent_excess_api_calls(self):
        """Test that API call not allowed when API call limit reached"""
        
        # create fake file with no calls remaining today
        today = datetime.utcnow().date()
        call_info = {"call_update_date":today,"calls_avail_bool":False, 
                    "qty_calls_remaining":0, "qty_results_remaining":0}
        
        file = open('test_resources/no_calls_remaining.pickle','wb')
        pickle.dump(call_info,file)
        file.close()

        assert requestTracking.check_api_call_budget('test_resources/no_calls_remaining.pickle',
                                    'test_resources/dummy.pickle')==False


class IngredProcessingUnitTests(unittest.TestCase):
    """Test that ingredient processing works correctly"""

    def test_qty_conversion(self):
        """Test unit conversion"""

        input_min = 0.5
        input_max = 1
        unit_to_convert = 'quart'

        minim, maxim, unit = ingredientProcessing.convert_qty(input_min,
                                                            input_max,
                                                            unit_to_convert)
        assert minim == 2 and  maxim == 4 and unit == 'cup'


    def test_unit_conversion(self):
        """Test unit conversion"""

        unit_to_convert = 'TBS'

        converted = ingredientProcessing.standardize_unit(unit_to_convert)

        assert converted == 'tbs'


    def test_unit_comparison(self):
        """Test unit comparison"""
        
        pass


if __name__ == "__main__":

    unittest.main()


