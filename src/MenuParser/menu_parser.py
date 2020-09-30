from BoggleVariants.BoggleBase import BoggleBase
from BoggleVariants.BattleBoggle import BattleBoggle
from BoggleVariants.FoggleBoggle import FoggleBoggle
from BoggleVariants.GenerousBoggle import GenerousBoggle
from BoggleVariants.StandardBoggle import StandardBoggle

from IO.HostIO import HostIO
from FileParser.SettingsParser import SettingsParser
from FileParser.DictionaryParser import DictionaryParser
from Networking.HostNetworking import HostNetworking
from GameLogic.game_logic import run_game

from .MenuItem import MenuItem


def settings_standard(args):
    input_text, key = args
    SettingsParser.set_setting(key=key, value=HostIO.get_input(f"Set {input_text}: "))


def settings_standard_int(args):
    input_text, key = args
    try:
        val = int(HostIO.get_input(f"Set {input_text}: "))
    except ValueError:
        print("Input is not an int")
        return

    SettingsParser.set_setting(key=key, value=val)


def settings_standard_bool(args):
    input_text, key = args
    val = HostIO.get_input(f"Set {input_text} (should be 1, true, True, 0, false or False): ")
    if val in ['1', 'true', 'True']:
        SettingsParser.set_setting(key=key, value=True)
    elif val in ['0', 'false', 'False']:
        SettingsParser.set_setting(key=key, value=False)
    else:
        HostIO.print("Input is not a bool")


def settings_main_menu(exit_command):
    exit_command[0] = True
    SettingsParser.save_settings()
    DictionaryParser.load_dictionary(language=SettingsParser.get_setting('language'))


def generate_settings():
    exit_command = [False]

    while not exit_command[0]:
        menu_items = [
            MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['language'].capitalize()} "
                          f"{SettingsParser.get_setting('language')}",
                     key='l',
                     function=settings_standard,
                     args=("language", "language")),
            MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['board size'].capitalize()} "
                          f"{SettingsParser.get_setting('board_size')}x{SettingsParser.get_setting('board_size')}",
                     key='b',
                     function=settings_standard_int,
                     args=("board size", "board_size")),
            MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['show solution'].capitalize()} "
                          f"{SettingsParser.get_setting('show_solution')}",
                     key='s',
                     function=settings_standard_bool,
                     args=("show solutions", "show_solution")),
            MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['number of players'].capitalize()} "
                          f"{SettingsParser.get_setting('number_players')}",
                     key='n',
                     function=settings_standard_int,
                     args=("number of players", "number_players")),
            MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['seconds per game'].capitalize()} "
                          f"{SettingsParser.get_setting('game_time')}",
                     key='t',
                     function=settings_standard_int,
                     args=("seconds per game", "game_time")),
            MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['save'].capitalize()}",
                     args=exit_command,
                     key='q',
                     function=settings_main_menu),
        ]

        HostIO.display_settings_menu(menu_items)


def generate_menu():
    while True:
        menu_items = [
            MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['play'].capitalize()} standard boggle",
                     key='0',
                     function=run_game,
                     args=StandardBoggle),
            MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['play'].capitalize()} Generous boggle",
                     key='1',
                     function=GenerousBoggle),
            MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['play'].capitalize()} Battle boggle",
                     key='2',
                     function=BattleBoggle),
            MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['play'].capitalize()} Foggle boggle",
                     key='2',
                     function=FoggleBoggle),
            MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['settings'].capitalize()}",
                     key='s',
                     function=generate_settings),
            MenuItem(text=f"{DictionaryParser.get_dict_meta('actions')['quit'].capitalize()}",
                     key='q',
                     function=exit),
        ]
        HostIO.display_main_menu(menu_items)
