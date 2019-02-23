import requests, os
from utilities import ingredientTools

edamam_id = os.environ['search_id']
edamam_key = os.environ['search_key']


# keys for Edamam nutrition API
# nutrition_id = os.environ['ingred_id']
# nutrition_key = os.environ['ingred_key']

def get_recipes(query, diet, health, num_recipes, excluded):
    """High level function to get recipes and return digested recipe info"""

    data = query_recipe_api(query, diet, health, num_recipes, excluded)
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


def get_recipes_within_range(query, min_amt, max_amt, unit, diet, health, 
                                excluded=None):
    """Search with ingredient limits"""

    qualifying_recipes = []
    num_recipes = 2

    recipes = get_recipes(query, diet, health, num_recipes, excluded)
    rel_recipes, ingred_list = get_relevant_recipes_and_ingred(query, recipes)
    parsed_ingredients = ingredientTools.query_ingred_api(ingred_list)

    # note assuming each recipe only has target ingredient listed once
    for idx, recipe in enumerate(rel_recipes):
        qualify = ingredientTools.check_ingred_qty(parsed_ingredients[idx],
                                                    min_amt, max_amt, unit)
        if qualify:
            qualifying_recipes.append(recipe)
        else:
            continue

    return qualifying_recipes


def get_relevant_recipes_and_ingred(query, recipes):
    """Extract list of strings with ingredient with limits"""
    relevant_recipes = []
    target_ingreds = []
    for recipe in recipes:
        if query.lower() not in ','.join(recipe['ingredients']).lower():
            continue
        else:
            target_ingred = ''
            for ingredient in recipe['ingredients']:
                if query.lower() in ingredient.lower():
                    target_ingred = ingredient
            relevant_recipes.append(recipe)
            target_ingreds.append(target_ingred) # will only take last match from a recipe
        
    return [relevant_recipes, '\n'.join(target_ingreds)]

