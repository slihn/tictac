import random
import itertools
import numpy as np


from tictac.tictac import transform


BOARD_SIZE = 3
BOARD_DIMENSIONS = (BOARD_SIZE, BOARD_SIZE)

CELL_X = 1
CELL_O = -1
CELL_EMPTY = 0

RESULT_X_WINS = 1
RESULT_O_WINS = -1
RESULT_DRAW = 0
RESULT_NOT_OVER = 2  # this is not for the end result. it is just an intermediate status.

# a Board is an array of CELLs representing N x N matrix
new_board = np.array([CELL_EMPTY] * BOARD_SIZE ** 2)


def play_game(x_strategy, o_strategy):
    board = Board()  # new board
    player_strategies = itertools.cycle([x_strategy, o_strategy])

    while not board.is_game_over():
        play = next(player_strategies)  # X, O, X, O, ..., game over
        board = play(board)

    return board


def play_games(total_games, x_strategy, o_strategy, play_single_game=play_game):
    results = {
        RESULT_X_WINS: 0,
        RESULT_O_WINS: 0,
        RESULT_DRAW: 0
    }

    for g in range(total_games):
        end_of_game = (play_single_game(x_strategy, o_strategy))
        result = end_of_game.get_game_result()
        results[result] += 1

    x_wins_percent = results[RESULT_X_WINS] / total_games * 100
    o_wins_percent = results[RESULT_O_WINS] / total_games * 100
    draw_percent = results[RESULT_DRAW] / total_games * 100

    print(f"x wins: {x_wins_percent:.2f}%")
    print(f"o wins: {o_wins_percent:.2f}%")
    print(f"draw  : {draw_percent:.2f}%")

    percents = {
        RESULT_X_WINS: x_wins_percent,
        RESULT_O_WINS: o_wins_percent,
        RESULT_DRAW: draw_percent
    }
    return percents


def is_even(value):
    return value % 2 == 0


def is_empty(values):
    return values is None or len(values) == 0


# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------
class Board:
    def __init__(self, board=None, illegal_move=None):
        if board is None:
            self.board = np.copy(new_board)
        else:
            self.board = board

        self.illegal_move = illegal_move

        self.board_2d = self.board.reshape(BOARD_DIMENSIONS)

    def get_game_result(self):
        if self.illegal_move is not None:
            return RESULT_O_WINS if self.get_turn() == CELL_X else RESULT_X_WINS

        rows_cols_and_diagonals = get_rows_cols_and_diagonals(self.board_2d)

        sums = list(map(sum, rows_cols_and_diagonals))
        max_value = max(sums)
        min_value = min(sums)

        if max_value == BOARD_SIZE:
            return RESULT_X_WINS

        if min_value == -BOARD_SIZE:
            return RESULT_O_WINS

        if CELL_EMPTY not in self.board_2d:
            return RESULT_DRAW

        return RESULT_NOT_OVER

    # result related routines
    def is_game_over(self):
        return self.get_game_result() != RESULT_NOT_OVER

    def is_draw(self):
        return self.get_game_result() == RESULT_DRAW

    # ----------------------------------------------------
    # moves and state
    def is_in_illegal_state(self):
        return self.illegal_move is not None

    def play_move(self, move_index: int):  # returns next Board()
        board_copy = np.copy(self.board)

        if move_index not in self.get_valid_move_indexes():
            return Board(board_copy, illegal_move=move_index)

        board_copy[move_index] = self.get_turn()
        return Board(board_copy)

    def get_turn(self):  # who should play next move
        non_zero = np.count_nonzero(self.board)
        return CELL_X if is_even(non_zero) else CELL_O

    def get_valid_move_indexes(self) -> [int]:
        return [i for i in range(self.board.size) if self.board[i] == CELL_EMPTY]

    def get_illegal_move_indexes(self) -> [int]:
        return [i for i in range(self.board.size) if self.board[i] != CELL_EMPTY]

    def get_random_valid_move_index(self) -> int:
        return random.choice(self.get_valid_move_indexes())

    # -----------------------------------------------------
    def print_board(self):
        print(self.get_board_as_string())

    def get_board_as_string(self) -> str:
        rows, cols = self.board_2d.shape
        board_as_string = "-------\n"
        for r in range(rows):
            for c in range(cols):
                move = get_symbol(self.board_2d[r, c])
                if c == 0:
                    board_as_string += f"|{move}|"
                elif c == 1:
                    board_as_string += f"{move}|"
                else:
                    board_as_string += f"{move}|\n"
        board_as_string += "-------\n"

        return board_as_string


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
class BoardCache:
    def __init__(self):
        # a generic cache for {board -> value} data
        self.cache = {}

    def set_for_position(self, board, o):
        self.cache[board.board_2d.tobytes()] = o

    def get_for_position(self, board):
        board_2d = board.board_2d

        orientations = transform.get_symmetrical_board_orientations(board_2d)

        for b, t in orientations:
            result = self.cache.get(b.tobytes())
            if result is not None:
                return (result, t), True

        return None, False

    def reset(self):
        self.cache = {}


def get_rows_cols_and_diagonals(board_2d):
    rows_and_diagonal = get_rows_and_diagonal(board_2d)
    cols_and_anti_diagonal = get_rows_and_diagonal(np.rot90(board_2d))
    return rows_and_diagonal + cols_and_anti_diagonal


def get_rows_and_diagonal(board_2d):
    num_rows = board_2d.shape[0]
    return ([row for row in board_2d[range(num_rows), :]]
            + [board_2d.diagonal()])


def get_symbol(cell):
    if cell == CELL_X:
        return 'X'
    if cell == CELL_O:
        return 'O'
    return '-'


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# this player plays a random move
def play_random_move(board: Board) -> Board:
    move = board.get_random_valid_move_index()
    return board.play_move(move)
