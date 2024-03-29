import numpy as np
import pymysql
from flask import Flask
from flask import Flask , redirect , url_for, render_template , request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask_api_user import USER_API
from flask_api_plant import PLANT_API
from flask_api_iot import IOT_API
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
# JWT configuration
# TODO real key
JWT_API_KEY = "sup"
app.config['JWT_SECRET_KEY'] = JWT_API_KEY

# SQL configuration
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size" : 20,
    "pool_recycle": 15,
    "max_overflow" : -1
}
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 15
# app.config['SQLALCHEMY_MAX_OVERFLOW'] = -1
# app.config["SQLALCHEMY_POOL_SIZE"] = 20

jwt = JWTManager(app)
CORS(app)

pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

# database information
HOST = "34.87.205.64"
USER = "root"
PASSWORD = "reza123"
DATABASE = "smart_plant"
socket_path = "/cloudsql"
cloud_sql_instance_name = "smart-plant-1:australia-southeast1:smartplant-dbms"


# deployed configuration, uncomment this for deployed version
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@/{}?unix_socket={}/{}".format(USER, PASSWORD, DATABASE,
                                                                                               socket_path,
                                                                                               cloud_sql_instance_name)

# LOCAL configuration, uncomment this for local running
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(app)
# register APIs to application
app.register_blueprint(USER_API)
app.register_blueprint(PLANT_API)
app.register_blueprint(IOT_API)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

# run API at localhost:8080
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
