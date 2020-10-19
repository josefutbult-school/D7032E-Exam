from random import choice

from BoggleGame.BoardTypes.MultipleBoardBoggle import MultipleBoardBoggle


class FoggleBoggle(MultipleBoardBoggle):
    def __init__(self, number_of_boards, board_size):
        super().__init__(number_of_boards, board_size)

    def create_board(self, board_size) -> list:
        board = super(FoggleBoggle, self).create_board(board_size)
        for row in board:
            for col in range(len(row)):
                row[col].value = str(choice(list(range(10))))
        return board

    def rules(self, board_id, move, rules_args=None) -> bool:
        if rules_args not in self.get_used_words(board_id):
            for char in rules_args:
                if char not in [str(i) for i in range(10)] + ['+', '-', '*', '/', '=']:
                    return False
            func = rules_args.split('=')
            if eval(func[0]) == eval(func[1]):
                self.get_used_words(board_id).append(rules_args)
                return True
        return False

    def check_move(self, board_id, move, rules_args=None) -> tuple:
        parsed_move = ''.join(list(filter(lambda char: char.isdigit(), move)))
        if move not in self.get_used_words(board_id) and \
                self._check_move(board_id=board_id, move=parsed_move, rules_args=move):
            return True, "Correct number!"
        return False, "No such number on the board, or number occupied, or incorrect"

    def get_points(self, move) -> int:
        res = ''.join(list(filter(lambda char: char in [str(i) for i in range(10)], list(move))))
        return super(FoggleBoggle, self).get_points(res)

    def get_game_info(self, board_id):
        return f"The numbers used already are: \n{' '.join(self.get_used_words(board_id))}"

    def __str__(self):
        return "Foggle Boggle"

    @staticmethod
    def get_name():
        return "Foggle Boggle"
