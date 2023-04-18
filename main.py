import pygame, sys
import numpy as np
import numpy.random as rd
import time
import pickle


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
def get_max_Q_fom_symmetric_states(Q, board):
    max_Q = max(Q.get(s, 0) for s in get_symmetric_states(board))
    return max_Q

def get_min_Q_fom_symmetric_states(Q, board):
    min_Q = min(Q.get(s, 0) for s in get_symmetric_states(board))
    return min_Q

def board_to_str(board):
    board_ = board.astype(int)
    str_arr = board_.astype(str)
    return ''.join(str_arr.flatten())

def take_action(current_board, action, player):
    b = current_board.copy()
    b[action[0], action[1]] = player
    return b


def draw_horizontal_lines():
    y_axis = 0
    for i in range(2):
        y_axis += int(HEIGHT/3)
        pygame.draw.line( screen, LINE_COLOR, (0, y_axis), (WIDTH, y_axis), LINE_WIDTH )


def draw_vertical_lines():
    x_axis = 0
    for i in range(2):
        x_axis += int(WIDTH/3)
        pygame.draw.line( screen, LINE_COLOR, (x_axis, 0), (x_axis, HEIGHT), LINE_WIDTH )


def draw_lines():

    draw_horizontal_lines()
    draw_vertical_lines()


def draw_figures():
    x_square, y_square = WIDTH/3, HEIGHT/3
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row, col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col*x_square+x_square/2), int(row*y_square+y_square/2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row, col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col*x_square+SPACE, row*y_square+y_square-SPACE),
                                 (col*x_square+x_square-SPACE, row*y_square+SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col*x_square+SPACE, row*y_square+SPACE),
                                 (col*x_square+x_square-SPACE, row*y_square+y_square-SPACE), CROSS_WIDTH)

def mark_square(board, row, col, player):
    board[row, col] = player
    return board


def initiate_player(human_player, AI_player):
    if human_player == 1:
        return human_player # human player's turn
    else:
        return AI_player # AI's turn


def available_square(row, col):
    return board[row, col] == 0

def is_board_full():
    val = np.prod(board)
    return val > 0

def handle_human_event(player, human_player, board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if player == human_player:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = mouseY // int(HEIGHT/3)
                clicked_col = mouseX // int(WIDTH/3)

                if board[clicked_row, clicked_col] == 0:
                    board = mark_square(board, clicked_row, clicked_col, player)
                    draw_figures()
                    player = 3 - player
    return player

def ai_max(available_actions, board, player, Q):
    possible_boards = [take_action(board, action, player) for action in available_actions]
    q_values = [get_min_Q_fom_symmetric_states(Q, b) for b in possible_boards]
    if sum(q_values) == 0:
        rand_id = rd.randint(len(available_actions))
        action = available_actions[rand_id]
    else:
        m = q_values == np.min(q_values)
        if np.sum(m) > 1:
            rand_id = rd.randint(len(available_actions[m]))
            action = available_actions[m][rand_id]
        else:
            action = available_actions[np.argmax(q_values)]
    clicked_row, clicked_col = action[0], action[1]
    return clicked_row, clicked_col


def ai_min(available_actions, board, player, Q):
    possible_boards = [take_action(board, action, player) for action in available_actions]
    q_values = [get_min_Q_fom_symmetric_states(Q, b) for b in possible_boards]
    if sum(q_values) == 0:
        rand_id = rd.randint(len(available_actions))
        action = available_actions[rand_id]
    else:
        m = q_values == np.max(q_values)
        if np.sum(m) > 1:
            rand_id = rd.randint(len(available_actions[m]))
            action = available_actions[m][rand_id]
        else:
            action = available_actions[np.argmin(q_values)]
    clicked_row, clicked_col = action[0], action[1]
    return clicked_row, clicked_col

def handle_ai_event(player, AI_player, Q, board):
    if player == AI_player:
        available_actions = np.argwhere(board == 0)
        if len(available_actions) > 0:
            if AI_player == 1:
                clicked_row, clicked_col = ai_max(available_actions, board, player, Q)
            else:
                clicked_row, clicked_col = ai_min(available_actions, board, player, Q)
            board = mark_square(board, clicked_row, clicked_col, player)
            draw_figures()
            player = 3 - player
    return player

pygame.init()

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 65
CIRCLE_WIDTH = 20
CROSS_WIDTH = 30
SPACE = 55
# rgb: red green blue
RED = (255, 0 , 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

# board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Load the dictionary from the file
with open('Q_table.pickle', 'rb') as f:
    Q = pickle.load(f)

print(len(Q))

draw_lines()

human_player = 1
AI_player = 2

player = initiate_player(human_player, AI_player)

# mainloop
while True:
        player = handle_human_event(player, human_player, board)
        pygame.display.update()
        player = handle_ai_event(player, AI_player, Q, board)
        pygame.display.update()

# def player_1_AI_takes_action():