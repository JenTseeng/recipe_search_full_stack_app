"""Models and database functions for recipe project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Technique(db.Model):
    """Cooking Technique"""

    __tablename__ = "techniques"

    technique_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    technique = db.Column(db.String(30))
    
    def __repr__(self):

        return f"<Technique technique_id={self.technique_id} technique={self.technique}>"


class Course(db.Model):
    """Course classification for a recipe"""

    __tablename__ = "courses"

    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course = db.Column(db.String(30))
    
    def __repr__(self):

        return f"<Course course_id={self.course_id} course={self.course}>"


class Timeframe(db.Model):
    """Time required to make recipe"""

    __tablename__ = "timeframes"

    timeframe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    timeframe = db.Column(db.String(30))
    
    def __repr__(self):

        return f"<Timeframe timeframe_id={self.timeframe_id} timeframe={self.timeframe}>"


class Complexity(db.Model):
    """Complexity of recipe"""

    __tablename__ = "complexities"

    complexity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    complexity = db.Column(db.String(20))
    
    def __repr__(self):

        return f"<Complexity level ={self.complexity}>"


# class Ingredient(db.Model):
#     """Ingredients that can be in a recipe"""

#     __tablename__ = "ingredients"

#     ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     ingred_name = db.Column(db.String(30))
    
#     def __repr__(self):

#         return f"<Ingredient_id={self.ingredient_id} name={self.ingred_name}>"


# class Pantry(db.Model):
#     """Pantry linking users of readily available ingredients"""

#     __tablename__ = "pantries"

#     pantry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'))
    
#     def __repr__(self):

#         return f"<Pantry item for user id: {self.user_id}>"


class ExcludedIngredient(db.Model):
    """Preferences of users for an ingredient"""

    __tablename__ = "ingredient_exclusions"

    ingredient_exclusion_id = db.Column(db.Integer, autoincrement=True, 
                                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    ingred_name = db.Column(db.String(60))
    user = db.relationship('User', backref=db.backref('excluded_ingreds'))


    def __repr__(self):

        return f"<Ingredient preference id={self.ingredient_pref_id} for user id {self.user_id}>"


class DietType(db.Model):
    """Dietary Categories"""

    __tablename__ = "diets"

    diet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    diet_name = db.Column(db.String(30))
    edamam_class = db.Column(db.String(16))
    
    def __repr__(self):

        return f"<Diet_id={self.diet_id} diet={self.diet_name}>"


class DietPreference(db.Model):
    """Dietary restrictions/preferences of a user"""

    __tablename__ = "diet_preferences"

    diet_pref_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.diet_id'))
    strictness = db.Column(db.Integer, nullable=True)
    
    diet_type = db.relationship('DietType', backref=db.backref('diet_prefs'))
    user = db.relationship('User', backref=db.backref('diet_prefs'))

    def __repr__(self):

        return f"<Dietary Preference id={self.diet_pref_id} for user id: {self.user_id}>"


class Cuisine(db.Model):
    """Cuisine types"""

    __tablename__ = "cuisines"

    cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cuisine_name = db.Column(db.String(50))
    
    def __repr__(self):

        return f"<Cuisine cuisine_id={self.cuisine_id} name={self.cuisine_name}>"


class CuisinePreference(db.Model):
    """Cuisine preference for user"""

    __tablename__ = "cuisine_preferences"

    cuisine_pref_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisines.cuisine_id'))
    cuisine_rating = db.Column(db.Integer, nullable=True)

    cuisine = db.relationship('Cuisine', backref=db.backref('cuisine_pref'))
    user = db.relationship('User', backref=db.backref('cuisine_pref'))
    
    def __repr__(self):

        return f"<Cuisine preference id={self.cuisine_pref_id} for user id: {self.user_id}>"


class User(db.Model):
    """User of recipe website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    rating = db.relationship("Rating")
    

    def __repr__(self):

        return f"<User user_id={self.user_id} email={self.email}>"


class Rating(db.Model):
    """Rating of recipe website."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

    # Define relationships to user
    user = db.relationship("User")

    def __repr__(self):

        return f"<Rating rating_id={self.rating_id} recipe_id={self.recipe_id}>"


class SavedRecipe(db.Model):
    """Saved recipe"""

    __tablename__ = "saved_recipes"
    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):

        return f"<Saved Recipe record_id={self.record_id}>"


class UnitConversion(db.Model):
    """Table to convert length units"""

    __tablename__ = "unit_conversions"
    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    base_unit = db.Column(db.String(32), nullable=False)
    meas_type = db.Column(db.String(32), nullable=False)
    std_unit = db.Column(db.String(32), nullable=False)
    mult_factor = db.Column(db.Float(5), nullable=False)
    
    def __repr__(self):

        return f"<Unit Conversion base_unit={self.base_unit}>"



class FormattedUnit(db.Model):
    """Table with standard name for units"""

    __tablename__ = "formatted_unit_names"
    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    unit_name = db.Column(db.String(32), nullable=False)
    formatted_name = db.Column(db.String(32), nullable=False)
    meas_type = db.Column(db.String(32), nullable=False)
    
    def __repr__(self):

        return f"<Unit Standard name base_unit={self.base_unit}>"



# class VolumeConversion(db.Model):
#     """Table to convert volumetric units"""

#     __tablename__ = "volume_conversions"
#     record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     base_unit = db.Column(db.String(16), nullable=False)
#     teasoon = db.Column(db.Float(5), nullable=False)
#     tablespoon = db.Column(db.Float(5), nullable=False)
#     fluid_ounce = db.Column(db.Float(5), nullable=False)
#     cup = db.Column(db.Float(5), nullable=False)
#     pint = db.Column(db.Float(5), nullable=False)
#     quart = db.Column(db.Float(5), nullable=False)
#     gallon = db.Column(db.Float(5), nullable=False)
#     milliliter = db.Column(db.Float(5), nullable=False)
#     liter = db.Column(db.Float(5), nullable=False)

#     def __repr__(self):

#         return f"<Volume Conversion base_unit={self.base_unit}>"


# class MassConversion(db.Model):
#     """Table to convert mass units"""

#     __tablename__ = "mass_conversions"
#     record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     base_unit = db.Column(db.String(16), nullable=False)
#     ounce = db.Column(db.Float(5), nullable=False)
#     pound = db.Column(db.Float(5), nullable=False)
#     gram = db.Column(db.Float(5), nullable=False)
    
#     def __repr__(self):

#         return f"<Mass Conversion base_unit={self.base_unit}>"


# class LengthConversion(db.Model):
#     """Table to convert length units"""

#     __tablename__ = "length_conversions"
#     record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     base_unit = db.Column(db.String(32), nullable=False)
#     inches = db.Column(db.Float(5), nullable=False)
#     millimeters = db.Column(db.Float(5), nullable=False)
#     centimeters = db.Column(db.Float(5), nullable=False)
    
#     def __repr__(self):

#         return f"<Length Conversion base_unit={self.base_unit}>"


##############################################################################
# Helper functions

def connect_to_db(app, database='recipes'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' + database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")