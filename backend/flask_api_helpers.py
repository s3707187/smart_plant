"""
Module storing API helper functionalities for ACME Smart Plant.
"""

# standard imports
import datetime
import re
import string
import random
import smtplib, ssl

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

# ------------ HELPER FUNCTIONS ----------------


def username_exists(username_to_query):
    """ 
    Helper method to check if user exists in database.

    Returns: boolean
    """
    # check username query return is not None
    username = User.query.get(username_to_query)
    if username is None:
        return False
    return True


def plant_exists(plant_to_query):
    """ 
    Helper method to check if plant exists in database.

    Returns: boolean
    """
    # check plant_id query return is not None
    plant = Plant.query.get(plant_to_query)
    if plant is None:
        return False
    return True



def password_match(plant_id, password):
    """ 
    Helper method to check if plant id/password (hashed) matches

    Returns: boolean
    """
    # check plant exists
    if plant_exists(plant_id):
        # get plant as dict
        plant = Plant.query.get(plant_id)
        result = Schema_Plant.dump(plant)
        # check password (hashed) matches exactly
        if not result['password'] == password:
            return False
        else:
            return True
    else:
        return False


def email_exists(email):
    """ 
    Helper method to check if email exists for user in database.

    Returns: boolean
    """
    # get user by matching email
    response = db.session.query(User).filter((User.email == email)).first()
    # return false if no user has this email already
    if response is None:
        return False
    return True


def get_user(username):
    """ 
    Helper method to return user details from database.

    Returns: dict
    """

    # fetch and return user details as dict
    user = User.query.get(username)
    result = Schema_User.dump(user)
    return result


def get_plant(plant_id):
    """ 
    Helper method to return plant details from database.

    Returns: dict
    """
    # fetch and return plant details as dict
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
        # append a random int and random ascii char
        word += str(random.randint(0, 9))
        word += random.choice(string.ascii_letters)
    return word


def get_plant_type(type_to_check):
    """ 
    Helper method to get details of plant_type from database

    Returns: dict
    """
    # fetch plant_type object as dict from database
    plant_type = Plant_type.query.get(type_to_check)
    result = Schema_Plant_type.dump(plant_type)
    # return dict
    return result


def plant_type_exists(plant_type_to_query):
    """ 
    Helper method to check if plant_type exists in database.

    Returns: boolean
    """
    # check plant_type exists in database (query is not None)
    plant_type = get_plant_type(plant_type_to_query)
    if plant_type is None or plant_type == {}:
        return False
    return True


def is_email(email):
    """ 
    Helper method to check if string matches email regex.

    Returns: boolean
    """
    # check email matches regex
    if re.match(r'[\w.-]+@([\w.-]+\.)+[\w-]+', email):
        return True
    return False

def get_plant_link(username, plant_id):
    """ 
    Helper method to return details of plant link from database.

    Returns: dict
    """
    # fetch plant_link from database
    plant_link = Plant_link.query.get((username, plant_id))
    # convert to dict
    result = Schema_Plant_link.dump(plant_link)
    # return None or dict
    if result == {}:
        result = None
    return result

def get_plant_maintainer(plant_id):
    """ 
    Helper method to return username of current allocated plant maintainer

    Returns: string or None
    """
    # get all plant links for this plant
    plant_links = Plant_link.query.filter_by(plant_id=plant_id).all()
    # find plant link of type maintenance
    for link in plant_links:
        # return username of maintenance link
        if link.user_type == "maintenance":
            return link.username
    return None
    

def get_plant_edit_permission(user_id, plant_id):
    """ 
    Helper method to check if user can edit plant

    Returns: boolean
    """

    # automatically return true for admins
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
    Helper method to check if user can read plant.

    Returns: boolean
    """

    # return true if user_id can read details for plant_id 
    # (i.e. is owner or viewer or admin)

    # always return true for admins
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
    # return True for admins attempting to do the editing
    user_obj = get_user(user_id)
    if user_obj["account_type"] == "admin":
        return True

    # return true if the user is editing itself
    return user_id == user_to_edit


def get_user_read_permission(user_id, user_to_edit):
    """ 
    Helper method to check if user can read other user

    Returns: boolean
    """
    # return True for admins attempting to do the reading
    user_obj = get_user(user_id)
    if user_obj["account_type"] == "admin":
        return True
        
    # return true if user is reading itself
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


