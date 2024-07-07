import math
# Code by
# Dominic Foraschick (Matrikelnummer: 222200429)
# Tommy Stettin (Matrikelnummer: 221200375)
# Johannes Peters (Matrikelnummer: 218205404)
# Laurin Haase (Matrikelnummer: 217204840) 


# Code für Minimax-Algorithmus mit Alpha-Beta-Pruning
def alphabeta(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_terminal(state):
        return evaluate(state)
    # alpha: bestes Ergebnis, das der maximierende Spieler bisher gefunden hat
    # beta: bestes Ergebnis, das der minimierende Spieler bisher gefunden hat
    if maximizing_player:
        max_eval = -math.inf
        for next in get_next(state):
            eval = alphabeta(next, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for next in get_next(state):
            eval = alphabeta(next, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
    
def is_terminal(state):
    # Prüfung, ob Schlange tot ist
    head = state["my_snake"]["head"]
    board_width = state["board"]["width"]
    board_height = state["board"]["height"]
    body = state["my_snake"]["body"]
    opponents = state["board"]["snakes"]
    possible_moves = {
        "up": {"x": head["x"], "y": head["y"] + 1},
        "down": {"x": head["x"], "y": head["y"] - 1},
        "left": {"x": head["x"] - 1, "y": head["y"]},
        "right": {"x": head["x"] + 1, "y": head["y"]}
    }
    
    if head["x"] < 0 or head["x"] >= board_width or head["y"] < 0 or head["y"] >= board_height:
        return True
    
    if head in state["my_snake"]["body"][1:] or head in state["board"]["snakes"]:
        return True
    
    if any(segment['x'] == head['x'] and segment['y'] == head['y'] for segment in body[1:]):
        return True
    
    for snake in opponents:
        if any(segment['x'] == head['x'] and segment['y'] == head['y'] for segment in snake['body']):
            return True
    

    
    return False

def evaluate(state):
    # Zustand der Schlange
    head = state["my_snake"]["head"]
    health = state["my_snake"]["health"]
    body = state["my_snake"]["body"]
    food = state["board"]["food"]
    opponents = state["board"]["snakes"]
    board_width = state["board"]["width"]
    board_height = state["board"]["height"]
    
    # Gewichtung
    weight_food_distance = 0.3
    weight_health = 0.2
    weight_space = 0.25
    weight_opponents_distance = 0.15
    weight_length = 0.1
    
    # Abstand zur Nahrung (Manhattan-Distanz)
    if food:
        min_food_distance = min(
            abs(head["x"] - f["x"]) + abs(head["y"] - f["y"])
            for f in food
        )
        food_distance_score = 1 / (min_food_distance + 1)
    else:
        food_distance_score = 0
        
    # Gesundheit
    health_score = health / 20
    
    # Freier Platz	
    space_score = calculate_space_score(state)
    
    # Abstand zu Gegnern (Manhattan-Distanz)
    min_opponents_distance = float("inf")
    for snake in opponents:
        for segment in snake["body"]:
            distance = abs(head["x"] - segment["x"]) + abs(head["y"] - segment["y"])
            if distance < min_opponents_distance:
                min_opponents_distance = distance
    opponents_distance_score = 1 / (min_opponents_distance + 1)
    
    # Länge der Schlange
    length_score = len(body) / (board_width * board_height)
    
    # Gesamtbewertung
    evaluation = (
        weight_food_distance * food_distance_score +
        weight_health * health_score +
        weight_space * space_score +
        weight_opponents_distance * opponents_distance_score +
        weight_length * length_score
    )
    
    return evaluation 

def calculate_space_score(state):
    # Kaluliert den freien Platz auf dem Spielfeld
    head = state["my_snake"]["head"]
    board_width = state["board"]["width"]
    board_height = state["board"]["height"]
    body = state["my_snake"]["body"]
    opponents = state["board"]["snakes"]
    
    space_score = 0
    for x in range(board_width):
        for y in range(board_height):
            if {"x": x, "y": y} not in body and not any(segment["x"] == x and segment["y"] == y for snake in opponents for segment in snake["body"]):
                space_score += 1
    return space_score / (board_width * board_height)

def get_next(state):
    # Mögliche nächste Zustände
    next = []
    head = state["my_snake"]["head"]
    body = state["my_snake"]["body"]
    board_width = state["board"]["width"]
    board_height = state["board"]["height"]
    opponents = state["board"]["snakes"]
    food = state["board"]["food"]
    
    possible_moves = {
        "up": {"x": head["x"], "y": head["y"] + 1},
        "down": {"x": head["x"], "y": head["y"] - 1},
        "left": {"x": head["x"] - 1, "y": head["y"]},
        "right": {"x": head["x"] + 1, "y": head["y"]}
    }
    
    for move, new_head in possible_moves.items():
        # Prüfung, Kopf innerhalb des Spielfelds
        if (new_head["x"] < 0 or new_head["x"] >= board_width or
            new_head["y"] < 0 or new_head["y"] >= board_height):
            continue
        
        # Prüfung, Kopf nicht in eigenem Körper
        if any(segment["x"] == new_head["x"] and segment["y"] == new_head["y"] for segment in body):
            continue
        
        # Prüfung, Kopf nicht in Körper eines Gegners
        collision = False
        for snake in opponents:
            if any(segment["x"] == new_head["x"] and segment["y"] == new_head["y"] for segment in snake["body"]):
                collision = True
                break
        if collision:
            continue
    
        new_body =[new_head] + body[:-1]
        new_state = {
            "my_snake": {
                "head": new_head,
                "body": new_body,
                "health": state["my_snake"]["health"] - 1
            },
            "board": {
                "width": board_width,
                "height": board_height,
                "food": food,
                "snakes": opponents + [{"head": new_head, "body": new_body, "health": state["my_snake"]["health"] - 1}]
            },
            "turn": state["turn"] + 1
        }
        
        # Prüfung, ob Kopf auf Nahrung
        if new_head in food:
            new_state["my_snake"]["health"] = 100
            new_state["my_snake"]["body"].append(body[-1])
            new_state["board"]["food"].remove(new_head)
            
        next.append(new_state)
        
    return next