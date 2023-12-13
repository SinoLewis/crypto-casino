from pprint import pprint
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import numpy as np
# DEV Import of modified rlcard package
import os
import sys

load_dotenv()
sys.path.append(os.getenv("RLCARD_DEV"))
from rlcard.games.limitholdem.game import LimitHoldemGame as Game
from rlcard.utils.supabase import getGame, getPlayers, getRound, getPlayer

app = Flask(__name__)


def get_random_seed():
    # Minimum and maximum seed values
    min_seed = 0
    max_seed = 2**32 - 1
    # Generate a random seed within the valid range
    random_seed = np.random.randint(min_seed, max_seed)
    return random_seed


# 1. GAME ADMIN API's
@app.route("/limitholdem/game", methods=["POST"])
def createRoomGame():
    game = Game(
        num_players=request.json["num_players"],
        update_db=False,
        random_seed=get_random_seed(),
        small_blind=request.json["small_blind"],
    )
    db_data = game.get_game()

    # TODO: Try return Game object
    # return jsonify({"game": game, "players": game.players, "round": game.round})
    return jsonify(
        {
            "game": db_data["game_data"],
            "players": db_data["players_data"],
            "round": db_data["round_data"],
        }
    )


@app.route("/limitholdem/game/<string:game_id>", methods=["GET"])
def getRoomGame(game_id):
    game_db = getGame(game_id)
    players_db = getPlayers(game_id)
    round_db = getRound(game_id)

    return jsonify(
        {
            "game": game_db if game_db else None,
            "players": players_db if players_db else None,
            "round": round_db if round_db else None,
        }
    )


@app.route("/limitholdem/game", methods=["PUT"])
def updateRoomGame():
    game_id = request.json["id"]
    action = request.json["action"]
    seed = request.json["seed"]

    game = Game(
        update_db=True,
        random_seed=seed,
    )
    game.game_uuid = game_id
    
    game.get_game()

    db_data = game.step(action)

    return jsonify(
        {
            "game": db_data["game_data"],
            "players": db_data["players_data"],
            "round": db_data["round_data"],
        }
    )


# 2. Player API's
@app.route("/limitholdem/player/<string:player_id>", methods=["GET"])
def getPlayerGame(player_id):
    player_db = getPlayer(player_id)
    game_db = getGame(player_db["game_uuid"])
    round_db = getRound(player_db["game_uuid"])

    return jsonify(
        {
            "game": game_db if game_db else None,
            "player": player_db if player_db else None,
            "round": round_db if round_db else None,
        }
    )


@app.route("/limitholdem/player", methods=["PUT"])
def updatePlayerAction():
    game_id = request.json["game_uuid"]
    action = request.json["action"]

    game = Game(
        update_db=True,
    )
    game.game_uuid = game_id
    db_data = game.get_game()
    player = db_data["game_pointer"]

    db_data = game.step(action)

    return jsonify(
        {
            "game": db_data["game_data"],
            "player": db_data["players_data"][player],
            "round": db_data["round_data"],
        }
    )


@app.route("/limitholdem/game/test", methods=["POST"])
def testGame():
    game = Game(
        num_players=request.json["num_players"],
        update_db=True,
        random_seed=request.json["seed"],
        small_blind=request.json["small_blind"],
    )

    game.game_uuid = request.json["game_id"]

    db_data = game.get_game()

    game_round_state = {}

    # Pre-flop Round to get Flop
    for index, player in enumerate(db_data['players_data']):
        print("Index: ", index)
        if index == game.num_players - 1:
            game.step("check")
        else:
            game.step("call")
            # print("Index: ", index)
        state = game.get_state(index)
        print(f"Player {index}, Pre-flop Action Played")
    game_round_state["Pre-flop"] = state
    # Flop Round to get River
    for index, player in enumerate(game.players):
        # print("Index: ", index)
        game.step("check")
        state = game.get_state(index)
        print(f"Player {index}, Flop Action Played")
    game_round_state["Flop"] = state

    # River round to get Turn
    for index, player in enumerate(game.players):
        print("Index: ", index)
        if index == 0:
            game.step("raise")
        else:
            game.step("call")
            # print("Index: ", index)
        state = game.get_state(index)
        print(f"Player {index}, River Action Played")
    game_round_state["River"] = state

    return jsonify(game_round_state)


if __name__ == "__main__":
    print("RLCard Server starting...")
    app.run(debug=True)

# def get_current_player(seed):
#     game = Game(random_seed=seed)
#     game.configure({'game_num_players' : 9})

#     state, current_player = game.init_game() #<class 'dict'>

#     print(f"{current_player}' nth Player State:\n")
#     pprint(state)

# def test_same_obj(seed):
#     get_current_player(seed)
#     get_current_player(seed)

# TEST: Get current player from game seed
# get_current_player(random_seed)

# TEST: Check two same objects current player
# test_same_obj(random_seed)
