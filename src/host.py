from BoggleGame.BoggleVariants.FoggleBoggle import FoggleBoggle
from BoggleGame.BoggleVariants.StandardBoggle import StandardBoggle
from MenuParser.menu_parser import generate_menu
from FileParser.SettingsParser import SettingsParser
from FileParser.DictionaryParser import DictionaryParser
from GameLogic.game_logic import run_game


def main():
    SettingsParser.load_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))
    generate_menu()


def mock_game():
    SettingsParser.load_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))
    run_game(boogle_class=StandardBoggle, mockup=True)


def generate_board():
    SettingsParser.load_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))
    boogle_instance = FoggleBoggle(2, 4)
    print(boogle_instance.get_board_string(0, colored=False))

    # boogle_instance.colored_text = False
    # instance = boogle_instance.get_board_string(0)
    # for row in instance:
    #     for instance in row:
    #         print(instance, end=' ')
    #     print('\n')
    # print(boogle_instance.check_move(board_id=0, move='1-1=0', generous_boggle=False))


if __name__ == '__main__':
    main()
