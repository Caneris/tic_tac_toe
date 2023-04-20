import pygame, sys
import numpy as np
import numpy.random as rd
import time
import pickle
import pygame.font

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

def handle_human_event(player, human_player, board, human_turn):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if player == human_player:
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and human_turn:
                human_turn = False
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = mouseY // int(HEIGHT/3)
                clicked_col = mouseX // int(WIDTH/3)

                if board[clicked_row, clicked_col] == 0:
                    board = mark_square(board, clicked_row, clicked_col, player)
                    draw_figures()
                    player = 3 - player
                    print(board)
                    print()

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_r:
        #         restart()
        #         game_over = False
    return board, player, human_turn

def ai_max(available_actions, board, player, Q):
    possible_boards = [take_action(board, action, player) for action in available_actions]
    q_values = [Q.get(board_to_str(b), 0) for b in possible_boards]
    if np.all(board==0):
        rand_id = rd.randint(len(available_actions))
        action = available_actions[rand_id]
    else:
        action = available_actions[np.argmax(q_values)]
    clicked_row, clicked_col = action[0], action[1]
    return clicked_row, clicked_col


def ai_min(available_actions, board, player, Q):
    possible_boards = [take_action(board, action, player) for action in available_actions]
    q_values = [Q.get(board_to_str(b), 0) for b in possible_boards]
    if np.all(board==0):
        rand_id = rd.randint(len(available_actions))
        action = available_actions[rand_id]
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
    return board, player, True


def game_ended(board):
    for player in [1, 2]:
        for row_i in range(board.shape[0]):
            row = board[row_i]
            if np.all(row == player):
                draw_horizontal_winning_line(row_i, player)
                return True, player
        for col_i in range(board.shape[0]):
            col = board.T[col_i]
            if np.all(col == player):
                draw_vertical_winning_line(col_i, player)
                return True, player
        if np.all(np.diag(board) == player):
            draw_descending_diag(player)
            return True, player
        elif np.all(np.diag(np.fliplr(board)) == player):
            draw_ascending_diag(player)
            return True, player
    if np.all(board != 0):
        return True, 0  # Draw
    return False, None  # Game not ended

def draw_vertical_winning_line(col, player):
    x_square = WIDTH/3
    posX = col*x_square + (x_square/2)
    if player == 1:
        color = CIRCLE_COLOR
    else:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT-15), 10)


def draw_horizontal_winning_line(row, player):
    y_square = HEIGHT / 3
    posY = row * y_square + (y_square / 2)
    if player == 1:
        color = CIRCLE_COLOR
    else:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, posY), (WIDTH-15, posY), 10)


def draw_ascending_diag(player):
    if player == 1:
        color = CIRCLE_COLOR
    else:
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT-15), (WIDTH-15, 15), 15)


def draw_descending_diag(player):
    if player == 1:
        color = CIRCLE_COLOR
    else:
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH-15, HEIGHT-15), 15)


def restart(player, board):
    screen.fill( BG_COLOR )
    draw_lines()
    player = 1
    board[:,:] = np.zeros((BOARD_ROWS, BOARD_COLS))
    return board, player


def start_screen():
    pygame.font.init()
    font_path = "04B_30__.TTF"
    font_size = 20
    font = pygame.font.Font(font_path, font_size)
    title_font = pygame.font.Font(font_path, font_size+10)
    note_font = pygame.font.Font(font_path, font_size - 5)
    title_surface = title_font.render("TIC TAC TOE", True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
    text_surface1 = font.render("Press '1' to be Player 1 (O)", True, (0, 0, 0))
    text_surface2 = font.render("Press '2' to be Player 2 (X)", True, (0, 0, 0))
    note_surface = note_font.render("Programmed by Caner Ates", True, (0, 0, 0))
    note_rect = note_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.fill(BG_COLOR)
    screen.blit(title_surface, title_rect)
    screen.blit(text_surface1, (WIDTH // 2 - text_surface1.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(text_surface2, (WIDTH // 2 - text_surface2.get_width() // 2, HEIGHT // 2))
    screen.blit(note_surface, note_rect)
    pygame.display.update()
    #pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2

def end_screen(winner, human_player, AI_player, player, board):
    if winner == human_player:
        text = "You won!"
    elif winner == AI_player:
        text = "You lost!"
    else:
        text = "It's a draw!"
    pygame.font.init()
    font_path = "I-pixel-u.ttf"
    font_size = 30
    font = pygame.font.Font(font_path, font_size)
    text_surface1 = font.render(text, True, (0, 0, 0))
    text_surface2 = font.render("Press 'R' to restart the game", True, (0, 0, 0))
    # screen.fill(BG_COLOR)
    screen.blit(text_surface1, (WIDTH // 2 - text_surface1.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(text_surface2, (WIDTH // 2 - text_surface2.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    #pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return restart(player, board)

pygame.init()

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 30
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 65
CIRCLE_WIDTH = 20
CROSS_WIDTH = 30
SPACE = 55
# rgb: red green blue
RED = (255, 0 , 0)
BG_COLOR = (255, 204, 229)
LINE_COLOR = (216, 162, 162)
CIRCLE_COLOR = (0, 102, 0)
CROSS_COLOR = (66, 66, 66)

# board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Load the dictionary from the file
with open('Q_table.pickle', 'rb') as f:
    Q = pickle.load(f)

len(Q)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

human_player = 1
AI_player = 2
player = initiate_player(human_player, AI_player)

game_over = False
start = False

human_player = start_screen()
AI_player = 3 - human_player
print(f"AI_player: {AI_player}")
human_turn = False
if human_player == 1:
    human_turn = True
else:
    human_turn = False


screen.fill(BG_COLOR)
draw_lines()
# mainloop
while True:
        board, player, human_turn = handle_human_event(player, human_player, board, human_turn)
        pygame.display.update()
        ended, winner = game_ended(board)
        if ended:
            game_over = True
            board, player = end_screen(winner, human_player, AI_player, player, board)
            game_over = False

        board, player, human_turn = handle_ai_event(player, AI_player, Q, board)
        ended, winner = game_ended(board)
        if ended:
            game_over = True
            board, player = end_screen(winner, human_player, AI_player, player, board)
            game_over = False
        pygame.display.update()