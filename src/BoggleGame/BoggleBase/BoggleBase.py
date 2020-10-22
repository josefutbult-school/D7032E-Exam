from itertools import product
from random import seed, choice
from datetime import datetime

from BoggleGame.BoggleBase.BoogleTile import BoggleTile
from FileParser.DictionaryParser import DictionaryParser

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'


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

    def _check_move(self, move, board_id, generous_boggle, rules_args=None) -> bool:
        if move == '':
            return False

        board = self.get_board(board_id)
        for row in range(len(board)):
            for column in range(len(board[row])):
                if move[0] == board[row][column].value and not board[row][column].traversed:
                    if not generous_boggle:
                        board[row][column].traversed = True
                    tiles = [board[row][column]] + self.traverse_board(board, move[1:], (row, column))
                    res = ''.join([str(instance.value) for instance in tiles])
                    if move == res and self.rules(board_id, move, rules_args):
                        for instance in tiles:
                            instance.traversed = False
                            instance.used_in_word = True
                        return True

                    for instance in tiles:
                        instance.traversed = False

        return False

    def get_board_size(self):
        return self.board_size

    def get_board_string(self, board_id, colored=True):
        if colored:
            return [[f"{FAIL if instance.used_in_word else OKGREEN}{instance.value}{ENDC}"
                 for instance in row] for row in self.get_board(board_id)]
        return [[instance.value for instance in row] for row in self.get_board(board_id)]

    # The following functions should/can be implemented in inherited classes
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

    def check_move(self, board_id, move, generous_boggle, rules_args=None) -> bool:
        raise NotImplementedError()

    def rules(self, board_id, move, rules_args=None) -> bool:
        raise NotImplementedError()

    def get_game_info(self, board_id):
        return ""

    def create_board(self, board_size, tile_config_name=None) -> list:
        tile_config = [[char.lower() for char in row] for row in
                       DictionaryParser.get_dict_meta('tile_configs')[tile_config_name]]
        return [[BoggleTile(value=choice(tile_config.pop(0))) for column in range(board_size)] for row in range(board_size)]

    def get_board(self, board_id) -> list:
        raise NotImplementedError()

    def get_used_words(self, board_id) -> list:
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    @staticmethod
    def get_name():
        raise NotImplementedError()
