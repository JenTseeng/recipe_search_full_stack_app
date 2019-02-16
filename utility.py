import os, requests, pickle
from datetime import datetime

def parse_recipe(recipe):
    """ Parse API returned recipe results and returns list of a dictionaries
    
    Recipe: label (ie: recipe title), image, url, yield, ingreds, ...
    Each ingredient: text, weight (few have quantity and measure)

    """

    parsed_recipe = {}
    ingredients = []

    # add relevant info to new_entry
    parsed_recipe['title'] = recipe['label']
    parsed_recipe['image'] = recipe['image']
    parsed_recipe['url'] = recipe['url']

    # extract text from each ingredient and add to new_entry
    for ingredient in recipe['ingredients']:
        ingredients.append(ingredient['text'])        
    parsed_recipe['ingredients'] = ingredients

    # return recipe with relevant information
    return parsed_recipe


def parse_search_results_with_ingred_limit(data, query, num_results = 5, min_qty=None, max_qty=None):
    recipe_results = []

    for hit in data:
        new_entry = {}
        ingredients = []
        recipe = hit['recipe']

        # add relevant info to new_entry
        new_entry['title'] = recipe['label']
        new_entry['image'] = recipe['image']
        new_entry['url'] = recipe['url']

        if ingred_check == True:
            check_quantity()


        # extract text from each ingredient and add to new_entry
        for ingredient in recipe['ingredients']:
            ingredients.append(ingredient['text'])        
        new_entry['ingredients'] = ingredients

        recipe_results.append(new_entry)

    return recipe_results


def check_quantity(ingredients, query_ingred, unit, condition):
    # starting with 1 thing in query to start
    # query = {ingred: 'flour', min: '2 cups', max = '4 cups'}
    
    for ingredient in ingredients:
        if ingredient == query_ingred:
            ingred_data = spoon.parse_ingredients(ingredient)
            num = ingred_data['amount']
            unit_short = ingred_data['unitShort']
            unit_long = ingred_data['unitLong']
            if unit == unit_short or unit == unit_long:
                if condition == "min_only":
                    # check for min    
                    pass

                elif condition == "max_only":
                    # check for max
                    pass

                else:
                    # check for both
                    pass




def determine_bounds(min_qty=None, max_qty=None):
    """ Check whether user input min/max """

    if min_qty and max_qty:
        bounds = 'both'
    elif min_qty:
        bounds = 'min_only'
    elif min_qty:
        bounds = 'min_only'
    else:
        bounds = 'skip_qty_check'

    return bounds


def update_API_calls_remaining(header):
    """Update remaining calls for spoonacular API"""

    # extract time and remaining budget from header
    date = datetime.strptime(header['Date'], '%a, %d %b %Y %X %Z').date()
    remaining_calls = header['X-RateLimit-requests-Remaining']
    remaining_results = header['X-RateLimit-results-Remaining']

    # set 'calls_left' variable
    if remaining_calls > 0 and remaining_results > 0:
        calls_left = True

    else:
        calls_left = False

    # write call information to file
    call_info = {"call_update_date":date,"calls_left":calls_left, 
                    "remaining_calls":remaining_calls,
                    "remaining_results":remaining_results}
    with open('call_tracker.data','w') as file:
        pickle.dump(call_info, file)


def check_for_API_calls_remaining():
    """Check for remaining API calls before making a call"""

    with open('call_tracker.data','wb') as file:
        call_info = pickle.load(file)

    if call_info['remaining_calls']==True:
        return True

    else:
        now = datetime.utcnow().date()
        if now > call_info['call_update_date']:
            reset_API_call_count()
            return True
            
        else:
            flash("You've run out of API calls.  Perhaps try a regular recipe search.")
            return False


def reset_API_call_count():
    """Reset counters for API"""
    # file = open(call_tracker.data, 'r')
    # call_info = pickle.load(file)

    CALL_LIMIT = 50
    RESULT_LIMIT = 500

    calls_left = True
    call_update_date = datetime.utcnow().date()
    remaining_results = RESULT_LIMIT
    remaining_calls = CALL_LIMIT

    call_info = {"call_update_date":call_update_date,"calls_left":calls_left, 
                "remaining_calls":remaining_calls,
                "remaining_results":remaining_results}
    with open('call_tracker.data','wb') as file:
        pickle.dump(call_info, file)