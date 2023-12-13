#!/usr/bin/env python

import asyncio
import websockets
import json
# action = input("What's your Action? ")
GAME_EVENT = {
    "game_uuid" : 47,
    "action" : True,
    "data" : {
        "action" : "call",
        "num_players" : 11,
    },
}
async def action():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:

        await websocket.send(json.dumps(GAME_EVENT))
        print(f">>> {GAME_EVENT}")

        resp = await websocket.recv()
        print(f"<<< {resp}")

if __name__ == "__main__":
    asyncio.run(action())