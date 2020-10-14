from random import choice, seed
from datetime import datetime
from .BoggleBase import BoggleBase


class FoggleBoggle(BoggleBase):
    def __init__(self, board_size):
        super().__init__(board_size)
        seed(datetime.now())
        for row in self.board:
            for col in range(len(row)):
                row[col].value = str(choice(list(range(10))))

        self.used_words = []

    def rules(self, move, rules_args=None):
        if rules_args not in self.used_words:
            func = rules_args.split('=')
            ret = eval(func[0]) == eval(func[1])
            print(ret)
            return ret

    def check_move(self, player, move, rules_args=None) -> tuple:
        parsed_move = ''.join(list(filter(lambda char: char.isdigit(), move)))
        print(parsed_move)
        if move not in self.used_words and super(FoggleBoggle, self)._check_move(move=parsed_move, rules_args=move):
            self.used_words.append(move)
            return True, "Correct number!"
        return False, "No such word in wordlist, or word occupied"

    def get_game_info(self):
        return f"The numbers used already are: \n{' '.join(self.used_words)}"
