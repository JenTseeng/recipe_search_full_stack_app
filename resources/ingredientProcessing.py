from model import VolumeConversion, MassConversion, LengthConversion, UnitCrosswalk
import string

def standardize_unit(original_unit):
    """Standardize unit for comparison"""

    # get rid of extra characters
    translator = str.maketrans('','',string.punctuation)
    unit = original_unit.translate(translator).strip()

    # lowercase unless it is T, t, or c
    if unit.lower != 't':
        unit.lower()

    return unit


def convert_qty(qty, original_unit):

    unit = standardize_unit(original_unit)

    # grab object with standard name and correct table
    crosswalk = UnitCrosswalk.query.filter(UnitCrosswalk.unit_name==unit)
    if crosswalk.measurement_type == 'volume':
        conversion = VolumeConversion.query.filter(VolumeConversion.base_unit==
                                                crosswalk.std_name).one()
    elif crosswalk.measurement_type == 'length':
        conversion = LengthConversion.query.filter(LengthConversion.base_unit==
                                                crosswalk.std_name).one()
    else:
        conversion = MassConversion.query.filter(MassConversion.base_unit==
                                                crosswalk.std_name).one()

    converted_qty = qty*conversion.standard

    return None

def check_quantity(ingredients, query_ingred, unit, condition):
    # starting with 1 thing in query to start
    # query = {ingred: 'flour', min: '2 cups', max = '4 cups'}
    
    pass

    # for ingredient in ingredients:
    #     if ingredient == query_ingred:
    #         ingred_data = spoon.parse_ingredients(ingredient)
    #         num = ingred_data['amount']
    #         unit_short = ingred_data['unitShort']
    #         unit_long = ingred_data['unitLong']
    #         if unit == unit_short or unit == unit_long:
    #             if condition == "min_only":
    #                 # check for min    
    #                 pass

    #             elif condition == "max_only":
    #                 # check for max
    #                 pass

    #             else:
    #                 # check for both
    #                 pass


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
