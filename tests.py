from unittest import TestCase
from flask import session
from server import app, initialize_API_call_count, check_for_API_calls_remaining, update_API_calls_remaining


class FlaskTestsAPICallTracking(TestCase):
    """Test tracking of API calls"""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_login(self):
        """Test user login"""

        pass
    

    def test_logout(self):
        """Test user logout"""

        pass


    def test_registration(self):
        """Test user registration"""

        pass


    def test_existing_user_registration(self):
        """Test existing users cannot register twice"""

        pass


# TODO: write unit tests for pickle checks



if __name__ == "__main__":
    import unittest

    unittest.main()
