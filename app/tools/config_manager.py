import configparser
import os
import re
from pathlib import Path
from typing import Any


class ConfigManager:
    class _ConfigSection:
        """
        Configuration manager used to load environment configuration.
        """

        __section: configparser.SectionProxy

        def __init__(self, parser, name):
            self._parser = parser
            self._name = name
            self.__section = configparser.SectionProxy(parser, name)

        def __getitem__(self, option):
            return self.get(option)

        def get(self, option):
            item = self._parser.get(self._name, option)
            # We test if the option is an environment variable, if so we replace by its value
            if isinstance(item, str) and re.match(r"^\${(\w+)}$", item):
                return os.getenv(re.match(r"^\${(\w+)}$", item).group(1))
            return item

        def get_int(self, option):
            return self._parser.getint(self._name, option)

        def get_float(self, option):
            return self._parser.getfloat(self._name, option)

        def get_boolean(self, option):
            return self._parser.getboolean(self._name, option)

        def set(self, option, value):
            return self._parser.set(self._name, option, value)

        def unset(self, option):
            return self._parser.remove_option(self._name, option)

    __config_parser: configparser.ConfigParser = None

    def __new__(cls) -> Any:
        if not hasattr(cls, "__instance"):
            cls.__instance = super().__new__(cls)
            cls.__instance.__config_parser = cls.__instance._load()
        return cls.__instance

    @staticmethod
    def _load() -> configparser.ConfigParser:
        config_parser = configparser.ConfigParser()
        config_file_path = (
            Path(os.path.dirname(os.path.abspath(__file__))).absolute().parent
            / "config"
            / "config.ini"
        )
        config_parser.read(config_file_path)

        config_file_path = config_file_path.parent / "config.ini.override"
        if config_file_path.exists():
            config_parser.read(config_file_path)

        return config_parser

    def __getitem__(self, section):
        return self._ConfigSection(self.__config_parser, section)

    def get(self, section, option):
        return self._ConfigSection(self.__config_parser, section).get(option)

    def set(self, section, option, value):
        return self._ConfigSection(self.__config_parser, section).set(option, value)

    def unset(self, section, option):
        return self._ConfigSection(self.__config_parser, section).unset(option)

    def get_int(self, section, option):
        return self._ConfigSection(self.__config_parser, section).get_int(option)

    def get_float(self, section, option):
        return self._ConfigSection(self.__config_parser, section).get_float(option)

    def get_boolean(self, section, option):
        return self._ConfigSection(self.__config_parser, section).get_boolean(option)

    def has_option(self, section, option):
        return self.__config_parser.has_option(section, option)

    def get_env(self):
        return self.__config_parser["config"]["environment"] or "local"
