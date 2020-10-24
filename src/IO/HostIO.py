import os
from FileParser.DictionaryParser import DictionaryParser


# This class takes care of all output to the command prompt and all input from the user.
# It also takes care of creating a command line based menu from a list of menu items.
class HostIO:
    @staticmethod
    def get_input(text):
        return input(text)

    @staticmethod
    def format_str_length(var, length):
        return var + ' ' * (length - len(var))

    @staticmethod
    def display_standard_menu(menu_string, menu_items):
        menu_items_string = ""
        for instance in menu_items:
            menu_items_string += HostIO.format_str_length(
                f"*    [{instance.key}] {instance.text}   ", 37) + "*\n"

        HostIO.clear()
        command = HostIO.get_input("".join(menu_string) % menu_items_string)

        if command in [str(instance.key) for instance in menu_items]:
            for instance in menu_items:
                if instance.key is command:
                    if instance.args is not None:
                        instance.function(*instance.args)
                    else:
                        instance.function()
                    break
        else:
            print(f"{DictionaryParser.get_dict_meta('actions')['unrecognized command'].capitalize()}\n")

    @staticmethod
    def display_settings_menu(menu_items):
        HostIO.display_standard_menu(DictionaryParser.get_dict_meta('settings'), menu_items)

    @staticmethod
    def display_main_menu(menu_items):
        HostIO.display_standard_menu(DictionaryParser.get_dict_meta('menu'), menu_items)

    @staticmethod
    def clear():
        os.system('cls||clear')

    @staticmethod
    def print(text, clear_screen=False, direct_continue=False):
        if clear_screen:
            HostIO.clear()
        if not direct_continue:
            input(text + '\nPress any key to continue')
        else:
            print(text)