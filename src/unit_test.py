import unittest

from os.path import isdir, isfile

from BoggleGame.BoggleGameMode.BattleBoggle import BattleBoggle
from BoggleGame.BoggleGameMode.FoggleBoggle import FoggleBoggle
from BoggleGame.BoggleGameMode.StandardBoggle import StandardBoggle
from FileParser.path import get_root_dir
from FileParser.SettingsParser import SettingsParser
from FileParser.DictionaryParser import DictionaryParser
from GameLogic.GameLogic import GameLogic
from IO.HostIO import HostIO


class DirTest(unittest.TestCase):
    def test_root_dir(self):
        self.assertTrue(isdir(get_root_dir()))

    def test_incorrect_json_exists(self):
        path = get_root_dir() / 'tests' / 'test_json_incorrect.json'
        self.assertTrue(isfile(path))

    def test_incorrect_settings_exists(self):
        path = get_root_dir() / 'tests' / 'test_settings_incorrect_format.json'
        self.assertTrue(isfile(path))

    def test_incorrect_meta_json_exists(self):
        path = get_root_dir() / 'tests' / 'test_dict_json_incorrect' / 'meta.json'
        self.assertTrue(isfile(path))

    def test_incorrect_dict_meta_exists(self):
        path = get_root_dir() / 'tests' / 'test_dict_format_incorrect' / 'meta.json'
        self.assertTrue(isfile(path))

    def test_incorrect_dict_exists(self):
        path = get_root_dir() / 'tests' / 'test_dict_format_incorrect' / 'dict.txt'
        self.assertTrue(isfile(path))


class SettingsTest(unittest.TestCase):
    def test_settings_wrong_filepath(self):
        path = '/this_dosnt_exist'
        try:
            SettingsParser.load_settings(path, silent=True)
        except SystemExit as cm:
            self.assertEqual(cm.code, 1)

    def test_settings_incorrect_json(self):
        path = get_root_dir() / 'tests' / 'test_json_incorrect.json'
        try:
            SettingsParser.load_settings(path, silent=True)
        except SystemExit as cm:
            self.assertEqual(cm.code, 2)

    def test_settings_incorrect_format(self):
        path = get_root_dir() / 'tests' / 'test_settings_incorrect_format.json'
        try:
            SettingsParser.load_settings(path, silent=True)
        except SystemExit as cm:
            self.assertEqual(cm.code, 3)

    def test_settings_correct(self):
        try:
            SettingsParser.load_settings(silent=True)
            success = True
        except SystemExit:
            success = False

        self.assertTrue(success)


class DictionaryTest(unittest.TestCase):
    def test_dictionary_wrong_filepath(self):
        path = '/this_dosnt_exist'
        try:
            DictionaryParser.load_dictionary(path, silent=True)
        except SystemExit as cm:
            self.assertEqual(cm.code, 4)

    def test_dictionary_incorrect_json(self):
        path = get_root_dir() / 'tests' / 'test_dict_json_incorrect'
        try:
            DictionaryParser.load_dictionary(path, silent=True)
        except SystemExit as cm:
            self.assertEqual(cm.code, 5)

    def test_dictionary_incorrect_files_format(self):
        path = get_root_dir() / 'tests' / 'test_dict_format_incorrect'
        try:
            DictionaryParser.load_dictionary(path, silent=True)
        except SystemExit as cm:
            self.assertEqual(cm.code, 6)

    def test_dictionary_correct(self):
        SettingsParser.load_settings(silent=True)
        try:
            DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'), silent=True)
            success = True
        except SystemExit:
            success = False

        self.assertTrue(success)


def check_winner(boggle_instance, words, time=1, further_words=[]):
    SettingsParser.set_setting('game_time', time)

    moves = [[words] if words is not None else [], further_words]

    return GameLogic.run_game(boggle_class=StandardBoggle,
                              mockup=True,
                              moves=moves,
                              predefined_boggle_instance=boggle_instance)


def standard_setup():
    SettingsParser.load_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))
    SettingsParser.set_setting('generous_boggle', False)
    HostIO.set_terminal_output(False)


def load_compleat_language():
    path = get_root_dir() / 'tests' / 'test_dict_compleat_lang'
    DictionaryParser.load_dictionary('complete lang', language_dir=path, silent=True)


