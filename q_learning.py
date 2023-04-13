import itertools

import numpy as np
import numpy.random as rd

# Encode board state as a string
def board_to_str(board):
    str_arr = board.astype(str)
    return ''.join(str_arr.flatten())

# Decode board state from a string
def str_to_board(board_str):
    return np.array(list(test_str), dtype=int).reshape(3,3)

# get Q(S_t)
def get_Q_val(Q, state):
    if not state in Q:
        Q[state] = 0
    return Q[state]

Q = {}
board = np.zeros((3,3))
player = 1
epsilon = 0.5

# choose action using epsilon-greedy strategy
available_actions = np.argwhere(board == 0)
# if rd.rand() < epsilon:
#     rand_id = rd.randint(len(available_actions))
#     action = available_actions[rand_id]
# else:
#     q_values =

# create a list with possible states
def take_action(current_board, action):
    b = current_board.copy()
    b[action[0], action[1]] = 1
    return b

take_action(board, available_actions[0])