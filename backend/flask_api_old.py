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



# DEBUGGING NEED TO DELETE 
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



