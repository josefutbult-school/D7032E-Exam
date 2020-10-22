from BoggleGame.BoardTypes.MultipleBoardBoggle import MultipleBoardBoggle
from BoggleGame.BoggleBase.NumberBoggleBase import NumberBoggleBase


class FoggleBoggle(NumberBoggleBase, MultipleBoardBoggle):
    def __init__(self, number_of_boards, board_size):
        super().__init__(number_of_boards, board_size)

    def check_move(self, board_id, move, generous_boggle, rules_args=None) -> tuple:
        return (True, "Correct number!") if self._check_move(board_id=board_id,
                                                             move=move,
                                                             generous_boggle=generous_boggle) \
            else (False, "No such number on the board, or number occupied, or incorrect")

    def __str__(self):
        return "Foggle Boggle"

    @staticmethod
    def get_name():
        return "Foggle Boggle"
