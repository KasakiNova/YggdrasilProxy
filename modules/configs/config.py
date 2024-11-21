# coding=utf-8
import sys
import os

# If Python Version is Lower than 3.11 or not found tomllib, this well be import tomli to change tomllib
try:
    import tomllib
except ImportError:
    import tomli as tomllib

from print_color import print

import modules.globalVariables as gVar
from modules.configs.defaultConfig import create_config_file
from modules.configs.configChecker import validate_config

class Config:
    def __init__(self):
        self._file_name = gVar.configFileName
        self._content = {}

    # Setup config
    # return Ture or False
    # Ture is Success
    # False is Failure
    def init(self) -> bool:
        # If config.toml does not exist, create it
        if not os.path.exists(self._file_name):
            create_config_file(self._file_name)
            print("Created default config file", tag="success", tag_color='green', color='white')
            return True

        # Check config.toml is not folder
        if not os.path.isfile(self._file_name):
            print("config.toml not file", tag="Error", tag_color='red', color='white')
            return False

        # Check config.toml is can readable
        if not os.access(self._file_name, os.R_OK):
            print("config.toml not readable", tag="Error", tag_color='red', color='white')
            return False
        return True

    def read(self) -> dict:
        with open(self._file_name, 'rb') as fff:
            f = tomllib.load(fff)
            if not validate_config(f):
                sys.exit("Config File is incorrect")
            try:
                if f["General"]["debug"] :
                    gVar.debugMode = True
            except KeyError:
                gVar.debugMode = False
            return f

