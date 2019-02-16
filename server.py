from pprint import pformat

from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from model import *
from utility import *
from flask import Flask, render_template, request, flash, redirect, session

app = Flask(__name__)
app.secret_key = "ABC"

# Jinja to raise errors for undefined vars
app.jinja_env.undefined = StrictUndefined

app.search_id = os.environ['search_id']
app.search_key = os.environ['search_key']
# keys for Edamam nutrition API
# app.ingred_id = os.environ['ingred_id']
# app.ingred_key = os.environ['ingred_key']


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

    # Redirect and request different login in email unavailable
    if User.query.filter(User.email==email_to_check).first():
        flash("User already exists. Please enter a different email or login.")
        return redirect("/registration")

    # add user to db
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

    # alert for incorrect credentials
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
    excluded = '' # will eventually draw from user db (or session)
    num_recipes = 5

    data = query_recipe_api(app.search_id, app.search_key, query, num_recipes, excluded)

    # extract relevant info from API response
    recipes = []
    for hit in data['hits']:
        recipe = hit['recipe']
        parsed_recipe = parse_recipe(recipe)
        recipes.append(parsed_recipe)

    return render_template("search_results.html", recipes=recipes)


@app.route("/ingredient_results", methods=['GET'])
def find_recipes_with_ingred_limits():
    """Recipe Search with ingredient qty checks"""

    # query = request.args.get('search_field')
    query = 'banana'
    excluded = '' # will eventually draw from user db (or session)
    num_recipes = 5

    data = query_recipe_api(app, query, num_recipes, excluded)

    # parse recipes in API results
    recipes = []
    for hit in data['hits']:
        recipe = hit['recipe']
        parsed_recipe = parse_recipe(recipe)
        recipes.append(parsed_recipe)

    return render_template("search_results.html", recipes=recipes)


# @app.route("/check_api_calls")
# def test_api_call_counter():
#     """Debug route"""

#     reset_API_call_count()
#     init_test = check_for_API_calls_remaining()

#     remaining_calls=False
#     call_update_date = datetime.utcnow().date()
#     setting_false = check_for_API_calls_remaining()

#     previous_date = datetime.strptime("14-Feb-2019", "%d-%b-%Y").date()
#     call_update_date = yesterday
#     next_day = check_for_API_calls_remaining()

#     return render_template("calls_debug.html", init = init_test, setting_false = setting_false, next_day=next_day)


######################## Trials with APIs ###########################

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
    