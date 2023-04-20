import numpy as np
import numpy.random as rd
import pickle

# Encode board state as a string
def board_to_str(board):
    str_arr = board.astype(str)
    return ''.join(str_arr.flatten())

# Decode board state from a string
def str_to_board(board_str):
    return np.array(list(board_str), dtype=int).reshape(3,3)

# get Q(S_t)
def get_Q_val(Q, state):
    if not state in Q:
        Q[state] = 0
    return Q[state]

# create a list with possible states
def take_action(current_board, action, player):
    b = current_board.copy()
    b[action[0], action[1]] = player
    return b

# Get all symmetric states
def get_symmetric_states(board):
    states = [board]

    # Rotations
    for _ in range(3):
        board = np.rot90(board)
        states.append(board)

    # Reflections
    board = np.flip(board, axis=0)
    states.append(board)
    for _ in range(3):
        board = np.rot90(board)
        states.append(board)

    states = list(set([board_to_str(state) for state in states]))
    return states


# Check if the game has ended and return the winner
def game_ended(board):
    for player in [1, 2]:
        for row in board:
            if np.all(row == player):
                return True, player
        for col in board.T:
            if np.all(col == player):
                return True, player
        if np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player):
            return True, player
    if np.all(board != 0):
        return True, 0  # Draw
    return False, None  # Game not ended

def get_max_Q_fom_symmetric_states(Q, board):
    max_Q = max(Q.get(s, 0) for s in get_symmetric_states(board))
    return max_Q

def get_min_Q_fom_symmetric_states(Q, board):
    min_Q = min(Q.get(s, 0) for s in get_symmetric_states(board))
    return min_Q

# Q = {}
with open('Q_table.pickle', 'rb') as f:
    Q = pickle.load(f)
epsilon_arr = np.linspace(0.1, 1.0, 10)[::-1]
gamma = 0.8
alpha = 0.5
T = 1000
epochs = np.arange(20)
for epoch in epochs:
    print(f"epoch: {epoch}")
    for epsilon in epsilon_arr:
        print(f"epsilon = {epsilon}")
        for episode in range(T):
            board = np.zeros((3, 3), dtype=int)
            player = 1
            if episode % int(T/4) == 0:
                print(f"{(episode/T)*100} %")
            player_list = []
            while True:
                # choose action using epsilon-greedy strategy
                available_actions = np.argwhere(board == 0)
                if rd.rand() < epsilon or np.all(board == 0):
                    rand_id = rd.randint(len(available_actions))
                    action = available_actions[rand_id]
                else:
                    possible_boards = [take_action(board, action, player) for action in available_actions]
                    q_values = [Q.get(board_to_str(b), 0) for b in possible_boards]
                    if player == 1:
                        action = available_actions[np.argmax(q_values)]
                    else:
                        action = available_actions[np.argmin(q_values)]

                # Take action and observe next state
                next_board = take_action(board, action, player)
                ended, winner = game_ended(next_board)
                # Update Q-table
                if ended:
                    reward = 1 if winner == 1 else -1 if winner == 2 else 0
                    symmetric_states = get_symmetric_states(next_board)
                    for ss in symmetric_states:
                        Q[ss] = reward
                    target = gamma * reward
                else:
                    next_state = board_to_str(next_board)
                    target = gamma * Q.get(next_state, 0)

                current_symmetric_states = get_symmetric_states(board)
                for ss in current_symmetric_states:
                    Q[ss] = Q.get(ss, 0) + alpha * (target - Q.get(ss, 0))

                if ended:
                    break

                board = next_board
                player = 3 - player

# Save the dictionary to a file
with open('Q_table.pickle', 'wb') as f:
    pickle.dump(Q, f)

# # Load the dictionary from the file
# with open('Q_table.pickle', 'rb') as f:
#     Q = pickle.load(f)