# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import math
import random
import typing
from minimax import alphabeta


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "novynova",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    state = parse_game_state(game_state)
    best_move = get_best_move(state)
    print(f"MOVE {game_state['turn']}: {best_move}")
    return {"move": best_move}

def parse_game_state(data):
    parsed_state = {
        "my_snake": {
            "head": data["you"]["body"][0],
            "body": data["you"]["body"],
            "health": data["you"]["health"]
        },
        "board": {
            "width": data["board"]["width"],
            "height": data["board"]["height"],
            "food": data["board"]["food"],
            "snakes": data["board"]["snakes"]
        },
        "turn": data["turn"]
    }
    return parsed_state

def get_best_move(state):
    best_move = None
    best_value = -math.inf

    for move in get_possible_moves(state):
        new_state = simulate_move(state, move)
        move_value = alphabeta(new_state, depth=3, alpha=-math.inf, beta=math.inf, maximizing_player=False)
        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move

def get_possible_moves(state):
    # Gib alle möglichen Züge für die Schlange zurück (z.B. ["up", "down", "left", "right"])
    return ["up", "down", "left", "right"]

def simulate_move(state, move):
    # Simuliere einen Zug und gib den neuen Zustand zurück
    new_state = state.copy()
    head = new_state['you']['body'][0]
    new_head = head.copy()
    
    if move == "up":
        new_head['y'] += 1
    elif move == "down":
        new_head['y'] -= 1
    elif move == "left":
        new_head['x'] -= 1
    elif move == "right":
        new_head['x'] += 1
        
    new_state['you']['body'].insert(0, new_head)  # Neue Kopfposition hinzufügen
    new_state['you']['body'].pop()  # Letztes Segment entfernen, wenn die Schlange nicht wächst

    # Weitere Logik hier, z.B. Wachstum bei Futter, Kollisionen etc.
    
    return new_state

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
