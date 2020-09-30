import unittest
from pathlib import Path

from os.path import isdir, isfile
from FileParser.path import get_root_dir
from FileParser.settings_parser import load_settings, get_setting, settings
from FileParser.dictionary_parser import load_dictionary


class DirTest(unittest.TestCase):
    def test_root_dir(self):
        self.assertTrue(isdir(get_root_dir()))

    def test_incorrect_json_exists(self):
        path = get_root_dir() / 'tests' / 'test_json_incorrect.json'
        self.assertTrue(isfile(path))

    def test_incorrect_settings_exists(self):
        path = get_root_dir() / 'tests' / 'test_settings_incorrect_format.json'
        self.assertTrue(isfile(path))

    def test_incorrect_meta_json_exists(self):
        path = get_root_dir() / 'tests' / 'test_dict_json_incorrect' / 'meta.json'
        self.assertTrue(isfile(path))

    def test_incorrect_dict_meta_exists(self):
        path = get_root_dir() / 'tests' / 'test_dict_format_incorrect' / 'meta.json'
        self.assertTrue(isfile(path))

    def test_incorrect_dict_exists(self):
        path = get_root_dir() / 'tests' / 'test_dict_format_incorrect' / 'dict.txt'
        self.assertTrue(isfile(path))



class SettingsTest(unittest.TestCase):
    def test_settings_wrong_filepath(self):
        path = '/this_dosnt_exist'
        try:
            load_settings(path, silent=True)
        except SystemExit as cm:
            self.assertEqual(cm.code, 1)

    def test_settings_incorrect_json(self):
        path = get_root_dir() / 'tests' / 'test_json_incorrect.json'
        try:
            load_settings(path, silent=True)
        except SystemExit as cm:
            self.assertEqual(cm.code, 2)

    def test_settings_incorrect_format(self):
        path = get_root_dir() / 'tests' / 'test_settings_incorrect_format.json'
        try:
            load_settings(path, silent=True)
        except SystemExit as cm:
            self.assertEqual(cm.code, 3)

    def test_settings_correct(self):
        try:
            load_settings(silent=True)
            success = True
        except SystemExit:
            success = False

        self.assertTrue(success)


class DictionaryTest(unittest.TestCase):
    def test_dictionary_wrong_filepath(self):
        path = '/this_dosnt_exist'
        try:
            load_dictionary(path, silent=True)
        except SystemExit as cm:
            self.assertEqual(cm.code, 4)

    def test_dictionary_incorrect_json(self):
        path = get_root_dir() / 'tests' / 'test_dict_json_incorrect'
        try:
            load_dictionary(path, silent=True)
        except SystemExit as cm:
            self.assertEqual(cm.code, 5)

    def test_dictionary_incorrect_files_format(self):
        path = get_root_dir() / 'tests' / 'test_dict_format_incorrect'
        try:
            load_dictionary(path, silent=True)
        except SystemExit as cm:
            self.assertEqual(cm.code, 6)

    def test_dictionary_correct(self):
        load_settings(silent=True)
        try:
            load_dictionary(language=get_setting('language'), silent=True)
            success = True
        except SystemExit:
            success = False

        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
