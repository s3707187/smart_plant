# standard imports
import datetime
import re
import string
import random
# import json
# import os
# import requests

# third party imports
from sqlalchemy import orm as sql_alchemy_error
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, \
    jwt_required, jwt_refresh_token_required

# other imports
from flask_api_schema import *
from flask_api_schema import db
from flask import Blueprint, request, jsonify
# render_template, Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from flask import current_app as app
# from sqlalchemy import func, ForeignKey, desc

# from flask_api_schema import User_Schema, db, User, Plant, Plant_link, \
#     Schema_Plant, Schema_Plants_history, Schema_Plants_link, Plant_history, \
#     Schema_Users, Schema_Plants, Schema_Plant_link, Schema_User, Schema_Plant_type, \
#     Plant_type

# ------------ HELPER FUNCTIONS ----------------


def username_exists(username_to_query):
    """ TODO docstring
    """

    username = User.query.get(username_to_query)
    if username is None:
        return False
    return True


def plant_exists(plant_to_query):
    """ TODO docstring
    """

    plant = Plant.query.get(plant_to_query)
    if plant is None:
        return False
    return True


def password_match(plant_id, password):
    """ TODO docstring
    """

    if plant_exists(plant_id):
        plant = Plant.query.get(plant_id)
        result = Schema_Plant.dump(plant)

        if not result['password'] == password:
            return False
        else:
            return True


def email_exists(email):
    """ TODO docstring
    """

    response = db.session.query(User).filter((User.email == email)).first()
    if response is None:
        return False
    return True


def get_user(username):
    """ TODO docstring
    """

    user = User.query.get(username)
    result = Schema_User.dump(user)
    return result


def get_plant(plant_id):
    """ TODO docstring
    """

    plant = Plant.query.get(plant_id)
    result = Schema_Plant.dump(plant)
    return result


def create_random_word():
    """ TODO docstring
    """

    word = ""
    for i in range(4):
        word += str(random.randint(0, 9))
        word += random.choice(string.ascii_letters)
    return word


def get_plant_type(type):
    """ TODO docstring
    """

    plant_type = Plant_type.query.get(type)
    result = Schema_Plant_type.dump(plant_type)
    return result


def plant_type_exists(plant_type_to_query):
    """ TODO docstring
    """

    plant_type = get_plant_type(plant_type_to_query)
    if plant_type is None or plant_type == {}:
        return False
    return True


def is_email(email):
    """ TODO docstring
    """

    if re.match(r'[\w.-]+@([\w.-]+\.)+[\w-]+', email):
        return True
    return False


def get_plant_edit_permission(user_id, plant_id):
    """ TODO docstring
    """

    # return true if user_id can edit details for plant_id (i.e. is the owner)
    # (including whether they can edit the links for that plant, which they can
    # if they own it)
    # admins get TRUE too
    # use this to determine if they can get the plant password too
    pass


def get_plant_read_permission(user_id, plant_id):
    """ TODO docstring
    """

    # return true if user_id can READ details for plant_id (i.e. is owner or viewer)
    # admins get TRUE too
    pass


def get_user_edit_permission(user_id, user_to_edit):
    """ TODO docstring
    """

    # return true if user_id = user_to_edit or if user_id is an admin
    pass


def get_user_read_permission(user_id, user_to_edit):
    """ TODO docstring
    """

    # return true if user_id = user_to_edit or if user_id is an admin
    pass
