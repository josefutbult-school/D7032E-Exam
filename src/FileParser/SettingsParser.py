from pathlib import Path
from json import load, dump
from json.decoder import JSONDecodeError
from io import UnsupportedOperation

from FileParser.path import get_root_dir


class SettingsParser:
    DEFAULT_SETTINGS_STANDARD = {'board_size': int,
                                 'language': str,
                                 'show_solution': int,
                                 'number_players': int,
                                 'game_time': int,
                                 'generous_boggle': int}

    settings = {}

    @staticmethod
    def load_settings(settings_dir=None, silent=False):

        if settings_dir is None:
            settings_dir = get_root_dir() / 'settings' / 'settings.json'

        try:
            with open(settings_dir, 'r') as file:
                try:
                    SettingsParser.settings = load(file)
                except JSONDecodeError:
                    if not silent:
                        print("settings.json is not readable by the program. \n" +
                              "Make sure settings.json follows the correct standard.")
                    exit(2)
        except FileNotFoundError:
            if not silent:
                print("settings.json not found in settings sub-folder")
            exit(1)

        for key, instance in SettingsParser.settings.items():
            if not key in SettingsParser.DEFAULT_SETTINGS_STANDARD.keys() or \
                    not type(instance) is SettingsParser.DEFAULT_SETTINGS_STANDARD[key]:
                if not silent:
                    print("settings.json has the wrong format.  \n" +
                          "Make sure settings.json follows the correct standard.")
                exit(3)

    @staticmethod
    def save_settings(settings_dir=None, silent=False):
        if settings_dir is None:
            settings_dir = get_root_dir() / 'settings' / 'settings.json'

        try:
            with open(settings_dir, 'w') as file:
                dump(SettingsParser.settings, file)
        except FileNotFoundError:
            if not silent:
                print("settings.json not found in settings sub-folder")
            exit(1)
        except UnsupportedOperation:
            if not silent:
                print("Unable to write instance to file")
            exit(1)

    @staticmethod
    def get_setting(key):
        return SettingsParser.settings[key]

    @staticmethod
    def set_setting(key, value):
        SettingsParser.settings[key] = value

    # TODO: Remove
    @staticmethod
    def print_settings():
        print(SettingsParser.settings)
