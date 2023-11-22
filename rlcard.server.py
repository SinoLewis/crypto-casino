# app.py
from flask import Flask, jsonify, request
from rlcard.games.limitholdem.game import LimitHoldemGame as Game

app = Flask(__name__)

# TODO: RLcard Casino Game classed API DB's
# 1. Game has super one to many relations to other Classes
# 2. Player
# 3. Dealer
# 4. Judger
# 5. Round

@app.route('/')
def hello_world():
    return 'Hello, Friend! Welcome to RLCard Server'

@app.route('/api/submit', methods=['POST'])
def submit_data():
    data = request.get_json()
    # Do something with the data (e.g., process it, return a response)
    return jsonify({'message': 'Data received successfully'})


if __name__ == '__main__':
    print("RLCard Server starting...")
    app.run(debug=True)
