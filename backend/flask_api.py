from flask_api_schema import *
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app
from sqlalchemy import func, ForeignKey, desc
from passlib.hash import pbkdf2_sha256
from flask_api_schema import User_Schema
from flask_jwt_extended import create_access_token


api = Blueprint("api", __name__)

# ------------ SETUP VARIBLES -------------------


PASSWORD_LENGTH = 8
ERRORS = {
    "general_error": "There was some sort of validation error",
    "password_length": "The password did not contain enough characters (min 8)",
    "username_error": "Username is incorrect",
    "email_error": "Email already exists or is incorrect",
    "name_error": "name already is incorrect",
    "login_error" : "username or password is incorrect"
    }


# ------------ CALLABLE API METHODS ----------------

@api.route("/login", methods=["POST"])
def login():
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
        ret_val = ERRORS["login_error"]
    else:
        hashed_password = get_user(username)["password"]

    if pbkdf2_sha256.verify(password, hashed_password) and valid_user:
        # return tokens
      #  ret_val = jsonify({
       #     "access_token": create_access_token("tom", expires_delta=datetime.timedelta(seconds=5)),
        #    "refresh_token": create_refresh_token("tom")
       # }), 201
    else:
        ret_val = ERRORS["login_error"]

    return ret_val

@api.route("/register", methods=["POST"])
def register_new_user():

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
        message = ERRORS["password_length"]
    if username_exists(username):
        valid_user = False
        message = ERRORS["username_error"]
    if email_exists(email):
        valid_user = False
        message = ERRORS["email_error"]
    if not first_name.isalpha() or len(first_name) == 0:
        valid_user = False
        message = ERRORS["name_error"]
    if not last_name.isalpha() or len(last_name) == 0:
        valid_user = False
        message = ERRORS["name_error"]

    if valid_user:
        new_user = User(username, hashed_password, first_name, last_name, email, account_type)
        message = "user successfully registered"
        db.session.add(new_user)
        db.session.commit()

    return message
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

@api.route("/users", methods=["GET"])
def getUsers():
    user = User.query.all()
    result = Schema_Users.dump(user)
    return jsonify(result)

