import datetime
from flask_api_schema import *
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app
from sqlalchemy import func, ForeignKey, desc
from passlib.hash import pbkdf2_sha256
from flask_api_schema import User_Schema
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import random, string
from functools import wraps

api = Blueprint("api", __name__)

# ------------ SETUP VARIBLES -------------------


PASSWORD_LENGTH = 8

# ------------ CALLABLE API METHODS ----------------

@api.route("/login", methods=["POST"])
def login():
    ERRORS = []
    username = request.json["username"]
    password = request.json["password"]

    valid_user = True
    if not username_exists(username):
        valid_user = False
        ERRORS.append({
            "path": ['username'],
            "message": "username or password is incorrect"
        })
        return jsonify({
            "errors": ERRORS
        }), 400
    else:
        hashed_password = get_user(username)["password"]

    if pbkdf2_sha256.verify(password, hashed_password) and valid_user:
        # return tokens
        return jsonify({
            "access_token": create_access_token(username),
            "refresh_token": create_refresh_token(username)
        }), 201

    else:
        ERRORS.append({
            "path": ['password'],
            "message": "username or password is incorrect"
        })
        return jsonify({
            "errors": ERRORS
        }), 400

@api.route("/register", methods=["POST"])
def register_new_user():
    ERRORS = []
    valid_user = True
    username = request.json["username"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    email = request.json["email"]
    password = request.json["password"]
    account_type = request.json["account_type"]

    if len(password) >= PASSWORD_LENGTH:
        hashed_password = pbkdf2_sha256.hash(password)
    else:
        valid_user = False
        ERRORS.append({
            "path": ['password'],
            "message": "The password did not contain enough characters (min 8)"
        })
    if username_exists(username):
        valid_user = False
        ERRORS.append({
            "path": ['username'],
            "message": "Username already exists or is incorrect"
        })
    if email_exists(email):
        valid_user = False
        ERRORS.append({
            "path": ['email'],
            "message": "Email already exists or is incorrect"
        })
    if not first_name.isalpha() or len(first_name) == 0:
        valid_user = False
        ERRORS.append({
            "path": ['first_name'],
            "message": "first name is incorrect"
        })
    if not last_name.isalpha() or len(last_name) == 0:
        valid_user = False
        ERRORS.append({
            "path": ['last_name'],
            "message": "lastname is incorrect"
        })

    if valid_user:
        new_user = User(username, hashed_password, first_name, last_name, email, account_type)
        message = "user successfully registered"
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message), 201
    else:
        return jsonify({
            "errors": ERRORS
        }), 400

@api.route("/register_plant", methods=["POST"])
#@jwt_required
def register_new_plant():
    valid = True
    ERRORS = []
    # get username from token
    #current_user = get_jwt_identity()
    current_user = request.json["username"]

    plant_type = request.json["plant_type"]
    plant_name = request.json["plant_name"]
    # determine plant health by comparing data to plant_types data
    plant_health = request.json["plant_health"]

    # create a random password for plant
    password = create_random_word()

    if not plant_type_exists(plant_type):
        valid = False
        ERRORS.append({
            "path": ['plant_type'],
            "message": "plant type is incorrect"
        })
    if len(plant_name) == 0:
        valid = False
        ERRORS.append({
            "path": ['plant_name'],
            "message": "plant name is empty"
        })

    if not username_exists(current_user):
        valid = False
        ERRORS.append({
            "path": ['username'],
            "message": "Username does not exist"
        })

    if valid:
        new_plant = Plant(plant_type,plant_name, password, plant_health)
        message = "plant successfully registered"
        db.session.add(new_plant)
        db.session.commit()
        new_plant_dict = Schema_Plant.dump(new_plant)

        user_type = "plant_manager"
        new_plant_link = Plant_link(current_user, new_plant_dict['plant_id'], user_type)
        db.session.add(new_plant_link)
        db.session.commit()

        return jsonify(message), 201
    else:
        return jsonify({
            "errors": ERRORS
        }), 400

#Dashboard Page
@api.route("/get_users_plants", methods=["GET"])
@jwt_required
def get_users_plants():
    ERRORS=[]
    current_user = get_jwt_identity()
    if username_exists(current_user):
        plants = []
        list_of_plants = []

        plant_link = Plant_link.query.filter_by(username=current_user).all()
        link = Schema_Plants_link.dump(plant_link)

        for x in link:
            if plant_exists(x["plant_id"]):
                plants.append(x["plant_id"])

        for i in plants:
            plant = Plant.query.filter_by(plant_id=i).all()
            result = Schema_Plant.dump(plant)
            list_of_plants.append(result)

        return jsonify(list_of_plants), 201
    else:
        ERRORS.append({
            "path": ['username'],
            "message": "incorrect token"
        })
        return jsonify({
            "errors": ERRORS
        }), 400


