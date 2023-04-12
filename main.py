import pygame, sys
import numpy as np

pygame.init()

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
# rgb: red green blue
RED = (255, 0 , 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

# board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

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


def mark_square(row, col, player):
    board[row, col] = player


def available_square(row, col):
    return board[row, col] == 0

def is_board_full():
    val = np.prod(board)
    return val > 0

print(is_board_full())
draw_lines()

player = 1

# mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = mouseY // int(HEIGHT/3)
            clicked_col = mouseX // int(WIDTH/3)
            print(clicked_row, clicked_col)

            if available_square(clicked_row, clicked_col):


    pygame.display.update()