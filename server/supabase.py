from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def updateGame(game, game_uuid=None, update=False):
    game_data = None
    data = {
        "seed": game.random_seed,
        "game_pointer": game.game_pointer,
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
        game_data = (
            supabase.table("limitholdem").update(data).eq("id", game_uuid).execute()
        )
    else:
        game_data = supabase.table("limitholdem").insert(data).execute()

    return game_data.data[0]


def updatePlayers(game, game_uuid=None, update=False):
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
            response = (
                supabase.table("player")
                .update(data)
                .eq("game_uuid", game_uuid)
                .execute()
            )
        else:
            data["game_uuid"] = game_uuid
            response = supabase.table("player").insert(data).execute()
        if response.data[0]:
            players_data.insert(index, response.data[0])
    return players_data


def updateRound(game, game_uuid=None, update=False):
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
        round_data = (
            supabase.table("round").update(data).eq("game_uuid", game_uuid).execute()
        )
    else:
        data["game_uuid"] = game_uuid
        round_data = supabase.table("round").insert(data).execute()

    return round_data.data[0]


def getGame(game_uuid):
    response = supabase.table("limitholdem").select("*").eq("id", game_uuid).execute()
    return response.data[0]


def getPlayers(game_uuid):
    response = supabase.table("player").select("*").eq("game_uuid", game_uuid).execute()
    return response.data


def getPlayer(player_id):
    response = supabase.table("player").select("*").eq("id", player_id).execute()
    return response.data[0]


def getRound(game_uuid):
    response = supabase.table("round").select("*").eq("game_uuid", game_uuid).execute()
    return response.data[0]
