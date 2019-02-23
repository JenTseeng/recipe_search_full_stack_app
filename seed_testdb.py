"""Utility file to seed recipe database"""

from datetime import datetime
from sqlalchemy import func
from model import connect_to_db, db, DietType, UnitConversion, FormattedUnit, User
from server import app
from seed import load_diets, load_name_conventions, load_unit_conversions


def load_users():
    """Load diets from u.diet into database."""

    print("Test Users Table")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.diet file and insert data
    for row in open("seed_data/u.test_users"):
        row = row.rstrip()
        email, pw = row.split("|")

        user = User(email = email, password = pw)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app, 'test_db')

    # In case tables haven't been created, create them
    db.create_all()
    load_diets()
    load_name_conventions()
    load_unit_conversions()
    load_users()
