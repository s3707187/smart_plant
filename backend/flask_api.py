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
from flask import Blueprint, request, jsonify
# render_template, Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from flask import current_app as app
# from sqlalchemy import func, ForeignKey, desc

from flask_api_schema import User_Schema, db, User, Plant, Plant_link, \
    Schema_Plant, Schema_Plants_history, Schema_Plants_link, Plant_history, \
    Schema_Users, Schema_Plants, Schema_Plant_link, Schema_User, Schema_Plant_type, \
    Plant_type

# from functools import wraps

api = Blueprint("api", __name__)

# ------------ SETUP VARIBLES -------------------


PASSWORD_LENGTH = 8


# ------------ CALLABLE API METHODS ----------------
@api.route("/login", methods=["POST"])
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


@api.route("/register", methods=["POST"])
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


@api.route("/refresh", methods=["POST"])
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


@api.route("/register_plant", methods=["POST"])
@jwt_required
def register_new_plant():
    """ TODO docstring
    """

    valid = True
    errors = []
    # get username from token
    current_user = get_jwt_identity()
    # current_user = request.json["username"]

    plant_type = request.json["plant_type"]
    plant_name = request.json["plant_name"]
    # determine plant health by comparing data to plant_types data
    plant_health = request.json["plant_health"]

    # create a random password for plant
    password = create_random_word()

    if not plant_type_exists(plant_type):
        valid = False
        errors.append({
            "path": ['plant_type'],
            "message": "plant type is invalid. "
                       "Please ask an administrator for the valid plant types."
        })
    if len(plant_name) == 0:
        valid = False
        errors.append({
            "path": ['plant_name'],
            "message": "plant name is empty"
        })

    if not username_exists(current_user):
        valid = False
        errors.append({
            "path": ['username'],
            "message": "Username does not exist"
        })

    if valid:
        new_plant = Plant(plant_type, plant_name, password, plant_health)
        message = "plant successfully registered"
        db.session.add(new_plant)
        db.session.commit()
        new_plant_dict = Schema_Plant.dump(new_plant)

        user_type = "plant_manager"
        new_plant_link = Plant_link(current_user,
                                    new_plant_dict['plant_id'],
                                    user_type)
        db.session.add(new_plant_link)
        db.session.commit()

        return jsonify(message), 201
    else:
        return jsonify({
            "errors": errors
        }), 400


# Dashboard Page
@api.route("/get_users_plants", methods=["GET"])
@jwt_required
def get_users_plants():
    """ TODO docstring
    """

    errors = []
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
            assert len(plant) > 0
            plant = plant[0]
            result = Schema_Plant.dump(plant)
            list_of_plants.append(result)

        return jsonify(list_of_plants), 201
    else:
        errors.append({
            "path": ['username'],
            "message": "incorrect token"
        })
        return jsonify({
            "errors": errors
        }), 400


# individual plant page
@api.route("/view_plant_details", methods=["GET"])
@jwt_required
def view_plant_details():
    """ TODO docstring
    """

    errors = []
    current_user = get_jwt_identity()
    plant_id = request.args.get('plant_id')
    if (username_exists(current_user) and
            get_plant_read_permission(current_user, plant_id)):
        return jsonify(get_plant(plant_id))

    else:
        errors.append({
            "path": ['username'],
            "message": "incorrect token"
        })
        return jsonify({
            "errors": errors
        }), 400


# IOT device
@api.route("/verify_plant", methods=["POST"])
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


@api.route("/save_plant_data", methods=["POST"])
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


@api.route("/get_plant_records", methods=["GET"])
@jwt_required
def get_recent_plant_record():
    """ TODO docstring
    """

    errors = []
    current_user = get_jwt_identity()
    plant_id = request.args.get['plant_id']
    if (username_exists(current_user)
            and get_plant_read_permission(current_user, plant_id)):

        result = Plant_history.query.order_by(
            Plant_history.date_time.desc()).filter(
                Plant_history.plant_id == plant_id)

        result = Schema_Plants_history.dump(result)

        if len(result) == 0:
            errors.append({
                "path": ['plant_id'],
                "message": "plant id is invalid. Please ask an administrator "
                           "for the valid plant types."
            })
            return jsonify({
                "errors": errors
            }), 400
        else:
            return jsonify(result), 201
    else:
        errors.append({
            "path": ['username'],
            "message": "Username does not exist"
        })
        return jsonify({
            "errors": errors
        }), 403


@api.route("/delete_plant", methods=["POST"])
@jwt_required
def delete_plant():
    """ TODO docstring
    """

    errors = []
    current_user = get_jwt_identity()
    can_delete = True
    if username_exists(current_user):
        plant_id = request.json["plant_id"]

        try:
            link_delete = Plant_link.query.get(plant_id)
            db.session.delete(link_delete)
            plant_delete = Plant.query.get(plant_id)
            db.session.delete(plant_delete)
            db.session.commit()
        except sql_alchemy_error.exc.UnmappedInstanceError:
            can_delete = False
            errors.append({
                "path": ['plant_id'],
                "message": "plant_id does not exist"
            }, 403)

    else:
        can_delete = False
        errors.append({
            "path": ['username'],
            "message": "Username does not exist"
        })

    if can_delete:
        return jsonify("Plant Successfully Deleted from Database"), 201

    return jsonify({
        "errors": errors
    }), 403


@api.route("/delete_user", methods=["POST"])
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


@api.route("/update_user_details", methods=["POST"])
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


@api.route("/update_plant_details", methods=["POST"])
@jwt_required
def update_plant_details():
    """ TODO docstring
    """

    errors = []
    successful_change = True
    current_user = get_jwt_identity()
    plant_id = request.json['plant_id']
    plant_name = request.json['plant_name']
    plant_type = request.json['plant_type']
    if username_exists(current_user):
        plant_to_change = Plant.query.get(plant_id)

        if plant_name != "":
            plant_to_change.plant_name = plant_name

        if plant_type != "":
            if plant_type_exists(plant_type):
                plant_to_change.plant_type = plant_type
            else:
                successful_change = False
                errors.append({
                    "path": ['plant_type'],
                    "message": "plant type is invalid. Please ask an "
                               "administrator for the valid plant types."
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


# DEBUGGING NEED TO DELETE LOL
@api.route("/users", methods=["GET"])
def get_users():
    """ TODO docstring
    """

    user = User.query.all()
    result = Schema_Users.dump(user)
    return jsonify(result)


@api.route("/plants", methods=["GET"])
def get_plants():
    """ TODO docstring
    """

    plant = Plant.query.all()
    result = Schema_Plants.dump(plant)
    return jsonify(result)


@api.route("/plant_link", methods=["GET"])
def get_plants_link():
    """ TODO docstring
    """

    plant_link = Plant_link.query.all()
    result = Schema_Plants_link.dump(plant_link)
    return jsonify(result)


@api.route("/plant_link_user", methods=["POST"])
def get_plants_link_user():
    """ TODO docstring
    """

    username = request.json["username"]
    link_delete = Plant_link.query.get(username)
    result = Schema_Plant_link.dump(link_delete)
    return jsonify(result)


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


@api.route("/current_user", methods=["GET"])
@jwt_required
def get_current_user():
    # Access the identity of the current user
    current_user = get_jwt_identity()
    return jsonify(username=current_user), 201
