from BoggleGame.BoggleGameMode.FoggleBoggle import FoggleBoggle
from BoggleGame.BoggleGameMode.StandardBoggle import StandardBoggle
from MenuParser.MenuParser import MenuParser
from FileParser.SettingsParser import SettingsParser
from FileParser.DictionaryParser import DictionaryParser
from GameLogic.GameLogic import GameLogic


# This is the main file for the host application. It sets up a new run of the program and loads a menu
def main():
    SettingsParser.load_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))
    MenuParser.generate_menu()


def mock_game():
    SettingsParser.load_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))
    GameLogic.run_game(boogle_class=StandardBoggle, mockup=True)


def generate_board():
    SettingsParser.load_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))
    boogle_instance = FoggleBoggle(2, 4)
    print(boogle_instance.get_board_string(0, colored=False))


def find_words_in_board():
    SettingsParser.load_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))
    boogle_instance = StandardBoggle(1, 4)
    boogle_instance.game_paralell_process()
    print(boogle_instance.get_game_end_info())


if __name__ == '__main__':
    main()
