import pickle, unittest
from utilities import requestTracking
from datetime import datetime


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


if __name__ == "__main__":

    unittest.main()