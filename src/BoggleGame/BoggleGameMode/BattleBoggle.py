from BoggleGame.BoardTypes.SingleBoardBoggle import SingleBoardBoggle
from BoggleGame.BoggleType.WordBoggleBase import WordBoggleBase


# This game mode is a word based mode where the different players share the same board
class BattleBoggle(WordBoggleBase, SingleBoardBoggle):
    def __init__(self, number_of_boards, board_size):
        super().__init__(number_of_boards, board_size)

    def check_move(self, board_id, move, generous_boggle, rules_args=None) -> tuple:
        return (True, "Word exists in wordlist!") if self._check_move(board_id=board_id,
                                                                      move=move,
                                                                      generous_boggle=generous_boggle) \
            else (False, "No such word in wordlist, or already taken by you or another player")

    def __str__(self):
        return "Battle Boggle"

    @staticmethod
    def get_name():
        return "Battle Boggle"
