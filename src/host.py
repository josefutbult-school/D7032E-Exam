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


if __name__ == '__main__':
    mock_game()
