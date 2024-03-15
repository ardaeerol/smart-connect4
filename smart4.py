"""
    The code provided is a Python implementation of a Connect 4 game with an AI opponent using the
    minimax algorithm with alpha-beta pruning and iterative deepening for decision making.
    
    :param window: The `window` parameter in the code represents a list of 4 elements (pieces) in a row,
    column, or diagonal on the game board. The `evaluate_window` function takes this window as input and
    calculates a score based on the number and types of pieces in that window
    :param piece: Piece is a variable representing a player's game piece in the Connect 4 game. In this
    implementation, the piece can be either PLAYER_PIECE (1) or AI_PIECE (2). These values are used to
    identify which player's piece is placed in a particular cell on the game
    :return: The code returns the best column to place a piece in and the corresponding score for that
    move.
"""

import sys
import math
import random
import pygame
from base import *

MINIMAX = True  # Set to False to use iterative deepening

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4


def evaluate_window(window, piece):
    """
    Evaluate the score of a window (sequence of cells) for a given piece.
    """
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    """
    Evaluate the score of the board position for a given piece.
    """
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    """
    Check if the current board position is a terminal node (end of game).
    """
    return (
        winning_move(board, PLAYER_PIECE)
        or winning_move(board, AI_PIECE)
        or len(get_valid_locations(board)) == 0
    )


def minimax(board, depth, alpha, beta, maximizingPlayer):
    """
    Minimax algorithm with alpha-beta pruning for selecting the best move.
    """
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)  # High positive score for AI win
            elif winning_move(board, PLAYER_PIECE):
                return (
                    None,
                    -1000000000000,
                )  # High negative score for player win (fixed typo)
            else:
                return (None, 0)  # Game is a draw
        else:
            return (
                None,
                score_position(board, AI_PIECE),
            )  # Evaluate current position if depth limit is reached

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row == -1:
                continue  # Column is full, skip
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cutoff
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row == -1:
                continue  # Column is full, skip
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha cutoff
        return column, value


def iterative_deepening(board, max_depth):
    """
    Iterative Deepening algorithm for selecting the best move.
    """
    best_move = None
    for depth_limit in range(1, max_depth + 1):
        # Perform depth-limited search with alpha-beta pruning
        move, _ = depth_limited_search(board, depth_limit)
        if move is not None:
            best_move = move
    return best_move


# Depth-limited search algorithm with alpha-beta pruning for selecting the best move.
def depth_limited_search(
    board, depth_limit, alpha=-math.inf, beta=math.inf, maximizingPlayer=True
):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth_limit == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (
                None,
                score_position(board, AI_PIECE),
            )  # Evaluation function for non-terminal nodes

    if maximizingPlayer:
        value = -math.inf
        column = None
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row == -1:
                continue  # Column is full, skip
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            _, new_score = depth_limited_search(
                b_copy, depth_limit - 1, alpha, beta, False
            )
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = None
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row == -1:
                continue  # Column is full, skip
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            _, new_score = depth_limited_search(
                b_copy, depth_limit - 1, alpha, beta, True
            )
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):

    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                ),
                RADIUS,
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False

pygame.init()
pygame.display.set_caption("Smart Connect 4")

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)

    # # Ask for Player 2 Input
    if turn == AI and not game_over:

        # col = random.randint(0, COLUMN_COUNT-1)
        # col = pick_best_move(board, AI_PIECE)
        col, search_score = (
            minimax(board, 5, -math.inf, math.inf, True)
            if MINIMAX
            else depth_limited_search(board, 5, -math.inf, math.inf, True)
        )

        if is_valid_location(board, col):
            # pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)
