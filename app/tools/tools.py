import collections
import enum


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
