from BoggleGame.BoardTypes.SingleBoardBoggle import SingleBoardBoggle
from BoggleGame.BoggleBase.WordBoggleBase import WordBoggleBase


class BattleBoggle(WordBoggleBase, SingleBoardBoggle):
    def __init__(self, number_of_boards, board_size):
        super().__init__(number_of_boards, board_size)

    def check_move(self, board_id, move, rules_args=None) -> tuple:
        return (True, "Word exists in wordlist!") if self._check_move(board_id=board_id, move=move) \
            else (False, "No such word in wordlist, or already taken by you or another player")

    def __str__(self):
        return "Battle Boggle"

    @staticmethod
    def get_name():
        return "Battle Boggle"
