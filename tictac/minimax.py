import random

from tictac.tictac.board import Board
from tictac.tictac.board import BoardCache
from tictac.tictac.board import CELL_O
from tictac.tictac.board import is_empty

cache = BoardCache()  # global cache for minimax player


def create_minimax_player(randomize):
    def play(board: Board) -> Board:
        return play_minimax_move(board, randomize)

    return play


def play_minimax_move(board: Board, randomize=False) -> Board:
    move_value_pairs = get_move_value_pairs(board)
    move = filter_best_move(board, move_value_pairs, randomize)
    return board.play_move(move)


def get_move_value_pairs(board):
    valid_move_indexes = board.get_valid_move_indexes()
    assert not is_empty(valid_move_indexes), "never call with an end position"

    move_value_pairs = [(m, get_position_value(board.play_move(m)))
                        for m in valid_move_indexes]

    return move_value_pairs


# The recursion that traverse the game tree is:
#   get_position_value() -> calculate_position_value() -> get_position_value()
#
def get_position_value(board):
    result, found = cache.get_for_position(board)
    if found:
        return result[0]

    position_value = calculate_position_value(board)

    cache.set_for_position(board, position_value)

    return position_value


def calculate_position_value(board):
    # the end of recursion is "game over"
    if board.is_game_over():
        return board.get_game_result()

    valid_move_indexes = board.get_valid_move_indexes()

    values = [get_position_value(board.play_move(m)) for m in valid_move_indexes]
    # the low level minimax algorithm
    min_or_max = choose_min_or_max_for_comparison(board)
    position_value = min_or_max(values)

    return position_value


def filter_best_move(board, move_value_pairs, randomize):
    min_or_max = choose_min_or_max_for_comparison(board)
    move, value = min_or_max(move_value_pairs, key=lambda mvp: mvp[1])
    if not randomize:
        return move

    best_move_value_pairs = [mvp for mvp in move_value_pairs
                             if mvp[1] == value]
    chosen_move, _ = random.choice(best_move_value_pairs)
    return chosen_move


def choose_min_or_max_for_comparison(board):
    turn = board.get_turn()
    # if it is X's turn, use max. Aka prefers the winning move.
    # if it is O's turn, use min. Aka prefers the losing move.
    return min if turn == CELL_O else max
