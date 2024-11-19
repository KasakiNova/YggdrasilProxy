# coding=utf-8
import logging

from print_color import print

class Logger:
    def __init__(self):
        self._logger = logging.getLogger()