def load_uncompleat_language():
    path = get_root_dir() / 'tests' / 'test_dict_uncompleat_lang'
    DictionaryParser.load_dictionary('complete lang', language_dir=path, silent=True)


def load_minimal_language():
    path = get_root_dir() / 'tests' / 'test_dict_minimal_lang'
    DictionaryParser.load_dictionary('complete lang', language_dir=path, silent=True)


class BaseRequirementsTest(unittest.TestCase):

    # Requirement 1
    def test_run_one_player(self):
        standard_setup()
        SettingsParser.set_setting('number_players', 1)
        # Return code if the amount of players are incorrect
        self.assertEqual(GameLogic.run_game(StandardBoggle, mockup=True),
                         -1,
                         msg="The game was started with only one player")

    # Requirement 2
    def test_randomly_rolled(self):
        standard_setup()
        boards = (StandardBoggle(number_of_boards=1, board_size=4).get_board(0),
                  StandardBoggle(number_of_boards=1, board_size=4).get_board(0))

        unique = False
        for row in range(len(boards[0])):
            for col in range(len(boards[0][row])):
                if boards[0][row][col].value != boards[1][row][col].value:
                    unique = True

        self.assertTrue(unique, msg="The boards generated are not unique")

    def move_check(self, positions, output_text=""):
        standard_setup()
        standard_boggle = StandardBoggle(number_of_boards=1, board_size=4)

        standard_boggle.set_board_value(position=positions[0], value='c')
        standard_boggle.set_board_value(position=positions[1], value='o')
        standard_boggle.set_board_value(position=positions[2], value='w')

        # PlayerIO.set_mockup(True)
        # PlayerIO.write_player_gameboard(0, standard_boggle.get_board_string(board_id=0), "", 4)
        self.assertTrue(standard_boggle._check_move(move='cow',
                                                    board_id=0,
                                                    generous_boggle=False,
                                                    register_used_word=False),
                        msg=output_text)

        standard_boggle.set_board_value(position=positions[2], value='c')
        standard_boggle.set_board_value(position=positions[1], value='o')
        standard_boggle.set_board_value(position=positions[0], value='w')

        self.assertTrue(standard_boggle._check_move(move='cow',
                                                    board_id=0,
                                                    generous_boggle=False,
                                                    register_used_word=False),
                        msg=output_text)

    # Requirement 3
    def test_horizontal_move(self):
        self.move_check([(0, 0), (1, 0), (2, 0)])

    def test_vertical_move(self):
        self.move_check([(0, 0), (0, 1), (0, 2)])

    def test_diagonal_move(self):
        self.move_check([(0, 0), (1, 1), (2, 2)],
                        output_text="This test has a tendency to fail about every "
                                    "tenth time. Try rerunning and see if the fail "
                                    "remains.")

    # Requirement 4
    def test_winner(self):
        standard_setup()

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(0, 0), value='c')
        standard_boggle.set_board_value(position=(0, 1), value='o')
        standard_boggle.set_board_value(position=(0, 2), value='w')

        id, points = check_winner(standard_boggle, 'cow')
        self.assertEqual(id, 0)

    # Requirement 5
    def test_winner_length(self):
        standard_setup()

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(0, 0), value='i')
        standard_boggle.set_board_value(position=(0, 1), value='f')

        id, points = check_winner(standard_boggle, 'if')
        self.assertEqual(points, 0)

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(0, 0), value='c')
        standard_boggle.set_board_value(position=(0, 1), value='o')
        standard_boggle.set_board_value(position=(0, 2), value='w')

        id, points = check_winner(standard_boggle, 'cow')
        self.assertEqual(points, 1)

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(0, 0), value='c')
        standard_boggle.set_board_value(position=(0, 1), value='o')
        standard_boggle.set_board_value(position=(0, 2), value='w')
        standard_boggle.set_board_value(position=(0, 3), value='s')

        id, points = check_winner(standard_boggle, 'cows')
        self.assertEqual(points, 1)

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(0, 0), value='m')
        standard_boggle.set_board_value(position=(0, 1), value='a')
        standard_boggle.set_board_value(position=(0, 2), value='t')
        standard_boggle.set_board_value(position=(0, 3), value='c')
        standard_boggle.set_board_value(position=(1, 3), value='h')

        id, points = check_winner(standard_boggle, 'match')
        self.assertEqual(points, 2)

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(0, 0), value='w')
        standard_boggle.set_board_value(position=(0, 1), value='i')
        standard_boggle.set_board_value(position=(0, 2), value='n')
        standard_boggle.set_board_value(position=(0, 3), value='n')
        standard_boggle.set_board_value(position=(1, 3), value='e')
        standard_boggle.set_board_value(position=(1, 2), value='r')

        id, points = check_winner(standard_boggle, 'winner')
        self.assertEqual(points, 3)

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(0, 0), value='l')
        standard_boggle.set_board_value(position=(0, 1), value='e')
        standard_boggle.set_board_value(position=(0, 2), value='t')
        standard_boggle.set_board_value(position=(0, 3), value='t')
        standard_boggle.set_board_value(position=(1, 3), value='e')
        standard_boggle.set_board_value(position=(1, 2), value='r')
        standard_boggle.set_board_value(position=(1, 1), value='s')

        id, points = check_winner(standard_boggle, 'letters')
        self.assertEqual(points, 5)

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(0, 0), value='p')
        standard_boggle.set_board_value(position=(0, 1), value='o')
        standard_boggle.set_board_value(position=(0, 2), value='s')
        standard_boggle.set_board_value(position=(0, 3), value='s')
        standard_boggle.set_board_value(position=(1, 3), value='i')
        standard_boggle.set_board_value(position=(1, 2), value='b')
        standard_boggle.set_board_value(position=(1, 1), value='l')
        standard_boggle.set_board_value(position=(1, 0), value='e')

        id, points = check_winner(standard_boggle, 'possible')
        self.assertEqual(points, 11)

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(0, 0), value='a')
        standard_boggle.set_board_value(position=(0, 1), value='c')
        standard_boggle.set_board_value(position=(0, 2), value='t')
        standard_boggle.set_board_value(position=(0, 3), value='i')
        standard_boggle.set_board_value(position=(1, 3), value='v')
        standard_boggle.set_board_value(position=(1, 2), value='i')
        standard_boggle.set_board_value(position=(1, 1), value='t')
        standard_boggle.set_board_value(position=(1, 0), value='i')
        standard_boggle.set_board_value(position=(2, 0), value='e')
        standard_boggle.set_board_value(position=(3, 0), value='s')

        id, points = check_winner(standard_boggle, 'activities')
        self.assertEqual(points, 11)

    # Requirement 6
    def test_qu(self):
        standard_setup()
        self.assertEqual(StandardBoggle(2, 4).get_points('quest'), 2)

    # Requirement 7
    def test_reused_word(self):
        standard_setup()

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(0, 0), value='c')
        standard_boggle.set_board_value(position=(0, 1), value='o')
        standard_boggle.set_board_value(position=(0, 2), value='w')

        standard_boggle._check_move(move='cow',
                                    board_id=0,
                                    generous_boggle=False)

        self.assertTrue(not standard_boggle._check_move(move='cow',
                                                        board_id=0,
                                                        generous_boggle=False))

    # Requirement 8
    def test_change_dict(self):
        load_compleat_language()

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(1, 0), value='n')
        standard_boggle.set_board_value(position=(1, 1), value='o')
        standard_boggle.set_board_value(position=(1, 2), value='t')

        self.assertTrue(standard_boggle._check_move(move='not',
                                                    board_id=0,
                                                    generous_boggle=False))

        load_uncompleat_language()
        self.assertTrue(not standard_boggle._check_move(move='not',
                                                        board_id=0,
                                                        generous_boggle=False))

    # Requirement 9
    def test_get_word_list(self):
        standard_setup()
        load_minimal_language()
        HostIO.set_terminal_output(True)

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(0, 0), value='w')
        standard_boggle.set_board_value(position=(0, 1), value='o')
        standard_boggle.set_board_value(position=(0, 2), value='r')
        standard_boggle.set_board_value(position=(0, 3), value='d')

        standard_boggle.game_paralell_process()
        self.assertCountEqual(standard_boggle.get_words_in_board(), ['word'])

    # Requirement 10
    def check_grid_size(self, size):
        standard_setup()
        SettingsParser.set_setting('board_size', size)
        if size not in [4, 5]:
            with self.assertRaises(IOError):
                StandardBoggle(number_of_boards=2, board_size=size)
        else:
            try:
                StandardBoggle(number_of_boards=2, board_size=size)
            except IOError:
                self.fail()

    def test_grid_sizes(self):
        self.check_grid_size(3)
        self.check_grid_size(4)
        self.check_grid_size(5)
        self.check_grid_size(6)

    # Requirement 11
    def test_dice_configurations(self):
        load_compleat_language()
        first_board = StandardBoggle(number_of_boards=2, board_size=4).get_board_string(0, colored=False)

        load_uncompleat_language()
        second_board = StandardBoggle(number_of_boards=2, board_size=4).get_board_string(0, colored=False)

        not_unique = False
        for row in range(len(first_board)):
            for col in range(len(first_board[row])):
                if first_board[row][col] == second_board[row][col]:
                    not_unique = True

        self.assertTrue(not not_unique)

    # Requirement 12
    def test_reused_dice(self):
        standard_setup()

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(1, 0), value='i')
        standard_boggle.set_board_value(position=(1, 1), value='n')
        standard_boggle.set_board_value(position=(2, 0), value='t')

        self.assertTrue(not standard_boggle._check_move(move='init',
                                                        board_id=0,
                                                        generous_boggle=False))

    # Requirement 13
    def test_generous_reused_dice(self):
        standard_setup()

        standard_boggle = StandardBoggle(number_of_boards=2, board_size=4)
        standard_boggle.set_board_value(position=(0, 0), value='a')
        standard_boggle.set_board_value(position=(1, 0), value='l')
        standard_boggle.set_board_value(position=(2, 0), value='k')
        standard_boggle.set_board_value(position=(2, 1), value='y')

        self.assertTrue(standard_boggle._check_move(move='alkyl',
                                                    board_id=0,
                                                    generous_boggle=True))

    # Requirement 15
    def test_reused_battle_word(self):
        standard_setup()

        battle_boggle = BattleBoggle(number_of_boards=2, board_size=4)
        battle_boggle.set_board_value(position=(0, 0), value='c')
        battle_boggle.set_board_value(position=(0, 1), value='o')
        battle_boggle.set_board_value(position=(0, 2), value='w')

        battle_boggle._check_move(move='cow',
                                  board_id=0,
                                  generous_boggle=False)

        self.assertTrue(not battle_boggle._check_move(move='cow',
                                                      board_id=1,
                                                      generous_boggle=False))

    # Requirement 16
    def test_see_players_word(self):
        standard_setup()

        battle_boggle = BattleBoggle(number_of_boards=2, board_size=4)
        battle_boggle.set_board_value(position=(0, 0), value='c')
        battle_boggle.set_board_value(position=(0, 1), value='o')
        battle_boggle.set_board_value(position=(0, 2), value='w')

        battle_boggle._check_move(move='cow',
                                  board_id=0,
                                  generous_boggle=False)

        self.assertTrue("cow" in battle_boggle.get_game_info(1))

    # Requirement 17
    def test_none_arithmetic_operation(self):
        standard_setup()

        foggle_boggle = FoggleBoggle(number_of_boards=2, board_size=4)
        foggle_boggle.set_board_value(position=(0, 0), value='1')
        foggle_boggle.set_board_value(position=(0, 1), value='1')
        foggle_boggle.set_board_value(position=(0, 2), value='2')

        self.assertTrue(not foggle_boggle._check_move(move='fail1+1=2',
                                                      board_id=0,
                                                      generous_boggle=False))

    def test_false_arithmetic_operation(self):
        standard_setup()

        foggle_boggle = FoggleBoggle(number_of_boards=2, board_size=4)
        foggle_boggle.set_board_value(position=(0, 0), value='1')
        foggle_boggle.set_board_value(position=(0, 1), value='1')
        foggle_boggle.set_board_value(position=(0, 2), value='1')

        self.assertTrue(not foggle_boggle._check_move(move='1+1=1',
                                                      board_id=0,
                                                      generous_boggle=False))


if __name__ == '__main__':
    unittest.main()
