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

from flask_api_helpers import *


# from functools import wraps

IOT_API = Blueprint("iot_api", __name__)

# ------------ SETUP VARIBLES -------------------


# ------------ CALLABLE API METHODS ----------------

# IOT device
@IOT_API.route("/verify_plant", methods=["POST"])
def verify_plant():
    """ TODO docstring
    """

    plant_id = request.json["plant_id"]
    password = request.json["password"]
    invalid_message = "incorrect password"
    valid_message = "Plant successfully verified"

    if password_match(plant_id, password):
        return jsonify(valid_message), 200
    else:
        return jsonify(invalid_message), 401


@IOT_API.route("/save_plant_data", methods=["POST"])
def save_plant_data():
    """ TODO docstring
    """

    errors = []
    plant_id = request.json["plant_id"]
    date_time = request.json["date_time"]
    light = request.json["light"]
    moisture = request.json["moisture"]
    humidity = request.json["humidity"]
    temperature = request.json["temperature"]
    password = request.json["password"]

    # validate plant details
    valid = True
    if not plant_exists(plant_id):
        valid = False
        errors.append({
            "path": ['plant_id'],
            "message": "Username does not exist"
        })

    if not password_match(plant_id, password):
        valid = False
        errors.append({
            "path": ['password'],
            "message": "invalid password"
        })

    if not isinstance(light, float):
        valid = False
        errors.append({
            "path": ['light'],
            "message": "light is invalid"
        })

    if not isinstance(moisture, float):
        valid = False
        errors.append({
            "path": ['moisture'],
            "message": "moisture is invalid"
        })

    if not isinstance(humidity, float):
        valid = False
        errors.append({
            "path": ['humidity'],
            "message": "humidity is invalid"
        })

    if not isinstance(temperature, float):
        valid = False
        errors.append({
            "path": ['temperature'],
            "message": "temperature is invalid"
        })

    if valid:
        real_time = datetime.datetime.strptime(date_time, "%H:%M:%S %Y-%m-%d")
        new_plant_history = Plant_history(
            plant_id, real_time, temperature, humidity, light, moisture)
        message = "New plant record successfully registered"
        db.session.add(new_plant_history)
        db.session.commit()
        return jsonify(message), 201
    else:
        return jsonify({
            "errors": errors
        }), 400
