# If Python Version is Lower than 3.11, this well be import tomli to change tomllib
try:
    import tomllib
except ImportError:
    import tomli as tomllib

import os

from print_color import print

import modules.globalVariables as gVar
from modules.configs.defaultConfig import create_config_file


class Config:
    def __init__(self):
        self._fileName = gVar.configFileName
        self._content = {}

    # Setup config
    # return Ture or False
    # Ture is Success
    # False is Failure
    def init(self) -> bool:
        # If config.toml does not exist, create it
        if not os.path.exists(self._fileName):
            create_config_file(self._fileName)
            print("Created default config file", tag="success", tag_color='green', color='white')
            return True

        # Check config.toml is not folder
        if not os.path.isfile(self._fileName):
            print("config.toml not file", tag="Error", tag_color='red', color='white')
            return False

        # Check config.toml is can readable
        if not os.access(self._fileName, os.R_OK):
            print("config.toml not readable", tag="Error", tag_color='red', color='white')
            return False
        return True

    def read(self) -> dict:
        with open(self._fileName, 'rb') as fff:
            f = tomllib.load(fff)
            if f["General"]["debug"] :
                gVar.debugMode = f["General"]["debug"]
                print(f)
            return f

