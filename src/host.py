from BoggleVariants.FoggleBoggle import FoggleBoggle
from MenuParser.menu_parser import generate_menu
from FileParser.SettingsParser import SettingsParser
from FileParser.DictionaryParser import DictionaryParser
from GameLogic.game_logic import run_game
from BoggleVariants.StandardBoggle import StandardBoggle


def main():
    SettingsParser.load_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))
    generate_menu()


def mock_game():
    SettingsParser.load_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))
    run_game(boogle_class=StandardBoggle, paralell_run=False, mockup=True)


def generate_board():
    SettingsParser.load_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))
    boogle_instance = FoggleBoggle(4)

    # boogle_instance.colored_text = False
    instance = boogle_instance.get_board_string()
    for row in instance:
        for instance in row:
            print(instance, end=' ')
        print('\n')
    print(boogle_instance.check_move(None, '1', ))


if __name__ == '__main__':
    main()
