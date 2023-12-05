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
    max_seed =  2**32 - 1
    # Generate a random seed within the valid range
    random_seed = np.random.randint(min_seed, max_seed)
    return random_seed

# @app.route('/game/limitholdem>', methods=['POST'])
def createGame():
    game = Game(num_players=request.json['num_players'])
    state, current_player = game.init_game()

    response = supabase.table('limitholdem').insert({
        "seed": get_random_seed(),
        "current_player_id": current_player,
        "small_blind": game.small_blind,
        "is_over": game.is_over(),
        "payoffs": game.get_payoffs()
        "allowed_raise_num": game.allowed_raise_num,
        "num_actions": game.get_num_actions()
        "num_players": game.num_players
        }
    ).execute()


    game_data = response["data"][0]
    
    player_data = []
    for player, index in enumerate(game.players):
        state = game.get_state(player.player_id)
        response = supabase.table('player').insert({
            "player_id": player.player_id,
            "status": player.status.value,
            "game_uuid": game_data["id"],
            "my_chips": state['my_chips'],
            "hand": state['hand'],
            "public_cards": state['public_cards'],
            "all_chips": state['all_chips'],
            "legal_actions": state['legal_actions'],        
        }).execute()   
        
        player_data.insert(index, response["data"][0])

    
    round_data = supabase.table('round').insert({
        "game_uuid": game.id,
        "player_folded": game.round.player_folded,
        "have_raised": game.round.have_raised,
        "not_raise_num": game.round.not_raise_num,
        "raised": game.round.raised

    return jsonify({"game" : game_data, "players" : player_data, "round" : round})

# @app.route('/game/limitholdem/<int:game_id>')
def getGame(game_id):
    game_data = supabase.table('limitholdem').select("*").eq('id', game_id).execute()
    players_data = supabase.table('player').select("*").eq('game_id', game_id).execute()
    round_data = supabase.table('round').select("*").eq('game_id', game_id).execute()

    return jsonify({"game" : game_data, "players" : player_data, "round" : round})

# @app.route('/game/limitholdem', methods=['PUT'])
def updateGame():
    game_id = request.json['id']
    action = request.json['action']

    game_data = supabase.table('limitholdem').select("*").eq('id', game_id).execute()
    players_data = supabase.table('player').select("*").eq('game_id', game_id).execute()
    round_data = supabase.table('round').select("*").eq('game_id', game_id).execute()

    game = Game(num_players=game.num_players, random_seed=game_data['seed'])
    state, current_player = game.init_game()

    game.game_pointer = game_data['current_player_id']
    game.small_blind = game_data['small_blind']
    game.big_blind = game.small_blind * 2
    
    return jsonify()

if __name__ == '__main__':
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

# @app.route('/')
# def hello_world():
#     return 'Hello, Friend! Welcome to RLCard Server'

# @app.route('/api/submit', methods=['POST'])
# def submit_data():
#     data = request.get_json()
#     # Do something with the data (e.g., process it, return a response)
#     return jsonify({'message': 'Data received successfully'})
