import json
from datetime import datetime


typemap = {
    datetime: (lambda v: v.isoformat(), lambda d: datetime.fromisoformat(d)),
}


def dump(obj, tmap=None):
    typemap = tmap if tmap is not None else globals()['typemap']

    if hasattr(obj, '__jsondump__'):
        obj = obj.__jsondump__()

    if isinstance(obj, dict):
        obj = {key: dump(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        obj = [dump(value) for value in obj]
    elif type(obj) in typemap:
        obj = typemap[type(obj)][0](obj)
    elif not isinstance(obj, (str, float, int)):
        obj = str(obj)

    return obj


def dumps(obj, tmap=None):
    return json.dumps(dump(obj))


def load(cls, data, tmap=None):
    if hasattr(cls, '__jsonload__'):
        return cls.__jsonload__(data)
    typemap = tmap if tmap is not None else globals()['typemap']
    if cls in typemap:
        return typemap[cls][1](data)
    return cls(data)


def loads(cls, data):
    data = json.loads(data)
    return load(cls, data)
