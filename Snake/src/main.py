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

# Code by
# Dominic Foraschick (Matrikelnummer: 222200429)
# Tommy Stettin (Matrikelnummer: 221200375)
# Johannes Peters (Matrikelnummer: 218205404)
# Laurin Haase (Matrikelnummer: 217204840) 

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Gruppe 1",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }
def start(game_state: typing.Dict):
    print("GAME START")

def end(game_state: typing.Dict):
    print("GAME OVER\n")

def move(game_state: typing.Dict) -> typing.Dict:
    state = parse_game_state(game_state)
    best_move = get_best_move(state)
    print(f"MOVE {game_state['turn']}: {best_move}")
    return {"move": best_move}

def parse_game_state(data):
    # Formartiert die Daten in ein für uns nutzbares Format
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
    # Findet den besten Zug für die Schlange
    best_move = []
    best_value = -math.inf

    for move in get_possible_moves(state):
        new_state = simulate_move(state, move)
        move_value = alphabeta(new_state, depth=3, alpha=-math.inf, beta=math.inf, maximizing_player=True) # minimax mit alpha-beta pruning
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
    # kopiert den aktuellen Zustand und führt den Zug aus
    new_state = state.copy()
    new_state["my_snake"] = state["my_snake"].copy()
    new_state["my_snake"]["body"] = state["my_snake"]["body"].copy()

    # update von der neuen Kopfposition
    new_head_position = new_state["my_snake"]["head"].copy()
    if move == "up":
        new_head_position['y'] += 1
    elif move == "down":
        new_head_position['y'] -= 1
    elif move == "left":
        new_head_position['x'] -= 1
    elif move == "right":
        new_head_position['x'] += 1
        
    # bewegt die Schlange
    new_body = [new_head_position] + new_state["my_snake"]["body"][:-1]
    new_state["my_snake"]["head"] = new_head_position
    new_state["my_snake"]["body"] = new_body

    if check_collision(new_state):
        new_state["my_snake"]["health"] = 0
    
    # gibt den neuen Zustand zurück
    return new_state

def check_collision(state):
    # Prüft, ob die Schlange kollidiert
    head = state['my_snake']['head']
    body = state['my_snake']['body']
    board_width = state['board']['width']
    board_height = state['board']['height']
    
    # Kollision mit der Wand
    if head['x'] < 0 or head['x'] >= board_width or head['y'] < 0 or head['y'] >= board_height:
        return True
    
    # Kollision mit sich selbst
    if head in body[1:]:  # exkludiert den Kopf
        return True
    
    # kolision mit anderen Schlangen
    for snake in state['board']['snakes']:
        if head in snake['body'][1:]:  # exkludiert den Kopf  
            return True
    
    # False wenn keine Kollision stattgefunden hat
    return False

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
