from itertools import product
from random import seed, choice
from datetime import datetime
from time import sleep

from BoggleGame.BoggleBase.BoogleTile import BoggleTile
from FileParser.DictionaryParser import DictionaryParser

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'


# This class is a top parent class for the different boogle variants.
# It defines all the methods needed for any subclass boggle variant to work, and does the mast heavy lifting
class BoggleBase:
    store_traversed_tiles = True

    def __init__(self, number_of_boards, board_size):
        seed(datetime.now())
        self.board_size = board_size

    def traverse_board(self, board, move, previous_position):
        if len(move) > 0:
            positions = list(product([previous_position[0] - 1,
                                      previous_position[0],
                                      previous_position[0] + 1],
                                     [previous_position[1] - 1,
                                      previous_position[1],
                                      previous_position[1] + 1]
                                     ))
            positions = list(filter(lambda position: 0 <= position[0] < len(board) and \
                                                     0 <= position[1] < len(board), positions))

            # TODO: This wont allow checking words with two of the same character as neighbor. It will just try the
            #  first instance
            for position in positions:
                if board[position[0]][position[1]].value == move[0] and \
                        not board[position[0]][position[1]].traversed:
                    board[position[0]][position[1]].traversed = True
                    return [board[position[0]][position[1]]] + \
                           self.traverse_board(move=move[1:], board=board, previous_position=position)

        return []

    def get_board_size(self):
        return self.board_size

    def get_board_string(self, board_id, colored=True):
        if colored:
            return [[f"{FAIL if instance.used_in_word else OKGREEN}{instance.value}{ENDC}"
                     for instance in row] for row in self.get_board(board_id)]
        return [[instance.value for instance in row] for row in self.get_board(board_id)]

    # The following functions should/can be implemented in inherited classes

    # This is the check for whether a word (move) exists on a board. It locates every tile with the fist character
    # in the move, and runs the recursive traverse_board method from that position to find a word. It should be
    # called from the check_move method.
    def _check_move(self, move, board_id, generous_boggle, rules_args=None, register_used_word=True) -> bool:
        if move == '':
            return False

        letter, remainder = self.split_move(move)
        board = self.get_board(board_id)
        for row in range(len(board)):
            for column in range(len(board[row])):
                if letter == board[row][column].value and not board[row][column].traversed:
                    if not generous_boggle:
                        board[row][column].traversed = True
                    tiles = [board[row][column]] + self.traverse_board(board, remainder, (row, column))
                    res = ''.join([str(instance.value) for instance in tiles])
                    if move == res and self.rules(board_id, move, register_used_word, rules_args):
                        for instance in tiles:
                            instance.traversed = False
                            if register_used_word:
                                instance.used_in_word = True
                        return True

                    for instance in tiles:
                        instance.traversed = False

        return False

    def get_points(self, move) -> int:
        if len(move) <= 2:
            return 0
        elif len(move) <= 4:
            return 1
        elif len(move) == 5:
            return 2
        elif len(move) == 6:
            return 3
        elif len(move) == 7:
            return 5
        return 11

    # This is called when either of the board type classes initializes and creates the number of boards specified in
    # that class. It should populate a board matrix sized after the board_size variable, using the tiles specified
    # in the current languages meta file.
    def create_board(self, board_size, tile_config_name=None) -> list:
        tile_config = [[char.lower() for char in row] for row in
                       DictionaryParser.get_dict_meta('tile_configs')[tile_config_name]]
        return [[BoggleTile(value=choice(tile_config.pop(0))) for column in range(board_size)] for row in
                range(board_size)]

    # The result of this is written after the game board to the players for every turn.
    def get_game_info(self, board_id):
        return ""

    # The result of this is written at the end of the game to all the players.
    def get_game_end_info(self):
        return ""

    # This function is run as a separate process at the start of a game. It can be used to do heavy processing
    # in the background.
    def game_paralell_process(self):
        pass

    # This functions is used in the _check_move to separate the first tile out from a move, and the rest of the move.
    # It can be used in case a special combination of characters should be seen as a single tile, for example 'Qu'.
    def split_move(self, move) -> tuple:
        return move[0], move[1:]

    # The following functions are abstract, and has to be implemented by a none abstract child class.

    # This function runs on the input provided by a player in game_logic. It should run the _check_move function,
    # and extra functionality if needed, and return whether the move was successful and a message that should be
    # given to the player.
    def check_move(self, board_id, move, generous_boggle, rules_args=None) -> bool:
        raise NotImplementedError()

    # This function assesses whether a move, that was correct on the board, is correct according to the game mode.
    # It receives the args provided to to _check_move and can use these in the manner that the specific mode requires.
    def rules(self, board_id, move, register_used_word, rules_args=None) -> bool:
        raise NotImplementedError()

    # get_board and get_used_words needs to be specified by the board types child classes.
    def get_board(self, board_id) -> list:
        raise NotImplementedError()

    def get_used_words(self, board_id) -> list:
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    @staticmethod
    def get_name():
        raise NotImplementedError()

    def set_board_value(self, position, value):
        raise NotImplementedError()
