"""Utility file to seed recipe database"""

from datetime import datetime
from sqlalchemy import func
from model import DietType

from model import connect_to_db, db
from server import app


def load_diets():
    """Load diets from u.diet into database."""

    print("Diets")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    DietType.query.delete()

    # Read u.diet file and insert data
    for row in open("seed_data/u.diet"):
        row = row.rstrip()
        diet_id, diet, classification = row.split("|")

        diet = DietType(diet_id=diet_id,
                    diet=diet,
                    edamam_classification=classification)


        # We need to add to the session or it won't ever be stored
        db.session.add(diet)

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()
