from pprint import pformat
import os, requests

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import *


app = Flask(__name__)
app.search_id = os.environ['search_id']
app.search_key = os.environ['search_key']
# app.ingred_id = os.environ['ingred_id']
# app.ingred_key = os.environ['ingred_key']

app.secret_key = "ABC"

# Jinja to raise errors for undefined vars
app.jinja_env.undefined = StrictUndefined



@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/registration")
def new_user():
    """Show registration form"""

    return render_template("registration.html")


@app.route("/confirm_registration", methods=['POST'])
def add_user():
    """Add new user."""

    email_to_check = request.form.get('email')
    pw = request.form.get('pw')

    # Indicate taken user info if email exists in db
    if User.query.filter(User.email==email_to_check).first():
        flash("User already exists. Please enter a different email or login.")
        return redirect("/registration")

    # add user
    else:
        user = User(email=email_to_check, password=pw)
        db.session.add(user)
        db.session.commit()

        flash("Successfully registered!")
        return redirect("/")


@app.route('/login')
def login():
    """Login page"""
    return render_template("login.html")


@app.route('/check_login', methods = ["POST"])
def check_login():
    """Check credentials"""

    email_to_check = request.form.get('email')
    pw = request.form.get('pw')
    user = User.query.filter(User.email==email_to_check, User.password==pw).first()

    # log in user with valid credentials
    if user:
        session['user_id'] = user.user_id
        flash("You are now logged in!")
        return redirect("/users/{}".format(user.user_id))

    # notice for incorrect credentials
    else:
        flash("Credentials incorrect. Please try again.")
        return redirect("/login") 


@app.route('/users/<user_id>')
def show_user_details(user_id):
    """User detail page"""

    user = User.query.get(int(user_id))
    return render_template("user_info.html", user=user)


@app.route('/logout')
def logout():
    """Logout page"""

    del session['user_id']
    flash("You are now logged out!")
    return redirect("/")


@app.route("/recipe_search")
def show_recipe_search_form():
    """Show recipe search form"""

    return render_template("recipe_search.html")


@app.route("/ingredient_search")
def show_ingred_search_form():
    """Show ingredient search form"""

    return render_template("ingredient_search.html")


@app.route("/standard_results", methods=['GET'])
def find_recipes():
    """Search for recipes with keywords"""

    query = request.args.get('search_field')
    excluded = '' # will draw from user db or session
    num_recipes = 5

    data = query_recipe_api(query, num_recipes, excluded)

    # parse results into digestible format
    recipes = parse_search_results(data['hits'])

    return render_template("search_results.html", data=data, recipes=recipes)


@app.route("/ingredient_results", methods=['GET'])
def find_recipes_with_ingred_limits():
    """Recipe Search with ingredient qty checks"""

    # debugging
    # query will be dictionary with ingredient with min and max?
    # query = 'banana'
    # min_qty = 1

    # TODO: parse query
    # figure out whether there is a min and/or max for each ingred
    # maybe phase 1 will require min and max
    # bounds = determine_bounds(min_qty, max_qty)

    pass
    


######### Helper Functions #########

def query_recipe_api(query, num_recipes = 5, excluded = None):
    """ Query Recipe API for search terms """

    payload = {'app_id':app.search_id, 'app_key':app.search_key, 'q':query, 
                'from':0, 'to':num_recipes, 'excluded':excluded}    
    url = 'https://api.edamam.com/search'
    
    response = requests.get(url, params=payload)
    data = response.json()

    return data



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

def parse_search_results(data):
    """ Parse API returned recipe results and returns list of a dictionaries
    
    Hit has keys of: recipe, bookmarked, and bought
    A recipe keys: label (ie: recipe title), image, url, yield, ingreds, etc.
    An ingredient is a list of dictionaries.  1 dictionary per ingredient
    Each ingredient dictionary has text and weight (few have quantity and measure)

    """
    recipe_results = []

    for hit in data:
        new_entry = {}
        ingredients = []
        recipe = hit['recipe']

        # add relevant info to new_entry
        new_entry['title'] = recipe['label']
        new_entry['image'] = recipe['image']
        new_entry['url'] = recipe['url']

        # extract text from each ingredient and add to new_entry
        for ingredient in recipe['ingredients']:
            ingredients.append(ingredient['text'])        
        new_entry['ingredients'] = ingredients

        recipe_results.append(new_entry)

    return recipe_results


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


def check_API_calls_remaining(response):
    """Check for remainins calls for spoonacular API"""

    pass

# Trials with other APIs
# url= 'https://api.edamam.com/api/nutrition-data'
# payload = {'app_id':app.ingred_id, 'app_key':app.ingred_key,'ingr':'1 cup flour'}
# response = requests.get(url, params=payload)

# response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/", headers={"X-RapidAPI-Key": "0259f0d9e1msha4cc9f28bb5ed5ep1deaf8jsn6ff56d1c04da"})
# response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/jokes/random",headers={"X-RapidAPI-Key": "0259f0d9e1msha4cc9f28bb5ed5ep1deaf8jsn6ff56d1c04da"})
# response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/cuisine",headers={"X-RapidAPI-Key": "0259f0d9e1msha4cc9f28bb5ed5ep1deaf8jsn6ff56d1c04da"})



if __name__ == "__main__":
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")