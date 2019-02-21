import requests, os
from resources import ingredientProcessing

edamam_id = os.environ['search_id']
edamam_key = os.environ['search_key']


# keys for Edamam nutrition API
# nutrition_id = os.environ['ingred_id']
# nutrition_key = os.environ['ingred_key']

def get_recipes(query, diet, health, num_recipes, excluded):
    """High level function to get recipes and return digested recipe info"""

    data = query_recipe_api(query, diet, health, num_recipes, 
                                            excluded)
    recipes = extract_recipes(data)
    
    return recipes


def query_recipe_api(query, diet, health, num_recipes = 5, excluded = None):
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


def get_recipes_with_ingred_limit(query, min_amt, max_amt, unit, diet, health, 
                                excluded=None):
    """Search with ingredient limits"""

    num_recipes = 10
    min_std, max_std, unit_std = recipeProcessing.convert_qty(min_amt, 
                                                                  max_amt, unit)
    recipes = get_recipes(query, diet, health, num_recipes, excluded)
    ingred_string = extract_target_ingredient(query, recipes)
    response = ingredientProcessing.check_quantity(ingred_string)

    return ingred_string


def extract_target_ingredient(query, recipes):
    """Extract list of strings with ingredient with limits"""

    target_ingreds = []
    for recipe in recipes:
        target_ingred = ''
        for ingredient in recipe['ingredients']:
            if query in ingredient:
                target_ingred = ingredient 
        target_ingreds.append(target_ingred) # will only take last match from a recipe

    return '\n'.join(target_ingreds)

