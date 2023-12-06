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
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)


def get_random_seed():
    # Minimum and maximum seed values
    min_seed = 0
    max_seed = 2 ** 32 - 1
    # Generate a random seed within the valid range
    random_seed = np.random.randint(min_seed, max_seed)
    return random_seed

def updateGameSupa(game, game_uuid=None, update=False):
    game_data = None
    data = {
        "seed": game.random_seed,
        "current_player_id": game.game_pointer,
        "small_blind": game.small_blind,
        "public_cards": game.public_cards,
        "is_over": game.is_over(),
        "history_raise_nums": [0 for _ in range(4)],
        # TODO: If Error return null
        # "payoffs": game.get_payoffs() if game.get_payoffs() else None,
        "allowed_raise_num": game.allowed_raise_num,
        "num_actions": game.get_num_actions(),
        "num_players": game.num_players,
    }
    if update:
        data["updated_at"] = "now()"
        game_data = supabase.table('limitholdem').update(data).eq('id', game_uuid).execute()
    else:
        game_data = supabase.table("limitholdem").insert(data).execute()

    return game_data.data[0]

def updatePlayersSupa(game, players_db=None, game_uuid=None, update=False):
    # NB: update False = new record
    players_data = []
    for index, player in enumerate(game.players):
        state = game.get_state(index)
        print(f"PLAYER STATUS: {player.status}")
        data = {
            "player_id": player.player_id,
            # "status": player.status.value,
            "game_uuid": game_uuid,
            "my_chips": state["my_chips"],
            "hand": state["hand"],
            "all_chips": state["all_chips"],
            "legal_actions": state["legal_actions"],
        }
        if update:
            data["updated_at"] = "now()"
            response = supabase.table('player').update(data).eq('id', players_db[index]['id']).execute()
        else:
            data["game_uuid"] = game_uuid
            response = supabase.table("player").insert(data).execute()

        players_data.insert(index, response.data[0])
    return players_data

def updateRoundSupa(game, game_uuid=None, update=False):
    round_data = None
    data = {
        "game_uuid": game_uuid,
        "player_folded": game.round.player_folded,
        "have_raised": game.round.have_raised,
        "not_raise_num": game.round.not_raise_num,
        "raised": game.round.raised,
    }
    if update:
        data["updated_at"] = "now()"
        round_data = supabase.table('round').update(data).eq('game_uuid', game_uuid).execute()
    else:
        data["game_uuid"] = game_uuid
        round_data = supabase.table("round").insert(data).execute()

    return round_data.data[0]


@app.route("/game/limitholdem", methods=["POST"])
def createGame():
    game = Game(
        num_players=request.json["num_players"],
        random_seed=get_random_seed(),
        small_blind=request.json["small_blind"],
    )
    game.init_game()

    game_data = updateGameSupa(game)
    players_data = updatePlayersSupa(game, game_uuid=game_data['id'])
    round_data = updateRoundSupa(game, game_uuid=game_data['id'])

    return jsonify({"game": game_data, "players": players_data, "round": round_data})


@app.route("/game/limitholdem/<string:game_id>", methods=["GET"])
def getGame(game_id):
    game_data = supabase.table("limitholdem").select("*").eq("id", game_id).execute()
    players_data = (
        supabase.table("player").select("*").eq("game_uuid", game_id).execute()
    )
    round_data = supabase.table("round").select("*").eq("game_uuid", game_id).execute()

    print(round_data.data)
    return jsonify(
        {
            "game": game_data.data[0] if game_data.data else None,
            "players": players_data.data if players_data.data else None,
            "round": round_data.data[0] if round_data.data else None,
        }
    )

@app.route("/game/limitholdem", methods=["PUT"])
def updateGame():
    game_id = request.json["id"]
    action = request.json["action"]

    game_data = (
        supabase.table("limitholdem").select("*").eq("id", game_id).execute().data[0]
    )
    players_data = (
        supabase.table("player").select("*").eq("game_uuid", game_id).execute().data
    )
    round_data = (
        supabase.table("round").select("*").eq("game_uuid", game_id).execute().data[0]
    )

    game = Game(
        num_players=game_data["num_players"],
        random_seed=game_data["seed"],
        small_blind=game_data["small_blind"],
    )
    game.init_game()
    game.configure(
        game=game_data,
        players=players_data,
        round=round_data,
    )

    game.step(action)

    # TODO: Supabase Update & Insert logic
    game_data = updateGameSupa(game, game_uuid=game_data["id"], update=True)
    players_data = updatePlayersSupa(game, players_db=players_data, game_uuid=game_data["id"], update=True)
    round_data = updateRoundSupa(game, game_uuid=game_data["id"], update=True)

    return jsonify(
        {
            "game": game_data if game_data else None,
            "players": players_data if players_data else None,
            "round": round_data if round_data else None,
        }
    )

@app.route("/game/limitholdem/test", methods=["GET"])
def testGame():
    game_id = "e96e99a3-f982-4b4e-a102-e02083a05666"
    game_data = (
        supabase.table("limitholdem").select("*").eq("id", game_id).execute().data[0]
    )
    players_data = (
        supabase.table("player").select("*").eq("game_uuid", game_id).execute().data
    )
    round_data = (
        supabase.table("round").select("*").eq("game_uuid", game_id).execute().data[0]
    )

    game = Game(
        num_players=game_data["num_players"],
        random_seed=game_data["seed"],
        small_blind=game_data["small_blind"],
    )
    game.init_game()
    game.configure(
        game=game_data,
        players=players_data,
        round=round_data,
    )
    
    game_round_state = {}

    # Pre-flop Round to get Flop
    for index, player in enumerate(game.players):
        print("Index: ", index)
        if(index == game.num_players-1):
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
        if(index == 0):
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
