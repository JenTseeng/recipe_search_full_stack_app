# Waste Not, Want Noms

![Homepage](/static/img/docs/homepage.png)

Waste Not, Want Noms is a web application aimed at helping home cooks find delicious recipes that use up available ingredients.  Users can input up to 3 ingredients and specify minimum and maximum quantities.  Waste Not, Want Noms will then gather recipes that satisfy those requirements.  Registered users can save dietary preferences as well as choose ingredients to omit from all recipes results.

## Table of Contents
* [Technologies](#technologies)
* [How to use Waste Not, Want Noms](#use)
* [Setup Instructions](#setup)
* [Credits](#credits)

## <a name="technologies"></a>Technologies
* Python
* Javascript/jQuery
* Flask
* SQLAlchemy Object Relational Mapper
* Python unittest and datetime modules
* CSS + Bootstrap
* AJAX/JSON
* HTML/CSS
* Jinja2
* Edamam API
* Spoonacular API
* Bcrypt

(Install requirements in requirements.txt)

## <a name="use"></a>How to use Waste Not, Want Noms

### Ingredient Search

![Ingredient Search](/static/img/README/ingredient_search.png)

Users can include up to 3 ingredients with quantity limits.  Results shown to 
the user will be those that best match the user's requirements.

### Profile

![Profile](/static/img/README/user_profile.png)

Users can save diet and ingredient preferences in their profile.  These preferences
will be automatically be applied to the recipe search results.

## <a name="use"></a>Local Installation and Running the Application

* Set up and activate a python virtualenv, then install all dependencies:
    * `pip3 install -r requirements.txt`
  
* Create the tables in your database:
    * `python -i model.py`
    * While in interactive mode, create tables: `db.create_all()`
    * Seed data into database: `python seed.py`
    
* Exit interactive mode. Start up the flask server:
    * `python server.py`

* Go to localhost:5000 to see the web app

## <a name="credits"></a>Credits
* Credits to [Edamam's API](https://developer.edamam.com/) for providing recipe information
* Credits to [Spoonacular's API](https://spoonacular.com/) for providing parsing recipe strings
