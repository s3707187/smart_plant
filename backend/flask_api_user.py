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

USER_API = Blueprint("api", __name__)

# ------------ SETUP VARIBLES -------------------


PASSWORD_LENGTH = 8


# ------------ CALLABLE API METHODS ----------------
@USER_API.route("/login", methods=["POST"])
def login():
    """ TODO docstring
    """

    errors = []
    username = request.json["username"]
    password = request.json["password"]

    valid_user = True
    if not username_exists(username):
        valid_user = False
        errors.append({
            "path": ['username'],
            "message": "username or password is incorrect"
        })
        return jsonify({
            "errors": errors
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
        errors.append({
            "path": ['password'],
            "message": "username or password is incorrect"
        })
        return jsonify({
            "errors": errors
        }), 400


@USER_API.route("/register", methods=["POST"])
def register_new_user():
    """ TODO docstring
    """

    errors = []
    valid_user = True
    username = request.json["username"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    email = request.json["email"]
    password = request.json["password"]
    # account_type = request.json["account_type"]
    account_type = "user"

    if len(password) >= PASSWORD_LENGTH:
        hashed_password = pbkdf2_sha256.hash(password)
    else:
        valid_user = False
        errors.append({
            "path": ['password'],
            "message": "The password did not contain enough characters (min 8)"
        })
    if username_exists(username):
        valid_user = False
        errors.append({
            "path": ['username'],
            "message": "Username already exists or is incorrect"
        })
    if email_exists(email) or not is_email(email):
        valid_user = False
        errors.append({
            "path": ['email'],
            "message": "Email already exists or is incorrect"
        })
    if not first_name.isalpha() or len(first_name) == 0:
        valid_user = False
        errors.append({
            "path": ['first_name'],
            "message": "first name is incorrect"
        })
    if not last_name.isalpha() or len(last_name) == 0:
        valid_user = False
        errors.append({
            "path": ['last_name'],
            "message": "lastname is incorrect"
        })

    if valid_user:
        new_user = User(username, hashed_password,
                        first_name, last_name, email, account_type)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "access_token": create_access_token(username),
            "refresh_token": create_refresh_token(username)
        }), 201
    else:
        return jsonify({
            "errors": errors
        }), 400


@USER_API.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    """ TODO docstring
    """

    current_user = get_jwt_identity()
    if username_exists(current_user):
        return jsonify({
            "access_token": create_access_token(current_user)
        }), 201
    else:
        return jsonify({
            "errors": [{
                "message": "The token is invalid",
                "path": []
            }]
        }), 401



@USER_API.route("/delete_user", methods=["POST"])
@jwt_required
def delete_user():
    """ TODO docstring
    """

    errors = []
    current_user = get_jwt_identity()
    can_delete = True
    if username_exists(current_user):
        username = current_user

        try:
            link_delete = Plant_link.query.get(username)
            db.session.delete(link_delete)
        except sql_alchemy_error.exc.UnmappedInstanceError:
            pass
        try:
            user_delete = User.query.get(username)
            db.session.delete(user_delete)
            db.session.commit()
        except sql_alchemy_error.exc.UnmappedInstanceError:
            can_delete = False
            errors.append({
                "path": ['username'],
                "message": "username does not exist"
            }, 403)
    else:
        can_delete = False
        errors.append({
            "path": ['username'],
            "message": "Username does not exist"
        })

    if can_delete:
        return jsonify("User Successfully Deleted from Database"), 201
    return jsonify({
        "errors": errors
    }), 403


@USER_API.route("/update_user_details", methods=["POST"])
@jwt_required
def update_user_details():
    """ TODO docstring
    """

    errors = []
    successful_change = True
    current_user = get_jwt_identity()
    password = request.json['password']
    email = request.json['email']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    if username_exists(current_user):
        user_to_change = User.query.get(current_user)
        if password != "":
            if len(password) >= PASSWORD_LENGTH:
                hashed_password = pbkdf2_sha256.hash(password)
                user_to_change.password = hashed_password
            else:
                successful_change = False
                errors.append({
                    "path": ['password'],
                    "message": "The password did not contain "
                               "enough characters (min 8)"
                })
        if email != "":
            if is_email(email):
                user_to_change.email = email
            else:
                successful_change = False
                errors.append({
                    "path": ['email'],
                    "message": "Email already exists or is incorrect"
                })

        if first_name != "":
            if first_name.isalpha() and len(first_name) > 0:
                user_to_change.first_name = first_name
            else:
                errors.append({
                    "path": ['first_name'],
                    "message": "first name is incorrect"
                })
        if last_name != "":
            if last_name.isalpha() and len(last_name) > 0:
                user_to_change.last_name = last_name
            else:
                successful_change = False
                errors.append({
                    "path": ['last_name'],
                    "message": "lastname is incorrect"
                })

    else:
        successful_change = False
        errors.append({
            "path": ['username'],
            "message": "Username does not exist"
        })

    if successful_change:
        db.session.commit()
        return jsonify("User Details Successfully Changed"), 201
    else:
        return jsonify({
            "errors": errors
        }), 403


@USER_API.route("/current_user", methods=["GET"])
@jwt_required
def get_current_user():
    """ TODO docstring
    """

    # Access the identity of the current user
    current_user = get_jwt_identity()
    return jsonify(username=current_user), 201