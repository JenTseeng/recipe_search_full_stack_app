import requests, os
from utilities import ingredientTools as itools

edamam_id = os.environ['search_id']
edamam_key = os.environ['search_key']


def get_recipes(query, diet, health, num_recipes, excluded):
    """High level function to get recipes and return digested recipe info"""

    data = call_recipe_api(query, diet, health, num_recipes, excluded)
    recipes = extract_recipes(data)
    
    return recipes


def call_recipe_api(query, diet, health, num_recipes = 5, excluded = None):
    """ Query Recipe API for search terms """

    payload = {'app_id':edamam_id, 'app_key':edamam_key, 'q':query, 
                'from':0, 'to':num_recipes, 'diet':diet, 'health':health,
                'excluded':excluded}    
    url = 'https://api.edamam.com/search'
    
    response = requests.get(url, params=payload)
    data = response.json()

    return data


def extract_recipes(data):
    """Extract recipes from API response of nested dictionaries"""

    recipes = []
    for hit in data['hits']:
        recipe = hit['recipe']
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

        recipes.append(parsed_recipe)

    return recipes


def get_qualifying_recipes(recipes, query, min_amt, max_amt, unit):
    """Search with ingredient limits"""

    qualifying_recipes = []
    
    rel_recipes, ingred_list = get_relevant_recipes_and_ingred(query, recipes)

    # NOTE TO SELF: WILL NEED TO PARSE INGREDIENT LIST AND DIVIDE LOAD BETWEEN
    # (LIST CONTAINS INDIVIDUAL INGREDIENTS)
    # ALSO NEED TO ACCOMODATE INGREDIENT RANGES FROM SEARCH INPUT
    # RESULT WILL NEED
    parsed_ingred_dict = itools.call_ingred_api('\n'.join(ingred_list))
    
    # create set of ingredients within min/max
    qualifying_ingred_set = itools.check_ingred_qty(parsed_ingred_dict, min_amt, 
                                                    max_amt, unit)

    # qualify recipes if ingredient in the qualifying set
    for idx, ingredient in enumerate(ingred_list):
        if ingredient in qualifying_ingred_set:
            qualifying_recipes.append(rel_recipes[idx])

    return qualifying_recipes


def get_relevant_recipes_and_ingred(query, recipes):
    """Extract list of strings with ingredient with limits"""

    relevant_recipes = []
    target_ingreds = []
    for recipe in recipes:
        if query not in ','.join(recipe['ingredients']).lower():
            continue
    
        # extract ingredients that match query
        target_ingred = ''
        for ingredient in recipe['ingredients']:
            if query.lower() in ingredient.lower():
                target_ingred = ingredient
        relevant_recipes.append(recipe)
        target_ingreds.append(target_ingred) # will only take last match from a recipe
            
    return [relevant_recipes, target_ingreds]

