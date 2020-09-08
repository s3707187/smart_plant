from flask import Flask
from flask import Flask , redirect , url_for, render_template , request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from backend.flask_api import api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = "sup"

jwt = JWTManager(app)
CORS(app)


HOST = "34.87.205.64"
USER = "root"
PASSWORD = "reza123"
DATABASE = "smart_plant"
socket_path = "/cloudsql"
cloud_sql_instance_name = "smart-plant-1:australia-southeast1:smartplant-dbms"
# <cloud_sql_instance_name> = <PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>


#mysql+pymysql://<USER>:<PASSWORD>@/<DATABASE>?unix_socket=<socket_path>/<cloud_sql_instance_name>
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@/{}?unix_socket={}/{}".format(USER, PASSWORD, DATABASE,
                                                                                              socket_path,
                                                                                              cloud_sql_instance_name)

#LOCAL
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(app)
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
