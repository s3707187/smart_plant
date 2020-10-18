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
SCALED_MIN = 0.33846
SCALED_MAX = 0.66154

# ------------ SETUP VARIBLES -------------------


# ------------ CALLABLE API METHODS ----------------
@IOT_API.route("/emailme", methods=["GET"])
def emailme():
    email("rohap12@gmail.com", "hello")
    hi = "Hi"
    return hi

#DELETE THIS
@IOT_API.route("/plants", methods=["GET"])
def get_plants():
    """ TODO docstring
    """

    plant = Plant.query.all()
    result = Schema_Plants.dump(plant)
    return jsonify(result)

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
    # date_time = datetime.datetime.now().strftime("%H:%M:%S %Y-%m-%d") #request.json["date_time"]
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

    if not (isinstance(light, float) or isinstance(light, int)):
        valid = False
        errors.append({
            "path": ['light'],
            "message": "light is invalid"
        })

    if not (isinstance(moisture, float) or isinstance(moisture, int)):
        valid = False
        errors.append({
            "path": ['moisture'],
            "message": "moisture is invalid"
        })

    if not (isinstance(humidity, float) or isinstance(humidity, int)):
        valid = False
        errors.append({
            "path": ['humidity'],
            "message": "humidity is invalid"
        })

    if not (isinstance(temperature, float) or isinstance(temperature, int)):
        valid = False
        errors.append({
            "path": ['temperature'],
            "message": "temperature is invalid"
        })

    if valid:
        plant_check = Plant.query.get(plant_id)
        plant_result = Schema_Plant.dump(plant_check)

        type_check = Plant_type.query.get(plant_result['plant_type'])
        type_result = Schema_Plant_type.dump(type_check)

        #toScaledRadarData(healthMin, healthMax, dataPoint)
        scaled_humidity = toScaledRadarData(type_result['humidity_min'], type_result['humidity_max'], humidity)
        scaled_moisture = toScaledRadarData(type_result['moisture_min'], type_result['moisture_max'], moisture)
        scaled_temperature = toScaledRadarData(type_result['temp_min'], type_result['temp_max'], temperature)
        scaled_light = toScaledRadarData(type_result['light_min'], type_result['light_max'], light)

        real_time = datetime.datetime.strptime(date_time, "%H:%M:%S %Y-%m-%d")
        new_plant_history = Plant_history(
            plant_id, real_time, scaled_temperature, scaled_humidity, scaled_light, scaled_moisture)
        message = "New plant record successfully registered"
        db.session.add(new_plant_history)
        
        # count number of unhealthy fields
        total_unhealthy = 0
        db.session.commit()

        for val in (scaled_humidity, scaled_moisture, scaled_temperature, scaled_light):
            if val < SCALED_MIN or val > SCALED_MAX:
                total_unhealthy += 1
        # update health
        if total_unhealthy > 0:
            plant_check.plant_health = "unhealthy"
        else:
            plant_check.plant_health = "healthy"
        # commit any plant change and new plant history
        db.session.commit()
        return jsonify(message), 201
    else:
        return jsonify({
            "errors": errors
        }), 400
