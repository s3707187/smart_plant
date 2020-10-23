# standard imports
import datetime
import re
import string
import random
import smtplib, ssl
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
    """ 
    Helper method to check if user exists in database.

    Returns: boolean
    """

    username = User.query.get(username_to_query)
    if username is None:
        return False
    return True


def plant_exists(plant_to_query):
    """ 
    Helper method to check if plant exists in database.

    Returns: boolean
    """

    plant = Plant.query.get(plant_to_query)
    if plant is None:
        return False
    return True



def password_match(plant_id, password):
    """ 
    Helper method to check if plant id/password matches

    Returns: boolean
    """

    if plant_exists(plant_id):
        plant = Plant.query.get(plant_id)
        result = Schema_Plant.dump(plant)

        if not result['password'] == password:
            return False
        else:
            return True


def email_exists(email):
    """ 
    Helper method to check if email exists for user in database.

    Returns: boolean
    """

    response = db.session.query(User).filter((User.email == email)).first()
    if response is None:
        return False
    return True


def get_user(username):
    """ 
    Helper method to return user details from database.

    Returns: dict
    """

    user = User.query.get(username)
    result = Schema_User.dump(user)
    return result


def get_plant(plant_id):
    """ 
    Helper method to return plant details from database.

    Returns: dict
    """

    plant = Plant.query.get(plant_id)
    result = Schema_Plant.dump(plant)
    return result


def create_random_word():
    """ 
    Helper method to create random 8 character string

    Returns: string
    """

    word = ""
    for i in range(4):
        word += str(random.randint(0, 9))
        word += random.choice(string.ascii_letters)
    return word


def get_plant_type(type_to_check):
    """ 
    Helper method to get details of plant_type from database

    Returns: dict
    """

    plant_type = Plant_type.query.get(type_to_check)
    result = Schema_Plant_type.dump(plant_type)
    return result


def plant_type_exists(plant_type_to_query):
    """ 
    Helper method to check if plant_type exists in database.

    Returns: boolean
    """

    plant_type = get_plant_type(plant_type_to_query)
    if plant_type is None or plant_type == {}:
        return False
    return True


def is_email(email):
    """ 
    Helper method to check if string matches email regex.

    Returns: boolean
    """

    if re.match(r'[\w.-]+@([\w.-]+\.)+[\w-]+', email):
        return True
    return False

def get_plant_link(username, plant_id):
    """ 
    Helper method to return details of plant link from database.

    Returns: dict
    """
    plant_link = Plant_link.query.get((username, plant_id))
    result = Schema_Plant_link.dump(plant_link)
    if result == {}:
        result = None
    return result

def get_plant_maintainer(plant_id):
    """ 
    Helper method to return username of current allocated plant maintainer

    Returns: string or None
    """
    plant_links = Plant_link.query.filter_by(plant_id=plant_id).all()
    for link in plant_links:
        if link.user_type == "maintenance":
            return link.username
    return None
    

def get_plant_edit_permission(user_id, plant_id):
    """ 
    Helper method to check if user can edit plant

    Returns: boolean
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
    """ 
    Helper method to check if user can read plant

    Returns: boolean
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
    """ 
    Helper method to check if user can edit other user

    Returns: boolean
    """
    user_obj = get_user(user_id)
    if user_obj["account_type"] == "admin":
        return True

    # return true if user_id = user_to_edit or if user_id is an admin
    return user_id == user_to_edit


def get_user_read_permission(user_id, user_to_edit):
    """ 
    Helper method to check if user can read other user

    Returns: boolean
    """
    user_obj = get_user(user_id)
    if user_obj["account_type"] == "admin":
        return True
        
    # return true if user_id = user_to_edit or if user_id is an admin
    return user_id == user_to_edit


def toScaledRadarData(healthMin, healthMax, dataPoint):
    """ 
    Helper method to convert data point to a scaled form for radar displays

    Returns: float (between 0 and 1)
    """
    # Static modifier for the standard deviation, this determines how large the healthy range should be on the chart
    dMod = 1.2
    # Calculated difference between min and max
    diff = healthMax - healthMin
    # Calculate midpoint of healthy range, this is the mean of the normal distribution
    mean = healthMax - (diff / 2)
    # Calculated scaled data, as well as the threshold for the min/max data
    sData = norm.cdf(dataPoint, mean, dMod * (diff))
    
    return sData #output

def send_password_email(target_email, temp_password):
    """ 
    Helper method to send email with temporary password to a user.

    Returns: None
    """
    port = 465  # For SSL
    password = "progamproject123"

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("progam.project.fellas@gmail.com", password)
        sender_email = "progam.project.fellas@gmail.com"
        target_email = target_email
        # message contents

        message = """\
        Subject: ACME Smart Plant Password Reset

        Your ACME Smart Plant temporary password is: """

        temp_password = temp_password

        warning = "\n!!! PLEASE CHANGE YOUR PASSWORD NEXT TIME YOU LOG IN !!!."

        # Send email here
        server.sendmail(sender_email, target_email, message + temp_password + warning)


