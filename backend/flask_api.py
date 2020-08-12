from flask_api_schema import *
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app
from sqlalchemy import func, ForeignKey, desc


api = Blueprint("api", __name__)

@api.route("/users", methods=["GET"])
def getUsers():
    user = User.query.all()
    result = Schema_Users.dump(user)
    return jsonify(result)
