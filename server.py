from pprint import pformat
import os

import requests
from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = os.environ['APIKey']


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/recipe-search")
def show_recipe_search_form():
    """Show recipe search form"""

    return render_template("recipe-search.html")


@app.route("/recipes")
def find_recipes():
    """Search for recipes on Spoonacular"""

    query = request.args.get('query')


    payload = {'number':5,'ranking':1,'ingredient':ingredient
                'X-RapidAPI-Key':app.secret_key}
    url = '"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients'
    
    response = requests.get(url, params=payload)

    data = response.json()
    # - (Make sure to save the JSON data from the response to the data
    #   variable so that it can display on the page as well.)

    #data = {'This': ['Some', 'mock', 'JSON']}
    events = []

    return render_template("afterparties.html",
                           data=pformat(data),
                           results=events)

    # # If the required info isn't in the request, redirect to the search form
    # else:
    #     flash("Please provide all the required information!")
    #     return redirect("/afterparty-search")


######### Helper Functions #########
def get_access_token(code):
    """Use access code to request user's access token"""

    # Add your post request here to get an access token
    # Call add_bookmark with your access token and event_id
    pass


def add_bookmark(access_token, event_id):
    """Use user's access token to save bookmark for event"""

    pass


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")