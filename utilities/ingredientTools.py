import string, os, requests
from model import UnitConversion, FormattedUnit

spoonacular_key = os.environ['APIKey']


def standardize_unit(original_unit):
    """Standardize unit for comparison"""

    # get rid of extra characters
    translator = str.maketrans('','',string.punctuation)
    unit = original_unit.translate(translator).strip()

    # lowercase unless it is T, t, or c
    if unit.lower != 't':
        unit = unit.lower()
        obj = FormattedUnit.query.filter(FormattedUnit.unit_name==unit).one()
        unit = obj.formatted_name

    return unit


def convert_qty(qty, original_unit):

    std_unit = standardize_unit(original_unit)

    # grab conversion object
    conversion = UnitConversion.query.filter(UnitConversion.base_unit
                                            ==std_unit).one()
    std_unit = conversion.std_unit
    std_qty = float(qty)*conversion.mult_factor
    
    return std_qty, std_unit


def query_ingred_api(ingredients):
    """Query Spoonacular API to parse target ingredient"""

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/parseIngredients"
    headers={"X-RapidAPI-Key": spoonacular_key, "Content-Type": "application/x-www-form-urlencoded"}
    payload={"ingredientList": ingredients,"servings": 1}

    response = requests.post(url, headers=headers, params = payload)
    data = response.json()

    return data


def check_ingred_qty(ingred_dict, min_qty, max_qty, unit):
    """Check whether ingredient lies within bounds"""

    # standardize bounds
    min_std, unit_std = convert_qty(min_qty, unit)
    max_std, unit_std = convert_qty(max_qty, unit)

    # format and standardize recipe qty
    unit = ingred_dict['unitLong']
    qty = ingred_dict['amount']
    converted_qty = convert_qty(qty, unit)

    if converted_qty>min_std and converted_qty<max_qty:
        return True
    else:
        return False
