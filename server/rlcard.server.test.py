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


# 1. Create Peristent game API handler
    # 1.1. Enum State in DB (the class main return data type)
        # 1. Seed int must be unique to a unique game uuid
        # 2. move Player.game_id from Game.players_ids: int[]
        # 3. move Round.game_id from Round.round_ids: int[]
        # 4. is_over: bool
    # 1.2. Supa Auth CRUD DB's actions handlers where needed
        # 1. get_current_player
    # 1.3 (PASS) Test if same Game object are equal to duplicate obj of unique seed
# 2. Create Rel DB's of games instance objects
    # 2.1. Each DB w/ Relation to Game DB and other same child DB's
    # 2.2. Enum State & Auth CRUD DB's actions where needed
    # 2.3. Test if same Game child Objects are equal to duplicate obj of unique seed

def get_random_seed():
    # Minimum and maximum seed values
    min_seed = 0
    max_seed =  2**32 - 1
    # Generate a random seed within the valid range
    random_seed = np.random.randint(min_seed, max_seed)
    return random_seed

random_seed = get_random_seed()
print(f"BEFORE RAND SEED: {random_seed}")

def get_current_player(seed):
    game = Game(random_seed=seed)
    game.configure({'game_num_players' : 9})

    state, current_player = game.init_game() #<class 'dict'>

    print(f"{current_player}' nth Player State:\n")
    pprint(state)

def test_same_obj(seed):
    get_current_player(seed)
    get_current_player(seed)

# API: Get current player from game seed
# get_current_player(random_seed)

# TEST: Check two same objects current player
test_same_obj(random_seed)



# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, Friend! Welcome to RLCard Server'

# @app.route('/api/submit', methods=['POST'])
# def submit_data():
#     data = request.get_json()
#     # Do something with the data (e.g., process it, return a response)
#     return jsonify({'message': 'Data received successfully'})


# if __name__ == '__main__':
#     print("RLCard Server starting...")
#     app.run(debug=True)
