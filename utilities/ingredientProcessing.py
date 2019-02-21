import string, os, requests
from model import UnitConversion

spoonacular_key = os.environ['APIKey']

def standardize_unit(original_unit):
    """Standardize unit for comparison"""

    # get rid of extra characters
    translator = str.maketrans('','',string.punctuation)
    unit = original_unit.translate(translator).strip()

    # lowercase unless it is T, t, or c
    if unit.lower != 't':
        unit = unit.lower()

    return unit


def convert_qty(min_qty, max_qty, original_unit):

    unit = standardize_unit(original_unit)

    # grab conversion object
    conversion = UnitConversion.query.filter(UnitConversion.base_unit==unit).one()
    std_unit = conversion.std_unit
    std_min = min_qty*conversion.mult_factor
    std_max = max_qty*conversion.mult_factor
    
    return std_min, std_max, std_unit


def query_ingredient_api(ingredients):
    """Query Spoonacular API to parse target ingredient"""

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/parseIngredients"
    headers={"X-RapidAPI-Key": spoonacular_key, "Content-Type": "application/x-www-form-urlencoded"}
    payload={"ingredientList": ingredients,"servings": 1}

    response = requests.post(url, headers=headers, params = payload)
    data = response.json()

    return data


# def determine_bounds(min_qty=None, max_qty=None):
#     """ Check whether user input min/max """

#     if min_qty and max_qty:
#         bounds = 'both'
#     elif min_qty:
#         bounds = 'min_only'
#     elif min_qty:
#         bounds = 'min_only'
#     else:
#         bounds = 'skip_qty_check'

#     return bounds
