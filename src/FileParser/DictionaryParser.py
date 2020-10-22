from pathlib import Path
from json import load
from json.decoder import JSONDecodeError

from FileParser.path import get_root_dir


class DictionaryParser:
    DEFAULT_DICT_STANDARD = {'name': str,
                             'author': str,
                             'menu': list,
                             'settings': list,
                             'client_text': str,
                             'actions': dict,
                             'letters': list,
                             'tile_configs': dict}

    meta = {}
    wordlist = []

    @staticmethod
    def load_dictionary(language, language_dir=None, silent=False):
        if language_dir is None:
            language_dir = get_root_dir() / 'dicts' / language

        language_meta_dir = language_dir / 'meta.json'
        language_list_dir = language_dir / 'dict.txt'

        try:
            with open(language_meta_dir) as file:
                try:
                    DictionaryParser.meta = load(file)
                except JSONDecodeError:
                    if not silent:
                        print("meta.json is not readable by the program. \n" +
                              "Make sure meta.json follows the correct standard.")
                    exit(5)

        except FileNotFoundError:
            if not silent:
                print(f"meta.json not found in dicts/{language} sub-folder")
            exit(4)

        for key, instance in DictionaryParser.meta.items():
            if not key in DictionaryParser.DEFAULT_DICT_STANDARD.keys() or \
                    not type(instance) is DictionaryParser.DEFAULT_DICT_STANDARD[key]:
                if not silent:
                    print("meta.json has the wrong format.  \n" +
                          "Make sure meta.json follows the correct standard.")
                exit(6)

        try:
            with open(language_list_dir) as dictionary:
                DictionaryParser.wordlist = [word.rstrip().upper() for word in dictionary]
        except FileNotFoundError:
            if not silent:
                print(f"dict.txt not found in dicts/{language} sub-folder")
            exit(4)
        tmp = DictionaryParser.wordlist
        if len(DictionaryParser.wordlist) == 0:
            if not silent:
                print("dict.txt is empty")
            exit(6)

    @staticmethod
    def get_dict_meta(key):
        return DictionaryParser.meta[key]

    @staticmethod
    def check_dict_word(word):
        return word.upper() in DictionaryParser.wordlist
