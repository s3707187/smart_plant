"""
Module storing Plant API functionalities for ACME Smart Plant.
"""
# standard imports
import datetime
import re
import string
import random

# third party imports
from sqlalchemy import orm as sql_alchemy_error
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims

# other imports
from flask_api_schema import *
from flask_api_schema import db
from flask import Blueprint, request, jsonify

from flask_api_helpers import *


# ------------ SETUP VARIBLES -------------------

# instantiate API
PLANT_API = Blueprint("plant_api", __name__)


# ------------ CALLABLE API METHODS ----------------
@PLANT_API.route("/register_plant", methods=["POST"])
@jwt_required
def register_new_plant():
    """ 
    API method to add a plant to the system

    Method: POST

    JSON Parameters: plant_type, plant_name, plant_owner
    Optional JSON Parameters: plant_health

    JWT: Required
    """
    valid = True
    errors = []
    # get username from token
    current_user = get_jwt_identity()

    plant_type = request.json["plant_type"]
    plant_name = request.json["plant_name"]
    # optional plant_health on registration
    plant_health = "healthy"
    if "plant_health" in request.json:
        plant_health = request.json["plant_health"]
    plant_owner = request.json.get("plant_owner", None)

    # allow only admins to register plants with another owner
    if plant_owner is not None and get_jwt_claims()['role'] != "admin":
        return jsonify({
            "errors": [{"message": "You do not have permission to do this.", "path": ["plant_owner"]}]
        }), 403

    # create a random password for plant
    password = create_random_word()

    # check plant_type exists
    if not plant_type_exists(plant_type):
        valid = False
        errors.append({
            "path": ['plant_type'],
            "message": "plant type is invalid. "
                       "Please ask an administrator for the valid plant types."
        })
    # check plant_name is not empty
    if len(plant_name) == 0:
        valid = False
        errors.append({
            "path": ['plant_name'],
            "message": "plant name is empty"
        })

    # check current_user or submitted plant_owner exist
    user = current_user if plant_owner is None else plant_owner
    if not username_exists(user):
        valid = False
        errors.append({
            "path": ['plant_owner'],
            "message": "Username does not exist"
        })

    if valid:
        # on a valid submission, create plant
        new_plant = Plant(plant_type, plant_name, password, plant_health)
        message = "plant successfully registered"
        db.session.add(new_plant)
        db.session.commit()
        new_plant_dict = Schema_Plant.dump(new_plant)

        # create ownership/management plant link
        user_type = "plant_manager"
        user = current_user if plant_owner is None else plant_owner
        new_plant_link = Plant_link(user,
                                    new_plant_dict['plant_id'],
                                    user_type)
        db.session.add(new_plant_link)
        # update database
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
    """ 
    API method to get all plants visible to user

    Method: GET

    GET Parameters: None

    JWT: Required
    """
    errors = []
    current_user = get_jwt_identity()
    if username_exists(current_user):
        # return all plants if user is admin
        if get_jwt_claims()['role'] == "admin":
            plants = Plant.query.all()
            all_plants = Schema_Plants.dump(plants)
            for plant in all_plants:
                maintainer = get_plant_maintainer(plant["plant_id"])
                plant["maintainer"] = maintainer
            return jsonify(all_plants), 200
        else:
            plants = []
            list_of_plants = []
            # get all links between the user and other plants
            plant_link = Plant_link.query.filter_by(username=current_user).all()
            link = Schema_Plants_link.dump(plant_link)

            # extract plant_ids
            for x in link:
                if plant_exists(x["plant_id"]):
                    plants.append(x["plant_id"])
            # fetch all plants (and their details) with matching IDs
            for i in plants:
                plant = Plant.query.filter_by(plant_id=i).all()
                assert len(plant) > 0
                plant = plant[0]
                result = Schema_Plant.dump(plant)
                list_of_plants.append(result)
            # get plant maintainers
            for processed_plant in list_of_plants:
                maintainer = get_plant_maintainer(processed_plant["plant_id"])
                processed_plant["maintainer"] = maintainer
            # return plants
            return jsonify(list_of_plants), 200
    else:
        errors.append({
            "path": ['username'],
            "message": "incorrect token"
        })
        return jsonify({
            "errors": errors
        }), 400


@PLANT_API.route("/view_plant_details", methods=["GET"])
@jwt_required
def view_plant_details():
    """ 
    API method to get details for a plant

    Method: GET

    GET Parameters: plant_id

    JWT: Required
    """

    errors = []
    current_user = get_jwt_identity()
    plant_id = request.args.get('plant_id')
    # check plant exists and user can view it (read permission)
    if (plant_exists(plant_id) and
        get_plant_read_permission(current_user, plant_id)):
        # get plant information
        plant_info = get_plant(plant_id)
        # get latest history reading
        latest_reading = Plant_history.query.order_by(
            Plant_history.date_time.desc()).filter(
                Plant_history.plant_id == plant_id).limit(1)

        latest_reading = Schema_Plants_history.dump(latest_reading)
        if len(latest_reading) == 1:
            plant_info["latest_reading"] = latest_reading[0]
        else:
            plant_info["latest_reading"] = None
        
        # return password only if user can edit plant
        if not get_plant_edit_permission(current_user, plant_id):
            plant_info["password"] = None
            plant_info["access"] = "read"
        else:
            plant_info["access"] = "edit"
        
        # include the plant maintainer if there is one
        maintainer = get_plant_maintainer(plant_id)
        plant_info["maintainer"] = maintainer

        return jsonify(plant_info)

    else:
        errors.append({
            "path": ['username'],
            "message": "Invalid permission or plant does not exist"
        })
        return jsonify({
            "errors": errors
        }), 400


