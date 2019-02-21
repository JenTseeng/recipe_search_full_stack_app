"""Utility file to seed recipe database"""

from datetime import datetime
from sqlalchemy import func
from model import connect_to_db, db, DietType, UnitConversion, FormattedUnit
from server import app


def load_diets():
    """Load diets from u.diet into database."""

    print("Diets")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    DietType.query.delete()

    # Read u.diet file and insert data
    for row in open("seed_data/u.diets"):
        row = row.rstrip()
        diet_id, diet_name, classification = row.split("|")

        diet = DietType(diet_id=diet_id,
                    diet_name=diet_name,
                    edamam_class=classification)


        # We need to add to the session or it won't ever be stored
        db.session.add(diet)

    # Once we're done, we should commit our work
    db.session.commit()



# def load_volume_units():
#     """Load diets from u.diet into database."""

#     print("Volume Conversion Table")

#     # Delete all rows in existing table to start fresh
#     VolumeConversion.query.delete()

#     # Read u.volume_units file and insert data
#     for row in open("seed_data/u.volume_units"):
#         row = row.rstrip()
#         base_unit, teasoon, tablespoon, fluid_ounce, cup, pint, quart, gallon, milliliter, liter= row.split("|")

#         unit = VolumeConversion(base_unit=base_unit, teasoon=teasoon, 
#                         tablespoon=tablespoon, fluid_ounce=fluid_ounce,
#                         cup=cup, pint=pint, quart=quart, gallon=gallon,
#                         milliliter=milliliter, liter=liter)


#         # We need to add to the session or it won't ever be stored
#         db.session.add(unit)

#     # Once we're done, we should commit our work
#     db.session.commit()


# def load_mass_units():
#     """Load diets from u.diet into database."""

#     print("Mass Conversion Table")

#     # Delete all rows in existing table to start fresh
#     MassConversion.query.delete()

#     # Read u.volume_units file and insert data
#     for row in open("seed_data/u.mass_units"):
#         row = row.rstrip()
#         base_unit, ounce, pound, gram = row.split("|")

#         unit = MassConversion(base_unit=base_unit, ounce=ounce, 
#                                 pound=pound, gram=gram)


#         # We need to add to the session or it won't ever be stored
#         db.session.add(unit)

#     # Once we're done, we should commit our work
#     db.session.commit()


# def load_length_units():
#     """Load diets from u.diet into database."""

#     print("Length Conversion Table")

#     # Delete all rows in existing table to start fresh
#     LengthConversion.query.delete()

#     # Read u.volume_units file and insert data
#     for row in open("seed_data/u.length_units"):
#         row = row.rstrip()
#         base_unit, inches, millimeters, centimeters = row.split("|")

#         unit = LengthConversion(base_unit=base_unit, inches=inches,
#                             millimeters=millimeters, centimeters=centimeters)


#         # We need to add to the session or it won't ever be stored
#         db.session.add(unit)

#     # Once we're done, we should commit our work
#     db.session.commit()


def load_unit_conversions():
    """Load unit conversions from u.unit_conversions into database."""

    print("Unit Conversion Table")

    # Delete all rows in existing table to start fresh
    UnitConversion.query.delete()

    # Read u.volume_units file and insert data
    for row in open("seed_data/u.unit_conversions"):
        row = row.rstrip()
        base_unit, meas_type, std_unit, mult_factor = row.split("|")

        conversion = UnitConversion(base_unit=base_unit, meas_type=meas_type, 
                                    std_unit=std_unit, mult_factor=mult_factor)


        # We need to add to the session or it won't ever be stored
        db.session.add(conversion)

    # Once we're done, we should commit our work
    db.session.commit()



def load_name_conventions():
    """Load unit name conventions from u.unit_crosswalks"""

    print("Unit Formatting Table")

    # Delete all rows in existing table to start fresh
    FormattedUnit.query.delete()

    # Read u.unit_formatting file and insert data
    # TODO: think about how to handle weight ounces vs. fluid ounces
    for row in open("seed_data/u.unit_formatting"):
        row = row.rstrip()
        unit_name, formatted_name, meas_type = row.split("|")

        convention = FormattedUnit(unit_name=unit_name, 
                                    formatted_name = formatted_name, 
                                    meas_type= meas_type)


        # We need to add to the session or it won't ever be stored
        db.session.add(convention)

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()
    load_diets()
    # load_volume_units()
    # load_mass_units()
    load_name_conventions()
    load_unit_conversions()