#individual plant page
@api.route("/view_plant_details", methods=["GET"])
def view_plant_details():
    plant_id = request.request.args.get['plant_id']
    return jsonify(get_plant(plant_id))

#IOT device
@api.route("/verify_plant", methods=["GET"])
def verify_plant():
    plant_id = request.request.args.get["plant_id"]
    password = request.request.args.get["password"]
    invalid_message = "incorrect password"
    valid_message = "Plant successfully verified"

    if password_match(plant_id, password):
        return jsonify(valid_message), 200
    else:
        return jsonify(invalid_message), 401


@api.route("/save_plant_data", methods=["POST"])
def save_plant_data():
    ERRORS= []
    plant_id = request.json["plant_id"]
    date_time = request.json["date_time"]
    light = request.json["light"]
    moisture = request.json["moisture"]
    humidity = request.json["humidity"]
    temperature = request.json["temperature"]

    #validate plant details
    valid = True
    if not plant_exists(plant_id):
        valid = False
        ERRORS.append({
            "path": ['plant_id'],
            "message": "Username does not exist"
        }), 403

    if not isinstance(light,float):
        valid = False
        ERRORS.append({
            "path": ['light'],
            "message": "light is invalid"
        }), 403

    if not isinstance(moisture, float):
        valid = False
        ERRORS.append({
            "path": ['moisture'],
            "message": "moisture is invalid"
        }), 403

    if not isinstance(humidity, float):
        valid = False
        ERRORS.append({
            "path": ['humidity'],
            "message": "humidity is invalid"
        }), 403

    if not isinstance(temperature, float):
        valid = False
        ERRORS.append({
            "path": ['temperature'],
            "message": "temperature is invalid"
        }), 403

    if valid:
        new_plant_history = Plant_history(plant_id, date_time, light, moisture, humidity, temperature)
        message = "New plant record successfully registered"
        db.session.add(new_plant_history)
        db.session.commit()
        return jsonify(message), 201
    else:
        return jsonify({
            "errors": ERRORS
        }), 400


# DEBUGGING NEED TO DELETE LOL
@api.route("/users", methods=["GET"])
def get_users():
    user = User.query.all()
    result = Schema_Users.dump(user)
    return jsonify(result)

@api.route("/plants", methods=["GET"])
def get_plants():
    plant = Plant.query.all()
    result = Schema_Plants.dump(plant)
    return jsonify(result)

@api.route("/plant_link", methods=["GET"])
def get_plants_link():
    plant_link = Plant_link.query.all()
    result = Schema_Plants_link.dump(plant_link)
    return jsonify(result)

# ------------ HELPER FUNCTIONS ----------------

def username_exists(username_to_query):
    username = User.query.get(username_to_query)
    if username is None:
        return False
    return True

def plant_exists(plant_to_query):
    plant = Plant.query.get(plant_to_query)
    if plant is None:
        return False
    return True

def password_match(plant_id, password):
    if plant_exists(plant_id):
        plant = Plant.query.get(plant_id)
        result = Schema_Plant.dump(plant)

        if not result['password'] == password:
            return False
        else:
            return True

def email_exists(email):
    response = db.session.query(User).filter((User.email == email)).first()
    if response is None:
        return False
    return True

def get_user(username):
    user = User.query.get(username)
    result = Schema_User.dump(user)
    return result

def get_plant(plant_id):
    plant = Plant.query.get(plant_id)
    result = Schema_Plant.dump(plant)
    return result

def create_random_word():
    word = ""
    for i in range(4):
        word += str(random.randint(0,9))
        word += random.choice(string.ascii_letters)
    return word

def get_plant_type(type):
    plant_type = Plant_type.query.get(type)
    result = Schema_Plant_type.dump(plant_type)
    return result

def plant_type_exists(plant_type_to_query):
    plant_type = get_plant_type(plant_type_to_query)
    if plant_type is None:
        return False
    return True


#?jwt=<token>
@api.route("/current_user", methods=["GET"])
@jwt_required
def get_current_user():
    # Access the identity of the current user
    current_user = get_jwt_identity()
    return jsonify(username=current_user), 201