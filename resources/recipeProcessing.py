import requests, os

edamam_id = os.environ['search_id']
edamam_key = os.environ['search_key']

# keys for Edamam nutrition API
# nutrition_id = os.environ['ingred_id']
# nutrition_key = os.environ['ingred_key']


def query_recipe_api(query, diet, health, num_recipes = 5, excluded = None):
    """ Query Recipe API for search terms """

    payload = {'app_id':edamam_id, 'app_key':edamam_key, 'q':query, 
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




