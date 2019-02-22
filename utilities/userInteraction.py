from model import db, DietPreference


def set_diet_info(session):
    """"""
    if 'user_id' in session:
        diet, health = get_diet_preferences(session['user_id'])
    else:
        diet = None
        health = None

    return diet, health


def update_diet_preference(user_id, preferences):
    """Add diet preference of user to table"""

    # delete previous entries
    DietPreference.query.filter_by(user_id=user_id).delete()

    # adding each diet preference to session
    for diet_id in preferences:
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