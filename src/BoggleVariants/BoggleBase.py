from itertools import product
from random import seed
from datetime import datetime

from .BoogleTile import BoggleTile

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'


class BoggleBase:
    store_traversed_tiles = True

    def __init__(self, board_size):
        seed(datetime.now())
        self.board = [[BoggleTile() for column in range(board_size)] for row in range(board_size)]

    def get_board(self):
        return self.board

    def get_board_string(self):
        return [[f"{FAIL if instance.traversed else OKGREEN}{instance}{ENDC}"
                 for instance in row] for row in self.board]

    def traverse_board(self, move, previous_position):
        if len(move) > 0:
            positions = list(product([previous_position[0] - 1,
                                      previous_position[0],
                                      previous_position[0] + 1],
                                     [previous_position[1] - 1,
                                      previous_position[1],
                                      previous_position[1] + 1]
                                     ))
            positions = list(filter(lambda position: 0 <= position[0] < len(self.board) and \
                                                     0 <= position[1] < len(self.board), positions))

            # TODO: This wont allow checking words with two of the same character as neighbor. It will just try the
            #  first instance
            for position in positions:
                if self.board[position[0]][position[1]].value == move[0] and \
                        not self.board[position[0]][position[1]].traversed:
                    self.board[position[0]][position[1]].traversed = True
                    return [self.board[position[0]][position[1]]] + \
                           self.traverse_board(move=move[1:], previous_position=position)

        return []

    def _check_move(self, move, rules_args=None) -> bool:
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if move[0] == self.board[row][column].value and not self.board[row][column].traversed:
                    print("Here")
                    self.board[row][column].traversed = True
                    tiles = [self.board[row][column]] + self.traverse_board(move[1:], (row, column))
                    res = ''.join([str(instance.value) for instance in tiles])
                    print(f"Res: {res}")
                    if move == res and self.rules(move, rules_args):
                        if not self.store_traversed_tiles:
                            for instance in tiles:
                                instance.traversed = False
                        return True

                    for instance in tiles:
                        instance.traversed = False

        return False

    def check_move(self, player, move, rules_args=None) -> bool:
        raise NotImplementedError()

    def rules(self, move, rules_args=None):
        raise NotImplementedError()

    def get_game_info(self):
        return ""
