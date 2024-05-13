"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
cached_states = {}
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    p1_count, p2_count = get_score(board)
    if color == 1:
        return p1_count - p2_count
    else:
        return p2_count - p1_count

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    num_moves = len(get_possible_moves(board, color))
    opp_moves = len(get_possible_moves(board, 3 - color))
    moves_weight = 0.6
    dim = len(board)
    corner_weight = 3
    num_corners = 0
    if board[0][0] == color:
        num_corners += 1
    if board[0][dim - 1] == color:
        num_corners += 1
    if board[dim - 1][0] == color:
        num_corners += 1
    if board[dim - 1][dim - 1] == color:
        num_corners += 1
    util_weight = 1
        
    return util_weight*compute_utility(board, color) + moves_weight*num_moves + corner_weight*num_corners - moves_weight*opp_moves
            

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    if limit == 0 or not get_possible_moves(board, 3 - color):
        return None, compute_utility(board, color)
    
    best_move = None
    best_utility = float('inf')
    
    if (board, 3 - color) in cached_states and caching:
        return cached_states[(board, 3 - color)]

    for move in get_possible_moves(board, 3 - color):
        new_board = play_move(board, 3 - color, move[0], move[1])
        _, utility = minimax_max_node(new_board, color, limit - 1, caching)
        if utility < best_utility:
            best_utility = utility
            best_move = move
            
    if caching:
        cached_states[(board, 3 - color)] = (best_move,best_utility)
    
    return best_move, best_utility

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    if limit == 0 or not get_possible_moves(board, color):
        return None, compute_utility(board, color)
    
    best_move = None
    best_utility = float('-inf')
    
    if (board, color) in cached_states and caching:
        return cached_states[(board, color)]

    for move in get_possible_moves(board, color):
        new_board = play_move(board, color, move[0], move[1])
        _, utility = minimax_min_node(new_board, color, limit - 1, caching)
        if utility > best_utility:
            best_utility = utility
            best_move = move
    
    if caching:
        cached_states[(board, color)] = (best_move,best_utility)
    
    return best_move, best_utility

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #IMPLEMENT (and replace the line below)
    best_move = None
    best_utility = float('-inf')

    for move in get_possible_moves(board, color):
        new_board = play_move(board, color, move[0], move[1])
        _, utility = minimax_min_node(new_board, color, limit - 1, caching)
        if utility > best_utility:
            best_utility = utility
            best_move = move
    
    return best_move

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if limit == 0 or not get_possible_moves(board, 3 - color):
        return None, compute_utility(board, color)
    
    best_move = None
    best_utility = float('inf')
    
    if (board, 3 - color, alpha, beta) in cached_states and caching:
        return cached_states[(board, 3 - color, alpha, beta)]
    
    all_moves = get_possible_moves(board, 3 - color)
    if ordering:
        all_moves = sorted(all_moves, key=lambda x: compute_heuristic(play_move(board, 3 - color, x[0], x[1]), color))

    for move in all_moves:
        new_board = play_move(board, 3 - color, move[0], move[1])
        _, utility = alphabeta_max_node(new_board, color, alpha, beta, limit - 1, caching, ordering)
        if (utility < best_utility):
            best_utility = utility
            best_move = move
        if best_utility <= alpha:
            if caching:
                cached_states[(board, 3 - color, alpha, beta)] = (best_move,best_utility)
            return best_move, best_utility
        beta = min(best_utility, beta)
    
    if caching:
        cached_states[(board, 3 - color, alpha, beta)] = (best_move,best_utility)
    
    return best_move, best_utility

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if limit == 0 or not get_possible_moves(board, color):
        return None, compute_utility(board, color)
    
    best_move = None
    best_utility = float('-inf')
    
    if (board, color, alpha, beta) in cached_states and caching:
        return cached_states[(board, color, alpha, beta)]
    
    all_moves = get_possible_moves(board, color)
    if ordering:
        all_moves = sorted(all_moves, key=lambda x: compute_heuristic(play_move(board, color, x[0], x[1]), color), reverse = True)

    for move in all_moves:
        new_board = play_move(board, color, move[0], move[1])
        _, utility = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching, ordering)
        if (utility > best_utility):
            best_utility = utility
            best_move = move
        if utility >= beta:
            if caching:
                cached_states[(board, color, alpha, beta)] = (best_move,best_utility)
            return best_move, best_utility
        alpha = max(alpha, best_utility)
    
    if caching:
        cached_states[(board, color, alpha, beta)] = (best_move,best_utility)
    
    return best_move, best_utility

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    best_move = None
    best_utility = float('-inf')

    for move in get_possible_moves(board, color):
        new_board = play_move(board, color, move[0], move[1])
        _, utility = alphabeta_min_node(new_board, color, best_utility, float('inf'), limit - 1, caching, ordering)
        if utility > best_utility:
            best_utility = utility
            best_move = move
    
    return best_move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