@PLANT_API.route("/get_plant_records", methods=["GET"])
@jwt_required
def get_recent_plant_record():
    """ 
    API method to get all plant history for a plant

    Method: GET

    GET Parameters: plant_id

    JWT: Required
    """

    errors = []
    current_user = get_jwt_identity()
    plant_id = request.args.get('plant_id')
    # check plant exists and user has read permission
    if (plant_exists(plant_id)
            and get_plant_read_permission(current_user, plant_id)):
        # get all history of plant in order of date (descending)
        result = Plant_history.query.order_by(
            Plant_history.date_time.desc()).filter(
                Plant_history.plant_id == plant_id)

        result = Schema_Plants_history.dump(result)
        # return error if no results
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
            # return success and history result
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
    """ 
    API method to delete plant from system

    Method: POST

    JSON Parameters: plant_id

    JWT: Required
    """

    errors = []
    current_user = get_jwt_identity()
    can_delete = True
    plant_id = request.json["plant_id"]
    # check plant exists and user has edit permission (admin or owner)
    if (plant_exists(plant_id)
        and get_plant_edit_permission(current_user, plant_id)):

        try:
            # get all histories linked to plant
            histories_unlink = Plant_history.query.filter_by(plant_id=plant_id)
            # remove plant_id from each history (safeguard on accidental plant data deletion)
            for history in histories_unlink:
                history.plant_id = None

            # get all plant links for the plant
            link_delete = Plant_link.query.filter_by(plant_id=plant_id)
            # delete each link
            for link in link_delete:
                db.session.delete(link)

            # delete plant itself
            plant_delete = Plant.query.get(plant_id)
            db.session.delete(plant_delete)

            # commit changes
            db.session.commit()

        # check if  a deletion error occurs
        except sql_alchemy_error.exc.UnmappedInstanceError:
            can_delete = False
            # roll back any changes
            db.session.rollback()
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
    """ 
    API method to update details for plant in system.

    Method: POST

    JSON Parameters: plant_id, plant_name, plant_type

    JWT: Required
    """

    errors = []
    successful_change = True
    current_user = get_jwt_identity()
    plant_id = request.json['plant_id']
    plant_name = request.json['plant_name']
    plant_type = request.json['plant_type']
    # check plant exists and user has edit permissions
    if (plant_exists(plant_id)
        and get_plant_edit_permission(current_user, plant_id)):

        plant_to_change = Plant.query.get(plant_id)
        # check each field is submitted (not empty) before updating
        if plant_name != "":
            plant_to_change.plant_name = plant_name

        if plant_type != "":
            # check plant type is valid
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
        # commit changes if successful
        db.session.commit()
        return jsonify("User Details Successfully Changed"), 201
    else:
        return jsonify({
            "errors": errors
        }), 403

@PLANT_API.route("/get_plant_members", methods=["GET"])
@jwt_required
def get_plant_members():
    """ 
    API method to get all members added to plant viewership.

    Method: GET

    JSON Parameters: plant_id

    JWT: Required
    """

    errors = []
    current_user = get_jwt_identity()
    plant_id = request.args.get('plant_id')

    # check current user has read permission on plant
    if get_plant_read_permission(current_user, plant_id):
        # get all links to plant
        plant_links = Plant_link.query.filter_by(plant_id=plant_id).all()
        links = Schema_Plants_link.dump(plant_links)
        user_ids = []
        # get user_ids from each link
        for link in links:
            if link["user_type"] == "plant_viewer":
                user_ids.append(link["username"])
        # return list of users
        return jsonify(user_ids), 200

    else:
        errors.append({
            "path": ['plant_id'],
            "message": "User does not have permission to view plant details."
        })
        return jsonify({
            "errors": errors
        }), 400

@PLANT_API.route("/get_plant_notifications", methods=["GET"])
@jwt_required
def get_plant_notifications():
    """ 
    API method to get notifications for unhealthy plants in system.

    Method: GET

    GET Parameters: None

    JWT: Required
    """

    errors = []
    current_user = get_jwt_identity()
    if username_exists(current_user):
        # admin list is all plants that are unhealthy and not allocated to an admin
        if get_jwt_claims()['role'] == "admin":
            # get all unhealthy plants
            plants = Plant.query.filter_by(plant_health="unhealthy").all()
            all_plants = Schema_Plants.dump(plants)
            
            # only append unhealthy plants that do not have a maintainer
            plants_in_need = []
            for plant in all_plants:
                maintainer = get_plant_maintainer(plant["plant_id"])
                if maintainer is None:
                    # notifications only need the ID and name of plant
                    plants_in_need.append({"plant_id" : plant["plant_id"], "plant_name" : plant["plant_name"]})
            return jsonify(plants_in_need), 200
        else:
            # return all user's unhealthy plants IDs and Names
            plants = []
            unhealthy_plants = []

            # get all IDs of plants linked to user
            plant_link = Plant_link.query.filter_by(username=current_user).all()
            links = Schema_Plants_link.dump(plant_link)

            for x in links:
                if plant_exists(x["plant_id"]):
                    plants.append(x["plant_id"])

            # get plants themselves
            for i in plants:
                plant = Plant.query.get(i)
                plant_details = Schema_Plant.dump(plant)
                # only need the ID and name for notifications
                if plant_details["plant_health"] == "unhealthy":
                    unhealthy_plants.append({"plant_id" : plant_details["plant_id"], "plant_name" : plant_details["plant_name"]})
            
            return jsonify(unhealthy_plants), 200
    else:
        errors.append({
            "path": ['username'],
            "message": "incorrect token"
        })
        return jsonify({
            "errors": errors
        }), 400