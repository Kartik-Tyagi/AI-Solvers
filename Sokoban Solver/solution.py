#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os  # for time functions
import math  # for infinity
from search import *  # for search engines
from sokoban import sokoban_goal_state, SokobanState, Direction, PROBLEMS  # for Sokoban specific classes and problems
import os

def manhattan_distance(loc1, loc2):
    return (abs(loc2[1] - loc1[1]) + abs(loc2[0] - loc1[0]))

def isPossible(loc1, loc2):
    return True

def hash_clear(list):
    for index in range(len(list)):
        list[index] = 0
        
def find_storage_x(list, box):
    for i in list:
        if i[0] == box[0]:
            return True
    return False
        
def find_storage_y(list, box):
    for i in list:
        if i[1] == box[1]:
            return True
    return False

def no_robot_left(state, value):
    for i in state.robots:
        if i[0] <= value:
            return False
    return True

def is_empty(lists):
    if lists == []:
        return False
    else:
        return True

def has_deadlock(state):
    boxes_available = list(state.boxes - state.storage)
    storages_available = list(state.storage - state.boxes)
    has_boxes = is_empty(boxes_available)
    deadlock = False
    while has_boxes and not deadlock:
        b = boxes_available[0]
        up = (b[0], b[1] - 1)
        right = (b[0] + 1, b[1])
        left = (b[0] - 1, b[1])
        down = (b[0], b[1] + 1)
        upright = (b[0] + 1, b[1] - 1)
        downright = (b[0] + 1, b[1] + 1)
        upleft = (b[0] - 1, b[1] - 1)
        downleft = (b[0] - 1, b[1] + 1)
        if ((b[0] == 0) or left in state.obstacles or right in state.obstacles) and ((b[1] == 0) or up in state.obstacles or down in state.obstacles):
            deadlock = True
        elif ((b[0] == state.width - 1) or left in state.obstacles or right in state.obstacles) and ((b[1] == 0) or up in state.obstacles or down in state.obstacles):
            deadlock = True
        elif ((b[0] == state.width - 1) or left in state.obstacles or right in state.obstacles) and ((b[1] == state.height - 1) or up in state.obstacles or down in state.obstacles):
            deadlock = True
        elif ((b[0] == 0) or left in state.obstacles or right in state.obstacles) and ((b[1] == state.height - 1) or up in state.obstacles or down in state.obstacles):
            deadlock = True
        elif (b[0] == 0) and (not find_storage_x(storages_available, b) or up in state.boxes or down in state.boxes):
            deadlock = True
        elif (b[1] == 0) and (not find_storage_y(storages_available, b) or left in state.boxes or right in state.boxes):
            deadlock = True
        elif (b[0] == state.width - 1) and (not find_storage_x(storages_available, b) or up in state.boxes or down in state.boxes):
            deadlock = True
        elif (b[1] == state.height - 1) and (not find_storage_y(storages_available, b) or left in state.boxes or right in state.boxes):
            deadlock = True
        elif ((up in state.boxes or up in state.obstacles) and (right in state.boxes or right in state.obstacles) and (upright in state.boxes or upright in state.obstacles)):
            deadlock = True
        elif ((up in state.boxes or up in state.obstacles) and (left in state.boxes or left in state.obstacles) and (upleft in state.boxes or upleft in state.obstacles)):
            deadlock = True
        elif ((down in state.boxes or down in state.obstacles) and (right in state.boxes or right in state.obstacles) and (downright in state.boxes or downright in state.obstacles)):
            deadlock = True
        elif ((down in state.boxes or down in state.obstacles) and (left in state.boxes or left in state.obstacles) and (downleft in state.boxes or downleft in state.obstacles)):
            deadlock = True
        elif (left in state.boxes and upright in state.obstacles and downright in state.obstacles):
            if (no_robot_left(state, b[0])):
                deadlock = True
        boxes_available.pop(0)
        has_boxes = is_empty(boxes_available)
    return deadlock

# SOKOBAN HEURISTICS
def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.
    # EXPLAIN YOUR HEURISTIC IN THE COMMENTS. Please leave this function (and your explanation) at the top of your solution file, to facilitate marking.
    if has_deadlock(state):
        return float('inf')
    
    all_goals = set(state.storage)
    all_boxes = set(state.boxes)
    
    hash_map = []
    
    for i in all_goals:
        hash_map.append(0)
        
    
    total_distance = 0
    
    if state.boxes != None:
        for box_pos in all_boxes:
            num = 0
            index = 0
            min_distance = float('inf')
            for goal_pos in all_goals:
                if (hash_map[num] == 0):
                    new_distance = manhattan_distance(box_pos, goal_pos)
                    if (new_distance < min_distance):
                        min_distance = new_distance
                        index = num
                num += 1
                if min_distance == 0:
                    break
            hash_map[index] = 1
            total_distance += min_distance
    
    return total_distance

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def heur_manhattan_distance(state):
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.
    total_distance = 0
    if state.boxes != None:
        for box_pos in state.boxes:
            min_distance = min([manhattan_distance(box_pos, goal) for goal in state.storage])
            total_distance += min_distance
    return total_distance

def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    
    return sN.gval + sN.hval * weight

# SEARCH ALGORITHMS
def weighted_astar(initial_state, heur_fn, weight, timebound):
    # IMPLEMENT    
    '''Provides an implementation of weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False as well as a SearchStats object'''
    '''implementation of weighted astar algorithm'''
    se = SearchEngine('custom', 'full')
    se.init_search(initial_state, sokoban_goal_state, heur_fn, lambda sN: fval_function(sN, weight))
    final_state = se.search(timebound)
    return final_state

def iterative_astar(initial_state, heur_fn, weight=1, timebound=5):  # uses f(n), see how autograder initializes a search line 88
    # IMPLEMENT
    '''Provides an implementation of realtime a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False as well as a SearchStats object'''
    '''implementation of iterative astar algorithm'''
    while (True):
        final_state = weighted_astar(initial_state, heur_fn, weight, timebound)
        if final_state == None:
            timebound += 1
        else:
            return final_state

def iterative_gbfs(initial_state, heur_fn, timebound=5):  # only use h(n)
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of iterative gbfs algorithm'''
    se = SearchEngine('best_first', 'full')
    se.init_search(initial_state, sokoban_goal_state, heur_fn)
    final_state = se.search(timebound)
    return final_state



