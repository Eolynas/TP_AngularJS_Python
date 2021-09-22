# TODO: Méthode importé de mes autrs projet qui me permet de transformer un objet SqlAlchemy en dict

import collections
import enum
from datetime import datetime


def todict(obj):
    """
    Recursively convert a Python object graph to sequences (lists)
    and mappings (dicts) of primitives (bool, int, float, string, ...)
    """
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, enum.Enum):
        return str(obj)
    elif isinstance(obj, dict):
        return dict((key, todict(val)) for key, val in obj.items())
    elif isinstance(obj, collections.Iterable):
        return [todict(val) for val in obj]
    elif hasattr(obj, "__slots__"):
        return todict(
            dict((name, getattr(obj, name)) for name in getattr(obj, "__slots__"))
        )
    elif hasattr(obj, "__dict__"):
        keys = vars(obj)
        if "_sa_instance_state" in keys:
            del keys["_sa_instance_state"]
        return todict(vars(obj))
    return obj


# TODO: Création du status coté back
#   Le status n'est pas présent dans la base de donnée, car impossible pour elle de changer "en temps reel"
#   Je renvoie donc systematique l'objet avec le status
#   Il n'est pas calculé coté front, car si une autre application veux requeter sur l'API elle n'aurait pas l'information du status (exemple requete via Postman)
def get_status(intervention: dict) -> dict:
    """
    Definition of the status of the intervention
    :param intervention: intervention object in dict
    :return: intervention object with status
    """
    for key, values in intervention.items():
        if not values:
            intervention['status'] = "Brouillon"
            break

    if not intervention.get('status'):
        if intervention['date_intervention'] < datetime.now():
            intervention['status'] = "Terminée"
        else:
            intervention['status'] = "Validée"

    return intervention
