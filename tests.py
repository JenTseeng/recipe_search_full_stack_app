import unittest, pickle
from datetime import datetime
from flask import session
from server import app
from model import *
from utilities import recipeTools, requestTracking, ingredientTools, userInteraction

class FlaskTestsWithoutLogin(unittest.TestCase):
    """Test Operations Not Requiring Logged In User"""

    def setUp(self):
        """Setup before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        
        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        # connect_to_db(app, 'test_db')

        def _mock_query_recipe_api(query, diet, health, num_recipes, 
                                    excluded=None):
            """Mock function to circumvent API"""

            file = open('test_resources/static_edamam_data.pickle', 'rb')
            fake_data = pickle.load(file)
            file.close()

            return fake_data


        # circumvent API request w/ mock functions
        recipeTools.query_recipe_api = _mock_query_recipe_api

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


    # def test_user_registration(self):
    #     """Test basic edamame recipe search without querying API"""

    #     result = self.client.post("/confirm_registration", data={
    #                                 'email':'blue@blue.com', 'pw':'hello'}, 
    #                                 follow_redirects = True)

    #     self.assertIn(b'User already exists', result.data)


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

        with app.app_context():
            db.init_app(app)
    

    def test_logout(self):
        """Test user logout"""

        result = self.client.get("/logout", follow_redirects = True)
        self.assertIn(b'You are now logged out', result.data)


    def test_get_diets(self):
        """Test user diet info retrieval"""

        diet, health = userInteraction.get_diet_preferences(1)
        
        assert diet == 'balanced' and health == 'vegan'


    def test_diet_addition(self):
        """Test addition of diet to user profile"""

        result = self.client.post("/update_diet", data={'diets':[1,5]},
                                    follow_redirects = True)

        self.assertIn(b'Diet preferences updated', result.data)


class RequestTrackingUnitTests(unittest.TestCase):
    """Test tracking of Spoonacular API calls"""

    def test_allow_api_call(self):
        """Test that API call allowed when API call limits not exhausted"""
        assert requestTracking.check_api_call_budget('test_resources/api_limits_reset.pickle',
                                    'test_resources/dummy.pickle')==True


    def test_refresh_api_call(self):
        """Test that daily API call count reset on next day"""
        assert requestTracking.check_api_call_budget(
                                        'test_resources/new_day_check.pickle',
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

        assert requestTracking.check_api_call_budget(
                                    'test_resources/no_calls_remaining.pickle',
                                    'test_resources/dummy.pickle')==False


    def test_update_tracker(self):
        """Test that call count is updated"""
        
        # load test header response
        filename = 'test_resources/header_response.pickle'
        test_outfile = 'test_resources/dummy_update.pickle'

        test_header_file = open(filename, 'rb')
        header = pickle.load(test_header_file)
        test_header_file.close()

        # update header date
        now = datetime.utcnow()
        new_date = now.strftime('%a, %d %b %Y %X')+' GMT'
        header['Date'] = new_date

        requestTracking.update_API_calls_remaining(header, test_outfile)==True
        
        with open(test_outfile, 'rb') as result:
            call_info = pickle.load(result)

        # check that file was updated
        assert call_info['call_update_date'] == now.date()


class IngredToolsUnitTests(unittest.TestCase):
    """Test that ingredient Tools work correctly"""

    def test_qty_conversion(self):
        """Test unit conversion"""

        converted, unit = ingredientTools.convert_qty(1, 'QUART')
        assert converted == 4 and unit == 'cup'


    def test_unit_standardization(self):
        """Test unit conversion"""

        unit_to_convert = 'GRAMS'
        converted = ingredientTools.standardize_unit(unit_to_convert)
        assert converted == 'gram'


    # def test_qty_checking(self):
    #     """Test unit conversion"""

    #     ingred_dict = {'unitLong':'pounds', 'amount':10}
    #     result = ingredientTools.check_ingred_qty(ingred_dict, 1, 
    #                                             20, 'pound')
    #     print(result)
    #     assert result == -1


if __name__ == "__main__":

    unittest.main()


