"""read logging.yaml for logging the program"""
import logging
import logging.config
import os
from pathlib import Path

import yaml

from app.tools.config_manager import ConfigManager

config = ConfigManager()
project_directory = Path(os.path.dirname(os.path.abspath(__file__))).absolute().parent
config_directory = project_directory / "config"
default_config_path = config_directory / "logging.yaml"


def setup_logging(
    module_name, config_path=default_config_path, default_level=logging.INFO
):

    if os.path.exists(config_path):
        with open(config_path, "rt") as f:
            try:
                config_yaml = yaml.safe_load(f.read())

                logging.config.dictConfig(config_yaml)
                if bool(os.getenv("NO_LOGGING", False)):
                    logging.disable()
                logger = logging.getLogger(module_name)
            except yaml.YAMLError as e:
                logging.basicConfig(level=default_level)
                logger = logging.getLogger(module_name)
                logger.warning(
                    'Error in "logging.yaml" configuration. Using default configuration.',
                    e,
                )
    else:
        logging.basicConfig(level=default_level)
        logger = logging.getLogger(module_name)
        logger.info('No "logging.yaml" file found. Using default configuration.')

    return logger
