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
        "author": "Gruppe 1",  # TODO: Your Battlesnake Username
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
    best_move = []
    best_value = -math.inf

    for move in get_possible_moves(state):
        new_state = simulate_move(state, move)
        move_value = alphabeta(new_state, depth=3, alpha=-math.inf, beta=math.inf, maximizing_player=True)
        if move_value > best_value:
            best_value = move_value
            best_move = [move]
        elif move_value == best_value:
            best_move.append(move)

    return random.choice(best_move) if best_move else None

def get_possible_moves(state):                          #filtert jetzt die deadly moves raus
    possible_moves = ["up", "down", "left", "right"]
    safe_moves = []

    for move in possible_moves:
        new_state = simulate_move(state, move)
        if not check_collision(new_state):
            safe_moves.append(move)

    return safe_moves

def simulate_move(state, move):
    # Copy the current state to avoid mutating the original
    new_state = state.copy()
    new_state["my_snake"] = state["my_snake"].copy()
    new_state["my_snake"]["body"] = state["my_snake"]["body"].copy()

    # Update the head position based on the move
    new_head_position = new_state["my_snake"]["head"].copy()
    if move == "up":
        new_head_position['y'] += 1
    elif move == "down":
        new_head_position['y'] -= 1
    elif move == "left":
        new_head_position['x'] -= 1
    elif move == "right":
        new_head_position['x'] += 1

    # Move the body
    new_body = [new_head_position] + new_state["my_snake"]["body"][:-1]
    new_state["my_snake"]["head"] = new_head_position
    new_state["my_snake"]["body"] = new_body

    if check_collision(new_state):
        
        return None
    # Return the new state
    return new_state

def check_collision(state):
    head = state['my_snake']['head']#[0]
    body = state['my_snake']['body']#[1:]  # Der Kopf wird nicht in den Körper einbezogen
    board_width = state['board']['width']
    board_height = state['board']['height']
   # opponents = state['board']['snakes']
    
    # Kollision mit der Wand
    if head['x'] < 0 or head['x'] >= board_width or head['y'] < 0 or head['y'] >= board_height:
        return True
    
    # Kollision mit dem eigenen Körper
    if head in body[1:]:
        return True
    
    # Kollision mit anderen Schlangen
    for snake in state['board']['snakes']:
        if head in snake['body']:
            return True
    
    return False

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
