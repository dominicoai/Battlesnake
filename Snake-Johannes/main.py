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

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Jojo",  # TODO: Your Battlesnake Username
        "color": "#888889",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }

prev_cells = []

# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    global prev_cells 
    prev_cells = []
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

    punkte = {
        "up" : 0,
        "down" : 0, 
        "left": 0, 
        "right": 0
    }

    global prev_cells
    
    round = game_state["turn"]
    
    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        punkte["left"] = punkte["left"] -100
        is_move_safe["left"] = False
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        punkte["right"] = punkte["right"] -100
        is_move_safe["right"] = False
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        punkte["down"] = punkte["down"] -100
        is_move_safe["down"] = False
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        punkte["up"] = punkte["up"] -100
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    if my_head["x"] == 0:
        punkte["left"] = punkte["left"] -100
        is_move_safe["left"] = False
    if my_head["x"] == game_state["board"]["width"]:
        punkte["right"] = punkte["right"] -100
        is_move_safe["right"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
        punkte["down"] = punkte["down"] -100
    if my_head["y"] == game_state["board"]["height"]:
        punkte["up"] = punkte["up"] -100
        is_move_safe["up"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state["you"]["body"][1:]
    for k_teil in my_body:
        if my_head["x"] == k_teil["x"]:
            if my_head["y"] == k_teil["y"] - 1:
                punkte["down"] = punkte["down"] -100
                is_move_safe["down"] = False 
            elif my_head["y"] == k_teil["y"] + 1:
                punkte["up"] = punkte["up"] -100
                is_move_safe["up"] = False
        if my_head["y"] == k_teil["y"]:
            if my_head["x"] == k_teil["x"] - 1:
                punkte["left"] = punkte["left"] -100
                is_move_safe["left"] = False 
            elif my_head["x"] == k_teil["x"] + 1:
                punkte["right"] = punkte["right"] -100
                is_move_safe["right"] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    enemies = game_state["board"]["snakes"]
    for enemy in enemies:
        if enemy["id"] != game_state["you"]["id"]:
            enemy_body = enemy["body"]
            for k_teil in enemy_body:
                if my_head["x"] == k_teil["x"]:
                    if my_head["y"] == k_teil["y"] - 1:
                        punkte["down"] = punkte["down"] -100
                        is_move_safe["down"] = False 
                    elif my_head["y"] == k_teil["y"] + 1:
                        punkte["up"] = punkte["up"] -100
                        is_move_safe["up"] = False
                if my_head["y"] == k_teil["y"]:
                    if my_head["x"] == k_teil["x"] - 1:
                        punkte["left"] = punkte["left"] -100
                        is_move_safe["left"] = False 
                    elif my_head["x"] == k_teil["x"] + 1:
                        punkte["right"] = punkte["right"] -100
                        is_move_safe["right"] = False
     
    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
    


    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    dist = []
    if len(food) > 0:
        for fast_food in food:
            if my_head["x"] < fast_food["x"] and my_head["y"] < fast_food["y"]:
                dis = fast_food["x"] - my_head["x"] + fast_food["y"] - my_head["y"]
                dist.append(dis)
            if my_head["x"] > fast_food["x"] and my_head["y"] > fast_food["y"]:
                dis = fast_food["x"] + my_head["x"] + fast_food["y"] + my_head["y"]
                dist.append(dis)	
            if my_head["x"] < fast_food["x"] and my_head["y"] > fast_food["y"]:
                dis = fast_food["x"] - my_head["x"] + fast_food["y"] + my_head["y"]
                dist.append(dis)
            if my_head["x"] > fast_food["x"] and my_head["y"] < fast_food["y"]:
                dis = fast_food["x"] + my_head["x"] + fast_food["y"] - my_head["y"]
                dist.append(dis)

        closest_food_id = dist.index(min(dist))
        clostest_food = food[closest_food_id]

    prev_cells.append((my_head["x"], my_head["y"]))
    
    
    if len(prev_cells) >= 4:
        runde = round-4
        previous_x = prev_cells[runde][0]
        previous_y = prev_cells[runde][1]  
        if (previous_x, previous_y) == (my_head["x"], my_head["y"]):
            if is_move_safe["right"] == True:
                punkte["right"] = punkte["right"] + 5
                print(f"MOVE {game_state['turn']}: kreis")
            if is_move_safe["left"] == True:
                punkte["left"] = punkte["left"] + 5
                print(f"MOVE {game_state['turn']}: kreis")
            if is_move_safe["up"] == True:
                punkte["up"] = punkte["up"] + 5    
                print(f"MOVE {game_state['turn']}: kreis")
            if is_move_safe["down"] == True:
                punkte["down"] = punkte["down"] + 5
                print(f"MOVE {game_state['turn']}: kreis")
        if len(safe_moves) >= 1 and len(food) > 0:
            if my_head["x"] < clostest_food["x"] and is_move_safe["right"]:
                punkte["right"] = punkte["right"] + 10
            if my_head["x"] > clostest_food["x"] and is_move_safe["left"]:
                punkte["left"] = punkte["left"] + 10
            if my_head["y"] < clostest_food["y"] and is_move_safe["up"]:
                punkte["up"] = punkte["up"] + 10
            if my_head["y"] > clostest_food["y"] and is_move_safe["down"]:
                punkte["down"] = punkte["down"] + 10
        elif len(safe_moves) >=1:
            next_move = random.choice(safe_moves)
            return {"move": next_move}
        else:
            print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
            next_move = "down"
            return {"move": next_move}
    else:
        if len(safe_moves) >= 1 and len(food) > 0:
            if my_head["x"] < clostest_food["x"] and is_move_safe["right"]:
                punkte["right"] = punkte["right"] + 10
            elif my_head["x"] > clostest_food["x"] and is_move_safe["left"]:
                punkte["left"] = punkte["left"] + 10
            elif my_head["y"] < clostest_food["y"] and is_move_safe["up"]:
                punkte["up"] = punkte["up"] + 10
            elif my_head["y"] > clostest_food["y"] and is_move_safe["down"]:
                punkte["down"] = punkte["down"] + 10
        elif len(safe_moves) >=1:
            next_move = random.choice(safe_moves)
            return {"move": next_move}
        else:
            print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
            next_move = "down"
            return {"move": next_move}

    print(f"Punkte: {punkte}")
    
    max_val = punkte["up"]
    max_step = "up"
    for step, val in punkte.items():
        if val > max_val:
            max_val = val
            max_step = step

    next_move = max_step
    
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}
    


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })        
           
