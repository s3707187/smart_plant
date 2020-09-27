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
import argparse


app = Flask(__name__)
# TODO real key
app.config['JWT_SECRET_KEY'] = "sup"

jwt = JWTManager(app)
CORS(app)

pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

HOST = "34.87.205.64"
USER = "root"
PASSWORD = "reza123"
DATABASE = "smart_plant"
socket_path = "/cloudsql"
cloud_sql_instance_name = "smart-plant-1:australia-southeast1:smartplant-dbms"
# <cloud_sql_instance_name> = <PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>

TEST_DATABASE = "testing_smart_plant"

# mysql+pymysql://<USER>:<PASSWORD>@/<DATABASE>?unix_socket=<socket_path>/<cloud_sql_instance_name>
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@/{}?unix_socket={}/{}".format(USER, PASSWORD, DATABASE,
                                                                                            #   socket_path,
                                                                                            #   cloud_sql_instance_name)

#LOCAL
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(app)
app.register_blueprint(USER_API)
app.register_blueprint(PLANT_API)
app.register_blueprint(IOT_API)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
    # testing argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action='store_true',
                            default=False, help="Set database to testing DB.")
    args = vars(parser.parse_args())
    
    if args["test"]:
        # set database to testing database
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, TEST_DATABASE)
        from flask_api_shutdown import SHUTDOWN_API
        # bring in the shutdown route
        app.register_blueprint(SHUTDOWN_API)

    app.run(host='127.0.0.1', port=8080, debug=True)
    exit()
