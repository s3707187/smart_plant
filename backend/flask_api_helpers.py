# standard imports
import datetime
import re
import string
import random
# import json
# import os
# import requests

# third party imports
from scipy.stats import norm
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


# def get_plant_link(user_id, plant_id_to_query):
#     """ TODO docstring
#     """

#     plant_link = Plant_link.query.filter_by(username=user_id, plant_id=plant_id_to_query)
#     # print(plant_link)
#     # plant_link = Plant_link.query.get(user_id).filter_by(plant_id=plant_id)
#     links = Schema_Plants_link.dump(plant_link)
#     print(links)
#     return links

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


def get_plant_type(type_to_check):
    """ TODO docstring
    """

    plant_type = Plant_type.query.get(type_to_check)
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

def get_plant_link(username, plant_id):
    """ TODO docstring
    """
    plant_link = Plant_link.query.get((username, plant_id))
    result = Schema_Plant_link.dump(plant_link)
    if result == {}:
        result = None
    return result

def get_plant_edit_permission(user_id, plant_id):
    """ TODO docstring
    """

    # return true if user_id can edit details for plant_id (i.e. is the owner)
    # (including whether they can edit the links for that plant, which they can
    # if they own it)
    # admins get TRUE too
    # use this to determine if they can get the plant password too
    user_obj = get_user(user_id)
    if user_obj["account_type"] == "admin":
        return True
    # get the links for a plant_id
    plant_links = Plant_link.query.filter_by(plant_id=plant_id).all()
    links = Schema_Plants_link.dump(plant_links)
    # search through links and see if user_id is inside a plant_manager link
    for link in links:
        if link["user_type"] == "plant_manager":
            if link["username"] == user_id:
                return True

    return False


def get_plant_read_permission(user_id, plant_id):
    """ TODO docstring
    """

    # return true if user_id can READ details for plant_id (i.e. is owner or viewer)
    # admins get TRUE too
    user_obj = get_user(user_id)
    if user_obj["account_type"] == "admin":
        return True

    # get the links for a plant_id
    plant_links = Plant_link.query.filter_by(plant_id=plant_id).all()
    links = Schema_Plants_link.dump(plant_links)
    # search through links and see if user_id is inside
    for link in links:
        if link["username"] == user_id:
            return True

    return False


def get_user_edit_permission(user_id, user_to_edit):
    """ TODO docstring
    """
    user_obj = get_user(user_id)
    if user_obj["account_type"] == "admin":
        return True

    # return true if user_id = user_to_edit or if user_id is an admin
    return user_id == user_to_edit


def get_user_read_permission(user_id, user_to_edit):
    """ TODO docstring
    """
    user_obj = get_user(user_id)
    if user_obj["account_type"] == "admin":
        return True
        
    # return true if user_id = user_to_edit or if user_id is an admin
    return user_id == user_to_edit


def toScaledRadarData(healthMin, healthMax, dataPoint):
    # Static modifier for the standard deviation, this determines how large the healthy range should be on the chart
    dMod = 1.2
    # Calculated difference between min and max
    diff = healthMax - healthMin
    # Calculate midpoint of healthy range, this is the mean of the normal distribution
    mean = healthMax - (diff / 2)
    # Calculated scaled data, as well as the threshold for the min/max data
    sData = norm.cdf(dataPoint, mean, dMod * (diff))
    # sMin = norm.cdf(healthMin, mean, dMod * (diff))
    # sMax = norm.cdf(healthMax, mean, dMod * (diff))
    # output = {
    #     "scaledData": sData,
    #     "scaledMin": sMin,
    #     "scaledMax": sMax
    # }
    # print(sMin)
    return sData #output
