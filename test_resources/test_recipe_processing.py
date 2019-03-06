import unittest
from utilities import recipeTools, ingredientTools

class IngredToolsUnitTests(unittest.TestCase):
    """Test that ingredient Tools work correctly"""

    def test_qty_conversion(self):
        """Test unit conversion"""

        converted, unit = ingredientTools.convert_qty(1, 'QUART')
        assert converted == 192 and unit == 'teaspoon'


    def test_unit_standardization(self):
        """Test unit conversion"""

        unit_to_convert = 'GRAMS'
        converted = ingredientTools.standardize_unit(unit_to_convert)
        assert converted == 'gram'


    # def test_qty_checking(self):
    #     """Test unit conversion"""

    #     ingred_dict = {'unitLong':'pounds', 'amount':10}
    #     result = ingredientTools.check_ingred_qty(ingred_dict, 1, 
    #                                             20, 'pound')
    #     print(result)
    #     assert result == -1


if __name__ == "__main__":

    unittest.main()


