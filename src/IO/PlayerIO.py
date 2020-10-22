from random import seed, random, choice, randint
from datetime import datetime
from string import ascii_lowercase

from Networking.HostNetworking import HostNetworking
from IO.HostIO import HostIO
from FileParser.SettingsParser import SettingsParser

TEST_WORDS = ['Cow', 'Moose', 'Geese', 'Goat', 'Toad']
SUCCESS_RATE = 0.5


class PlayerIO:
    mockup = False

    @staticmethod
    def set_mockup(state=False):
        if state:
            seed(datetime.now())

        PlayerIO.mockup = state

    @staticmethod
    def get_move(player_id):
        if not PlayerIO.mockup:
            return HostNetworking.player_read(player_id, "Insert word: ")
        else:
            if random() >= SUCCESS_RATE:
                word = choice(TEST_WORDS)
            else:
                word = ''.join([choice(ascii_lowercase) for i in range(randint(3, 6))])
            PlayerIO.write_player(player_id=player_id, out=f'Tries word {word}')
            return word

    @staticmethod
    def write_player_gameboard(player_id, board, game_info, board_size):
        if board is not None:
            gameboard = f"\n+{'-' * (board_size * 2 - 1)}+\n"
            for row in range(board_size):
                for column in range(board_size):
                    gameboard += f"|{board[row][column]}"
                gameboard += f"|\n+{'-' * (board_size * 2 - 1)}+\n"
        else:
            gameboard = ''
        PlayerIO.write_player(player_id=player_id, out=gameboard + game_info)

    @staticmethod
    def write_player(player_id, out):
        if not PlayerIO.mockup:
            HostNetworking.player_write(player_id, out + ('' if out != '' and out[-1] == '\n' else '\n'))
        else:
            HostIO.print(f'From player {player_id}\'s terminal: \"{out}\"', clear_screen=False, direct_continue=True)

    @staticmethod
    def clear_player(player_id):
        if not PlayerIO.mockup:
            HostNetworking.player_write(player_id, '\n' * 20)
