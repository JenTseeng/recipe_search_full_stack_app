from pprint import pformat
import os

import requests
from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

import spoonacular as sp


app = Flask(__name__)
app.search_id = os.environ['search_id']
app.search_key = os.environ['search_key']
# app.ingred_id = os.environ['ingred_id']
# app.ingred_key = os.environ['ingred_key']
spoon = sp.API(os.environ['APIKey'])

app.secret_key = "ABC"

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/recipe-search")
def show_recipe_search_form():
    """Show recipe search form"""

    return render_template("recipe-search.html")


@app.route("/recipes", methods=['GET'])
def find_recipes():
    """Search for recipes on Spoonacular"""
   
    # debugging
    query = 'banana'
    min_qty = 1

    # getting data from form
    # query = request.args.get('search_field')
    
    excluded = ''
    num_recipes = 20
    payload = {'app_id':app.search_id, 'app_key':app.search_key, 
    'q':query, 'from':0, 'to':num_recipes, 'excluded':excluded}    
    url = 'https://api.edamam.com/search'
    
    response = requests.get(url, params=payload)
    data = response.json()

    recipes = parse_search_results(data['hits'])
    filtered_recipes = filter_recipe(recipes, query, min_qty, 5)
    
    return render_template("search_results.html", data=data, recipes=recipes)


# url= 'https://api.edamam.com/api/nutrition-data'
# payload = {'app_id':app.ingred_id, 'app_key':app.ingred_key,'ingr':'1%20large%20apple'}
# response = requests.get(url, params=payload)

######### Helper Functions #########
def parse_search_results(data):
    """ Parse API returned recipe results and return a list of dictionaries

    Edamam returns results as a list of hits
    Each hit has a recipe, bookmarked, and bought
    Each recipe has: label (ie: recipe title), image, url, yield, ingreds, etc.
    Each ingredient is a list of dictionaries.  1 dictionary per ingredient
    Each ingredient dictionary has text and weight (few have quantity and measure)

    """
    recipe_results = []
    for hit in data:
        new_entry = {}
        ingredients = []
        recipe = hit['recipe']
        new_entry['title'] = recipe['label']
        new_entry['image'] = recipe['image']

        # Pull out text from each ingredient entry
        for ingredient in recipe['ingredients']:
            ingredients.append(ingredient['text'])        
        new_entry['ingredients'] = ingredients

        recipe_results.append(new_entry)

    return recipe_results


def filter_recipes(recipes, query, min_qty, numResults):
    count = 0
    returned_recipes = []
    for recipe in recipes:
        for ingredient in recipe['ingredients']:
            if query in ingredient:
                response = spoon.parse_ingredients(ingredient, servings=1)
                if # quantity is within bound
                    returned_recipes.append(recipe)
                    count += 1
                    if count == numResults:
                        break




if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")