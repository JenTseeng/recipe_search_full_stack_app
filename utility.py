import requests, pickle
from datetime import datetime
from model import db, DietPreference

def query_recipe_api(app_id, app_key, query, diet, health, num_recipes = 5, excluded = None):
    """ Query Recipe API for search terms """

    payload = {'app_id':app_id, 'app_key':app_key, 'q':query, 
                'from':0, 'to':num_recipes, 'diet':diet, 'health':health,
                'excluded':excluded}    
    url = 'https://api.edamam.com/search'
    
    response = requests.get(url, params=payload)
    data = response.json()

    return data

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
    
    pass

    # recipe_results = []

    # for hit in data:
    #     new_entry = {}
    #     ingredients = []
    #     recipe = hit['recipe']

    #     # add relevant info to new_entry
    #     new_entry['title'] = recipe['label']
    #     new_entry['image'] = recipe['image']
    #     new_entry['url'] = recipe['url']


    #     valid = check_quantity()


    #     # extract text from each ingredient and add to new_entry
    #     for ingredient in recipe['ingredients']:
    #         ingredients.append(ingredient['text'])        
    #     new_entry['ingredients'] = ingredients

    #     recipe_results.append(new_entry)

    # return recipe_results


def standardize_unit():
    """Standardize unit for comparison"""

    pass

def check_quantity(ingredients, query_ingred, unit, condition):
    # starting with 1 thing in query to start
    # query = {ingred: 'flour', min: '2 cups', max = '4 cups'}
    
    pass

    # for ingredient in ingredients:
    #     if ingredient == query_ingred:
    #         ingred_data = spoon.parse_ingredients(ingredient)
    #         num = ingred_data['amount']
    #         unit_short = ingred_data['unitShort']
    #         unit_long = ingred_data['unitLong']
    #         if unit == unit_short or unit == unit_long:
    #             if condition == "min_only":
    #                 # check for min    
    #                 pass

    #             elif condition == "max_only":
    #                 # check for max
    #                 pass

    #             else:
    #                 # check for both
    #                 pass


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


def update_diet_preference(user_id, preferences):
    """Add diet preference of user to table"""

    # delete previous entries
    DietPreference.query.filter_by(user_id=user_id).delete()

    # adding each diet preference to session
    for diet_id in preferences:
        new_preference_entry = DietPreference(user_id = user_id, 
                                                diet_id = diet_id)
        db.session.add(new_preference_entry)

    # committing changes
    db.session.commit()


def get_diet_preferences(user_id):
    """Get diet preferences from db"""

    preferences = DietPreference.query.filter_by(user_id=user_id).all()
    health = None
    diet = None

    for preference in preferences:
        if preference.diet_type.edamam_class == 'Health':
            health = preference.diet_type.diet_name
        else:
            diet = preference.diet_type.diet_name

    return diet, health


def update_API_calls_remaining(header):
    """Update remaining calls for spoonacular API"""

    # extract time and remaining budget from header
    date = datetime.strptime(header['Date'], '%a, %d %b %Y %X %Z').date()
    qty_calls_remaining = header['X-RateLimit-requests-Remaining']
    qty_results_remaining = header['X-RateLimit-results-Remaining']

    # set boolean for whether calls are available
    if qty_calls_remaining > 0 and qty_results_remaining > 0:
        calls_avail_bool = True

    else:
        calls_avail_bool = False

    # write call information to file
    call_info = {"call_update_date":date,"calls_avail_bool":calls_avail_bool, 
                    "qty_calls_remaining":qty_calls_remaining,
                    "qty_results_remaining":qty_results_remaining}
    with open('api_tracker.pickle','wb') as file:
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