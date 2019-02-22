from datetime import datetime
import pickle


def update_API_calls_remaining(header, file='api_tracker.pickle'):
    """Update remaining calls for spoonacular API"""

    # extract time and remaining budget from header
    date = datetime.strptime(header['Date'], '%a, %d %b %Y %X %Z').date()
    qty_calls_remaining = int(header['X-RateLimit-requests-Remaining'])
    qty_results_remaining = int(header['X-RateLimit-results-Remaining'])

    # set boolean for whether calls are available
    if qty_calls_remaining > 0 and qty_results_remaining > 0:
        calls_avail_bool = True

    else:
        calls_avail_bool = False

    # write call information to file
    call_info = {"call_update_date":date,"calls_avail_bool":calls_avail_bool, 
                    "qty_calls_remaining":qty_calls_remaining,
                    "qty_results_remaining":qty_results_remaining}
    with open(file,'wb') as file:
        pickle.dump(call_info, file)


def check_api_call_budget(infile='api_tracker.pickle', 
                                    outfile='api_tracker.pickle'):
    """Check for remaining API calls before making a call"""

    with open(infile,'rb') as file:
        call_info = pickle.load(file)

    if call_info['calls_avail_bool']==True and call_info['qty_calls_remaining']>0:
        return True

    else:
        now = datetime.utcnow().date()
        if now > call_info['call_update_date']:
            reset_api_call_count(outfile)
            return True
            
        else:
            return False


def reset_api_call_count(filename='api_tracker.pickle'):
    """Reset counters for API"""
    
    CALL_LIMIT = 50
    RESULT_LIMIT = 500

    calls_avail_bool = True
    call_update_date = datetime.utcnow().date()
    qty_results_remaining = RESULT_LIMIT
    qty_calls_remaining = CALL_LIMIT

    call_info = {"call_update_date":call_update_date,"calls_avail_bool":calls_avail_bool, 
                "qty_calls_remaining":qty_calls_remaining,
                "qty_results_remaining":qty_results_remaining}

    file = open(filename, 'wb')
    pickle.dump(call_info, file)
    file.close()