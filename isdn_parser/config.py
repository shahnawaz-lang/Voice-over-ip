"""
Configuration file for the ISDN parser
"""

import os
import logging
from configparser import ConfigParser
from typing import Optional, ClassVar


class Config:
    """
    Configuration for the CLI application
    This class is a singleton and should be used to load the configuration file
    """

    _instance: ClassVar[Optional['Config']] = None
    config: ConfigParser

    def __new__(cls) -> "Config":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = ConfigParser()
        return cls._instance

    @classmethod
    def get(cls, section, key, fallback=None) -> str:
        assert cls._instance is not None, "Config not loaded. Please load the config file"
        return cls._instance.config.get(section, key, fallback=fallback)

    @classmethod
    def load(cls):
        try:
            cls._instance.config.read(os.path.join(os.path.dirname(__file__), "config.ini"))
        except FileNotFoundError:
            logging.error("Config file not found")
            exit(1)

    def __getitem__(self, item):
        return self.config[item]


config = Config()
