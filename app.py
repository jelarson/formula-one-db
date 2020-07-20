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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Scores(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    highScore = db.Column(db.String(4), nullable=False)


    def __init__(self, name, highScore):
        self.name = name
        self.highScore = highScore

class ScoreSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'highScore')

score_schema = ScoreSchema()
scores_schema = ScoreSchema(many=True)

@app.route('/', methods=["GET"])
def home():
    return "<h1>Connect 4 high scores</h1>"

@app.route('/wakeup', methods=['POST'])
def auth_user():
  return str("I am awake!")

@app.route('/score', methods=['POST'])
def add_score():
    name = request.json['name']
    highScore = request.json['highScore']


    new_score = Scores(name, highScore)

    db.session.add(new_score)
    db.session.commit()

    score = Scores.query.get(new_score.id)
    return score_schema.jsonify(score)


@app.route('/scores', methods=["GET"])
def get_scores():
    all_scores = Scores.query.all()
    result = scores_schema.dump(all_scores)

    return jsonify(result)


@app.route('/score/<id>', methods=['GET'])
def get_score(id):
    score = Score.query.get(id)

    result = score_schema.dump(score)
    return jsonify(result)


@app.route('/score/<id>', methods=['PATCH'])
def update_user(id):
    score = Scores.query.get(id)

    new_name = request.json['name']
    new_highScore = request.json['highScore']

    user.name = new_name
    user.highScore = new_highScore

    db.session.commit()
    return score_schema.jsonify(score)

@app.route('/score/<id>', methods=['DELETE'])
def delete_score(id):
    record = Score.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Item deleted')


if __name__ == "__main__":
    app.debug = True
    app.run()