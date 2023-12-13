#!/usr/bin/env python

import asyncio
import websockets
from rlcard.games.limitholdem.game import LimitHoldemGame as Game
from pprint import pprint
import json

game_rooms = {}

def addGameRoom(game_id, players):
    # 1. Initialize Game
    game = Game()
    game.configure({'game_num_players' : players})
    state, current_player = game.init_game()
    game_rooms[game_id]  = game

    # 2. Display game data for game init & game actions
    print(f"Game Init. \n Current Player {current_player} Game \n State : {state}")

    return (game_id, current_player, state)

def addGameAction(game_id, action):
    game = game_rooms[game_id]
    state = game.step(action)

    return state


# 3. Create an Game Action socket to complete a game
async def action(websocket):
    client_req = await websocket.recv()
    req = json.loads(client_req)
    gid = req['game_uuid']
    data = req['data']
    # TODO: checkGameID from supabase function
    # if gid in game_rooms:
    if (req['action'] == True):

        state = addGameAction(gid, data['action'])
        resp = f"Current State {state}!"
    
        await websocket.send(resp)
    else:
        state_data = addGameRoom(gid, data["num_players"])
        resp = f"Room or Game ID: {state_data[0]}, Player ID: {state_data[1]} Current State {json.dumps(state_data[2])}!"

        await websocket.send(resp)
    print(f"Current Game Rooms: {game_rooms}")

async def main():
    async with websockets.serve(action, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())