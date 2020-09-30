from IO.HostIO import HostIO
from MenuParser.MenuItem import MenuItem
from MenuParser.menu_parser import generate_menu
from FileParser.SettingsParser import SettingsParser
from FileParser.DictionaryParser import DictionaryParser
# from Player.Player import Player


def main():
    SettingsParser.load_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))
    generate_menu()


if __name__ == '__main__':
    main()
