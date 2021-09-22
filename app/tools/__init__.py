# TODO: Pour la partie "tools", il s'agit d'un ensemble de fichier/methode que j'ai l'habitude d'utiliser pour ce genre de projet
#    Cette partie me sert à initialiser mon configmanager & mon logger

from app.tools.config_manager import ConfigManager
from app.tools.logger import setup_logging

config = ConfigManager()
logger = setup_logging("intervention_app")

