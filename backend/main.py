from flask import Flask
from flask import Flask , redirect , url_for, render_template , request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask_api import api, db

app = Flask(__name__)

HOST = "34.87.205.64"
USER = "root"
PASSWORD = "reza123"
DATABASE = "smart_plant"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(app)
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
