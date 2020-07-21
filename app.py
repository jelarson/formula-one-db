from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from environs import Env
import psycopg2
import os

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)

env = Env()
env.read_env()
DATABASE_URL = env("DATABASE_URL")

basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#     os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Drivers(db.Model):
    __tablename__ = "drivers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team = db.Column(db.String(100), nullable=False)


    def __init__(self, name, team):
        self.name = name
        self.team = team

class DriverSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'team')

driver_schema = DriverSchema()
drivers_schema = DriverSchema(many=True)

@app.route('/', methods=["GET"])
def home():
    return "<h1>Formula One Drivers - 2020</h1>"

@app.route('/wakeup', methods=['POST'])
def auth_user():
  return str("I am awake!")

@app.route('/driver', methods=['POST'])
def add_driver():
    name = request.json['name']
    team = request.json['team']


    new_driver = Drivers(name, team)

    db.session.add(new_driver)
    db.session.commit()

    driver = Drivers.query.get(new_driver.id)
    return driver_schema.jsonify(driver)


@app.route('/drivers', methods=["GET"])
def get_drivers():
    all_drivers = Drivers.query.all()
    result = drivers_schema.dump(all_drivers)

    return jsonify(result)


@app.route('/driver/<id>', methods=['GET'])
def get_driver(id):
    driver = Driver.query.get(id)

    result = driver_schema.dump(driver)
    return jsonify(result)


@app.route('/driver/<id>', methods=['PATCH'])
def update_driver(id):
    driver = Drivers.query.get(id)

    new_name = request.json['name']
    new_team = request.json['team']

    user.name = new_name
    user.team = new_team

    db.session.commit()
    return driver_schema.jsonify(driver)

@app.route('/driver/<id>', methods=['DELETE'])
def delete_driver(id):
    record = Driver.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Item deleted')


if __name__ == "__main__":
    app.debug = True
    app.run()