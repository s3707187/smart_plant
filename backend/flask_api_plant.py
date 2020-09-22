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
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims

# other imports
from backend.flask_api_schema import *
from backend.flask_api_schema import db
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

PLANT_API = Blueprint("plant_api", __name__)

# ------------ SETUP VARIBLES -------------------


# ------------ CALLABLE API METHODS ----------------
@PLANT_API.route("/register_plant", methods=["POST"])
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
@PLANT_API.route("/get_users_plants", methods=["GET"])
@jwt_required
def get_users_plants():
    """ TODO docstring
    """
    errors = []
    current_user = get_jwt_identity()
    if username_exists(current_user):
        if get_jwt_claims()['role'] == "admin":
            plant = Plant.query.all()
            print(plant)
            result = Schema_Plants.dump(plant)
            return jsonify(result), 200
        else:
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

            return jsonify(list_of_plants), 200
    else:
        errors.append({
            "path": ['username'],
            "message": "incorrect token"
        })
        return jsonify({
            "errors": errors
        }), 400


# individual plant page
@PLANT_API.route("/view_plant_details", methods=["GET"])
@jwt_required
def view_plant_details():
    """ TODO docstring
    """

    errors = []
    current_user = get_jwt_identity()
    plant_id = request.args.get('plant_id')
    if (username_exists(current_user) and
        get_plant_read_permission(current_user, plant_id)):
        
        plant_info = get_plant(plant_id)
        latest_reading = Plant_history.query.order_by(
            Plant_history.date_time.desc()).filter(
                Plant_history.plant_id == plant_id).limit(1)

        latest_reading = Schema_Plants_history.dump(latest_reading)
        if len(latest_reading) == 1:
            plant_info["latest_reading"] = latest_reading[0]
        else:
            plant_info["latest_reading"] = None
        
        if not get_plant_edit_permission(current_user, plant_id):
            plant_info["password"] = None
            plant_info["access"] = "read"
        else:
            plant_info["access"] = "edit"
        return jsonify(plant_info)

    else:
        errors.append({
            "path": ['username'],
            "message": "incorrect token or invalid permission"
        })
        return jsonify({
            "errors": errors
        }), 400


@PLANT_API.route("/get_plant_records", methods=["GET"])
@jwt_required
def get_recent_plant_record():
    """ TODO docstring
    """

    errors = []
    current_user = get_jwt_identity()
    plant_id = request.args.get('plant_id')
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
            return jsonify(result), 200
    else:
        errors.append({
            "path": ['username'],
            "message": "Username does not exist"
        })
        return jsonify({
            "errors": errors
        }), 403


@PLANT_API.route("/delete_plant", methods=["POST"])
@jwt_required
def delete_plant():
    """ TODO docstring
    """

    errors = []
    current_user = get_jwt_identity()
    can_delete = True
    plant_id = request.json["plant_id"]

    if (username_exists(current_user)
        and get_plant_edit_permission(current_user, plant_id)):

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
            "message": "Username does not exist or does not have permission"
        })

    if can_delete:
        return jsonify("Plant Successfully Deleted from Database"), 201

    return jsonify({
        "errors": errors
    }), 403


@PLANT_API.route("/update_plant_details", methods=["POST"])
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
    if (username_exists(current_user)
        and get_plant_edit_permission(current_user, plant_id)):

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
            "message": "Username does not exist or does not have permission"
        })

    if successful_change:
        db.session.commit()
        return jsonify("User Details Successfully Changed"), 201
    else:
        return jsonify({
            "errors": errors
        }), 403

@PLANT_API.route("/get_plant_members", methods=["GET"])
@jwt_required
def get_plant_members():
    """ TODO docstring
    """

    errors = []
    current_user = get_jwt_identity()
    plant_id = request.args.get('plant_id')

    if get_plant_read_permission(current_user, plant_id):
        plant_links = Plant_link.query.filter_by(plant_id=plant_id).all()
        links = Schema_Plants_link.dump(plant_links)
        # print(links)
        user_ids = []
        for link in links:
            if link["user_type"] == "plant_viewer":
                user_ids.append(link["username"])
        return jsonify(user_ids), 200

    else:
        errors.append({
            "path": ['plant_id'],
            "message": "User does not have permission to view plant details."
        })
        return jsonify({
            "errors": errors
        }), 400