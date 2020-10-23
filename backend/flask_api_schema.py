from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import current_app as app
from sqlalchemy import func, ForeignKey, desc
import datetime

db = SQLAlchemy()
ma = Marshmallow()


# User model
class User(db.Model):
    __tablename__ = "User"
    username = db.Column(db.VARCHAR(100), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.VARCHAR(100), nullable=False)
    first_name = db.Column(db.VARCHAR(100), nullable=False)
    last_name = db.Column(db.VARCHAR(100), nullable=False)
    email  = db.Column(db.VARCHAR(255), nullable=False)
    account_type  = db.Column(db.VARCHAR(100), nullable=False)

    def __init__(self, username, password, first_name, last_name, email, account_type):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.account_type = account_type

# Plant model
class Plant(db.Model):
    __tablename__ = "Plant"
    plant_id = db.Column(db.Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    plant_type = db.Column(db.VARCHAR(100), nullable=False) #, ForeignKey('Plant_type.plant_type')
    plant_name = db.Column(db.VARCHAR(100), nullable=False)
    password = db.Column(db.VARCHAR(100), nullable=False)
    plant_health = db.Column(db.VARCHAR(100), nullable=False)

    def __init__(self, plant_type, plant_name, password, plant_health):
        self.plant_type = plant_type
        self.plant_name = plant_name
        self.password = password
        self.plant_health = plant_health

# Plant_type model
class Plant_type(db.Model):
    __tablename__ = "Plant_type"
    plant_type = db.Column(db.VARCHAR(100), nullable=False, unique=True, primary_key=True)
    temp_min = db.Column(db.Float, nullable=False)
    temp_max = db.Column(db.Float, nullable=False)
    humidity_min = db.Column(db.Float, nullable=False)
    humidity_max = db.Column(db.Float, nullable=False)
    light_min = db.Column(db.Float, nullable=False)
    light_max = db.Column(db.Float, nullable=False)
    moisture_min = db.Column(db.Float, nullable=False)
    moisture_max = db.Column(db.Float, nullable=False)

    def __init__(self, plant_type, temp_min, temp_max, humidity_min, humidity_max, light_min, light_max, moisture_min, moisture_max):
        self.plant_type = plant_type
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.humidity_min = humidity_min
        self.humidity_max = humidity_max
        self.light_min = light_min
        self.light_max = light_max
        self.moisture_min = moisture_min
        self.moisture_max = moisture_max

# Plant_history model
class Plant_history(db.Model):
    __tablename__ = "Plant_history"
    history_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True) #, ForeignKey('Plant.plant_id')
    plant_id = db.Column(db.Integer, nullable=True)
    date_time = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    light  = db.Column(db.Float, nullable=False)
    moisture  = db.Column(db.Float, nullable=False)

    def __init__(self,plant_id,date_time, temperature, humidity, light, moisture):
        # self.history_id = history_id
        self.plant_id = plant_id
        self.date_time = date_time
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.moisture = moisture

# Plant_history model
class Plant_link(db.Model):
    __tablename__ = "Plant_link"
    username = db.Column(db.VARCHAR(100), nullable=False, primary_key=True) #primary_key=True #, ForeignKey('User.username')
    plant_id = db.Column(db.Integer, nullable=False, primary_key=True) #, ForeignKey('Plant.plant_id')
    user_type = db.Column(db.VARCHAR(100), nullable=False)


    def __init__(self, username, plant_id, user_type):
        self.username = username
        self.plant_id = plant_id
        self.user_type = user_type


class User_Schema(ma.Schema):

    def __init__(self, strict=True, **kwargs):
        super(User_Schema, self).__init__(**kwargs)

    class Meta:
        # Fields to expose
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'account_type')

class Plant_Schema(ma.Schema):

    def __init__(self, strict=True, **kwargs):
        super(Plant_Schema, self).__init__(**kwargs)

    class Meta:
        # Fields to expose
        fields = ('plant_id', 'plant_type', 'plant_name', 'plant_health', 'password')

class Plant_type_Schema(ma.Schema):

    def __init__(self, strict=True, **kwargs):
        super(Plant_type_Schema, self).__init__(**kwargs)

    class Meta:
        # Fields to expose
        fields = ('plant_id', 'temp_min', 'temp_max', 'humidity_min', 'humidity_max',
                  'light_min', 'light_max', 'moisture_min', 'moisture_max')

class Plant_history_Schema(ma.Schema):

    def __init__(self, strict=True, **kwargs):
        super(Plant_history_Schema, self).__init__(**kwargs)

    class Meta:
        # Fields to expose
        fields = ('plant_id', 'date_time', 'temperature', 'humidity', 'light', 'moisture')

class Plant_link_Schema(ma.Schema):

    def __init__(self, strict=True, **kwargs):
        super(Plant_link_Schema, self).__init__(**kwargs)

    class Meta:
        # Fields to expose
        fields = ('username', 'plant_id', 'user_type')

Schema_User = User_Schema()
Schema_Users = User_Schema(many=True)

Schema_Plant = Plant_Schema()
Schema_Plants = Plant_Schema(many=True)

Schema_Plant_type = Plant_type_Schema()
Schema_Plants_type = Plant_type_Schema(many=True)

Schema_Plant_history = Plant_history_Schema()
Schema_Plants_history = Plant_history_Schema(many=True)

Schema_Plant_link = Plant_link_Schema()
Schema_Plants_link = Plant_link_Schema(many=True)
