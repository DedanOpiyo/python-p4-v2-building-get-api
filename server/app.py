# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# start building your API here

@app.route('/games')
def games():

    games = [game.to_dict() for game in Game.query.all()] # Make more succinct # Other than looping and appending

    response = make_response(
        games, # jsonify accepts list or dictionaries as arguments # If we do jsonify(games) - we can exclude {"Content-Type": "application/json"} - json header
        200,
        {"Content-Type": "application/json"} # By default - Flask sets response header to - Content-Type: text/html # We have however, 'jsonified' games above
    )

    return response

@app.route('/games/<int:game_id>')
def game_by_game_i(game_id):
    game = Game.query.filter_by(id = game_id).first() # Single = for filter_by # field names directly as keywords, only simple equality comparisons.
    # game = Game.query.filter(Game.id == game_id).first() # expects SQL expressions # model attributes and comparison operators like ==, >, etc.

    if not game:
        return make_response({"error": f"No game matches the specified id: {game_id}"}, 404)

    game_dict = game.to_dict()

    response = make_response(game_dict, 200)
    return response

@app.route('/games/users/<int:id>')
def game_users_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    # use association proxy to get users for a game
    users = [user.to_dict(rules=("-reviews",)) for user in game.users] # user.to_dict(rules=("-reviews",)) # Parameters .to_dict() takes ?

    response = make_response(
        users,
        200
    )

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)

