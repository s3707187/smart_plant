from flask_api_schema import *
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app
from sqlalchemy import func, ForeignKey, desc
from passlib.hash import pbkdf2_sha256
from flask_api_schema import User_Schema
from flask_jwt_extended import create_access_token, create_refresh_token
import random, string

api = Blueprint("api", __name__)

# ------------ SETUP VARIBLES -------------------


PASSWORD_LENGTH = 8
#ERRORS = []

    #{
    #"general_error": "There was some sort of validation error",
    #"password_length": "The password did not contain enough characters (min 8)",
    #"username_error": "Username is incorrect",
    #"email_error": "Email already exists or is incorrect",
    #"name_error": "name already is incorrect",
    #"login_error" : "username or password is incorrect"
    #}


# ------------ CALLABLE API METHODS ----------------

@api.route("/login", methods=["POST"])
def login():
    ERRORS = []
    # LOGIN NEEDS TO
    # - get username / check username with db
    # - return some sort of error if username has no match
    # - get plain text password and verify with db
    # - return error if password doesn't match
    # - else return tokens (access/refresh)
    username = request.json["username"]
    password = request.json["password"]

    valid_user = True
    user = None
    hashed_password = ""
    ret_val = None
    if not username_exists(username):
        valid_user = False
        #ret_val = ERRORS["login_error"]
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
        #ret_val = ERRORS["login_error"]
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
def register_new_plant():
    valid = True
    ERRORS = []
    username = request.json["username"]
    plant_type = request.json["plant_type"]
    plant_name = request.json["plant_name"]
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

    if not username_exists(username):
        valid = False
        ERRORS.append({
            "path": ['username'],
            "message": "Username does not exist"
        })

    if valid:
        new_plant = Plant(plant_type,plant_name, password)
        message = "plant successfully registered"
        db.session.add(new_plant)
        db.session.commit()
        new_plant_dict = Schema_Plant.dump(new_plant)
        print(new_plant)

        user_type = "plant_manager"
        new_plant_link = Plant_link(username, new_plant_dict['plant_id'], user_type)
        db.session.add(new_plant_link)
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

def email_exists(email):
    response = db.session.query(User).filter((User.email == email)).first()
    if response is None:
        return False
    return True

def get_user(username):
    user = User.query.get(username)
    result = Schema_User.dump(user)
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



