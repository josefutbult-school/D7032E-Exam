from BoggleGame.BoggleGameMode.BattleBoggle import BattleBoggle
from BoggleGame.BoggleGameMode.FoggleBoggle import FoggleBoggle
from BoggleGame.BoggleGameMode.StandardBoggle import StandardBoggle

from IO.HostIO import HostIO
from FileParser.SettingsParser import SettingsParser
from FileParser.DictionaryParser import DictionaryParser
from GameLogic.GameLogic import GameLogic

from .MenuItem import MenuItem


class MenuParser:
    @staticmethod
    def settings_standard(input_text, key):
        SettingsParser.set_setting(key=key, value=HostIO.get_input(f"Set {input_text}: "))

    @staticmethod
    def settings_standard_int(input_text, key, set=True):
        try:
            val = int(HostIO.get_input(f"Set {input_text}: "))
        except ValueError:
            print("Input is not an int")
            return
        if set:
            SettingsParser.set_setting(key=key, value=val)
        else:
            return val

    @staticmethod
    def board_size_setting(input_text, key):
        val = MenuParser.settings_standard_int(input_text, key, set=False)
        if val is not None:
            if val not in [4, 5]:
                print("The board size should be 4 or 5")
            else:
                SettingsParser.set_setting(key=key, value=val)

    @staticmethod
    def settings_standard_bool(input_text, key):
        val = HostIO.get_input(f"Set {input_text} (should be 1, true, True, 0, false or False): ")
        if val in ['1', 'true', 'True']:
            SettingsParser.set_setting(key=key, value=1)
        elif val in ['0', 'false', 'False']:
            SettingsParser.set_setting(key=key, value=0)
        else:
            HostIO.print("Input is not a bool")

    @staticmethod
    def settings_main_menu(exit_command):
        exit_command[0] = True
        SettingsParser.save_settings()
        DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))

    @staticmethod
    def generate_settings():
        exit_command = [False]

        while not exit_command[0]:
            menu_items = [
                MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['language'].capitalize()} "
                              f"{SettingsParser.get_setting('language')}",
                         key='l',
                         function=MenuParser.settings_standard,
                         args=("language", "language")),
                MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['board size'].capitalize()} "
                              f"{SettingsParser.get_setting('board_size')}x{SettingsParser.get_setting('board_size')}",
                         key='b',
                         function=MenuParser.board_size_setting,
                         args=("board size", "board_size")),
                MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['show solution'].capitalize()} "
                              f"{SettingsParser.get_setting('show_solution')}",
                         key='s',
                         function=MenuParser.settings_standard_bool,
                         args=("show solutions", "show_solution")),
                MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['number of players'].capitalize()} "
                              f"{SettingsParser.get_setting('number_players')}",
                         key='n',
                         function=MenuParser.settings_standard_int,
                         args=("number of players", "number_players")),
                MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['seconds per game'].capitalize()} "
                              f"{SettingsParser.get_setting('game_time')}",
                         key='t',
                         function=MenuParser.settings_standard_int,
                         args=("seconds per game", "game_time")),
                MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['generous'].capitalize()} boggle "
                              f"{SettingsParser.get_setting('generous_boggle')}",
                         key='g',
                         function=MenuParser.settings_standard_int,
                         args=("generous boggle", "generous_boggle")),
                MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['save'].capitalize()}",
                         args=(exit_command,),
                         key='q',
                         function=MenuParser.settings_main_menu),
            ]

            HostIO.display_settings_menu(menu_items)

    @staticmethod
    def generate_menu():
        while True:
            menu_items = [
                MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['play'].capitalize()} standard boggle",
                         key='0',
                         function=GameLogic.run_game,
                         args=(StandardBoggle,)),
                MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['play'].capitalize()} Battle boggle",
                         key='1',
                         function=GameLogic.run_game,
                         args=(BattleBoggle,)),
                MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['play'].capitalize()} Foggle boggle",
                         key='2',
                         function=GameLogic.run_game,
                         args=(FoggleBoggle,)),
                MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['settings'].capitalize()}",
                         key='s',
                         function=MenuParser.generate_settings),
                MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['quit'].capitalize()}",
                         key='q',
                         function=exit),
            ]
            HostIO.display_main_menu(menu_items)
