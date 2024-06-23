import math

def minimax(state, depth, maximimizing_player):
    if depth == 0 or is_terminal(state):
        return evaluate(state)
    
    if maximimizing_player:
        max_eval = -math.inf
        for next in get_next(state):
            eval = minimax(next, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for next in get_next(state):
            eval = minimax(next, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def alphabeta(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_terminal(state):
        return evaluate(state)
    
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
            eval = alphabeta(next, depth -1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
    
def is_terminal(state):
    # Definition wann das Spiel beendet ist
    pass

def evaluate(state):
    # Bewertungsfunktion für einen Zustand
    pass

def get_next(state):
    # Erzeugung der möglichen Folgezustände
    pass
    
