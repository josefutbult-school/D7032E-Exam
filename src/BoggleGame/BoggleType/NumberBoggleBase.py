from abc import ABC
from random import choice

from BoggleGame.BoggleBase.BoggleBase import BoggleBase


# This is an abstract class meant to be one of two implemented by a game mode. It allows the game mode
# to operate on numeric operations.
class NumberBoggleBase(BoggleBase, ABC):
    def __init__(self, number_of_boards, board_size):
        super().__init__(number_of_boards, board_size=4)

    # Creates a board. Notice that the board_size passed in is ignored and that the size instead is
    # statically set to 4
    def create_board(self, board_size, tile_config_name=None) -> list:
        return super(NumberBoggleBase, self).\
            create_board(board_size=4, tile_config_name='foggle16')

    # Uses the full move instead of the shortened one made in _check_move, provided in rules_args
    # to see if it is already used, if it is a correct arithmetic statement and that it is
    # mathematically correct.
    def rules(self, board_id, move, register_used_word, rules_args=None) -> bool:
        if rules_args not in self.get_used_words(board_id):
            for char in rules_args:
                if char not in [str(i) for i in range(10)] + ['+', '-', '*', '/', '=']:
                    return False
            func = rules_args.split('=')
            if len(func) > 1 and eval(func[0]) == eval(func[1]):
                self.get_used_words(board_id).append(rules_args)
                return True
        return False

    # Adds an extra layer to the _check_move functionality of BoggleBase, stripping the operators from the move and
    # provides the full unaltered move as arguments to the rules function.
    def _check_move(self, move, board_id, generous_boggle, rules_args=None, register_used_word=True) -> bool:
        parsed_move = ''.join(list(filter(lambda char: char.isdigit(), move)))
        if move not in self.get_used_words(board_id) and \
                super(NumberBoggleBase, self)._check_move(board_id=board_id,
                                                          move=parsed_move,
                                                          rules_args=move,
                                                          generous_boggle=generous_boggle):
            return True
        return False

    # Strips the operators from a move before calculating the score
    def get_points(self, move) -> int:
        res = ''.join(list(filter(lambda char: char in [str(i) for i in range(10)], list(move))))
        return super(NumberBoggleBase, self).get_points(res)

    def get_game_info(self, board_id):
        return f"The numbers used already are: \n{' '.join(self.get_used_words(board_id))}"
