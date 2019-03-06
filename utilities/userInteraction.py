from model import db, DietPreference, ExcludedIngredient


def set_food_preferences(session):
    """Setting saved diet and ingredient exclusions for registered users"""
    if 'user_id' in session:
        diet, health = get_diet_preferences(session['user_id'])
        exclusion_list = get_ingred_exclusions(session['user_id'])
    else:
        diet = None
        health = None
        exclusion_list = None

    return diet, health, exclusion_list


def update_diet_preference(user_id, preferences):
    """Add diet preference of user to table"""

    # delete previous entries
    DietPreference.query.filter_by(user_id=user_id).delete()

    # adding each diet preference to session
    for diet_id in preferences:
        if diet_id != None:
            new_preference_entry = DietPreference(user_id = user_id, 
                                                diet_id = diet_id)
            db.session.add(new_preference_entry)

    # committing changes
    db.session.commit()


def get_diet_preferences(user_id):
    """Get diet preferences from db"""

    preferences = DietPreference.query.filter_by(user_id=user_id).all()
    health = None
    diet = None

    for preference in preferences:
        if preference.diet_type.edamam_class == 'Health':
            health = preference.diet_type.diet_name
        else:
            diet = preference.diet_type.diet_name

    return diet, health


def update_ingredient_exclusions(user_id, updates):
    """Add ingredients to exclude to database"""

    # deleting all preferences to start
    # TO DO: delete single ingredient functionality on user page
    ExcludedIngredient.query.filter_by(user_id=user_id).delete()

    # adding each ingredient to session
    exclusion_list = updates.split(',')
    for exclusion in exclusion_list:
        if exclusion != '':
            exclusion.strip()
            new_exclusion_entry = ExcludedIngredient(user_id = user_id, 
                                                    ingred_name = exclusion)
            db.session.add(new_exclusion_entry)

    # committing changes
    db.session.commit()

    return None


def get_ingred_exclusions(user_id):
    """Get diet preferences from db"""

    exclusions = ExcludedIngredient.query.filter_by(user_id=user_id).all()
    if exclusions:
        exclusion_list = []
        for exclusion in exclusions:
            exclusion_list.append(exclusion.ingred_name)

        return exclusion_list
    else:
        return None