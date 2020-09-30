from os import path
from pathlib import Path


# TODO: Check that this works on Windows and Mac
def get_root_dir():
    return Path(path.abspath(__file__)).parent.parent.parent
