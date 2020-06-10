from jsonlight import datetime, dump, dumps, load, loads

from pathlib import Path
from uuid import UUID, uuid4


def test_uuid():
    obj = uuid4()
    encoded = dumps(obj)
    decoded = loads(UUID, encoded)
    assert obj == decoded


def test_datetime():
    obj = datetime.now()
    assert loads(datetime, dumps(obj)) == obj


def test_path():
    obj = Path('/foo')
    assert loads(Path, dumps(obj)) == obj


def test_obj():
    class Foo:
        def __init__(self, uuid, path, dt):
            self.path = path
            self.uuid = uuid
            self.dt = dt

        def __jsondump__(self):
            return dump(self.__dict__)

        @classmethod
        def __jsonload__(cls, data):
            return cls(
                dt=load(datetime, data['dt']),
                path=load(Path, data['path']),
                uuid=load(UUID, data['uuid']),
            )

    obj = Foo(uuid4(), Path('/bar'), datetime.now())
    result = loads(Foo, dumps(obj))
    assert obj.path == result.path
    assert obj.uuid == result.uuid
    assert obj.dt == result.dt


class YourClass:
    def __init__(self, uuid=None):
        self.uuid = uuid or uuid4()

    def __jsondump__(self):
        return dict(uuid=self.uuid)

    @classmethod
    def __jsonload__(cls, data):
        return cls(UUID(data['uuid']))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return other.uuid == self.uuid
        return super().__eq__(other)


def test_your_class_and_nesting():
    obj = YourClass()
    encoded = dumps(obj)
    decoded = loads(YourClass, encoded)
    assert obj == decoded


class YourClassList(list):
    """Represents a list of YourClass objects"""

    @classmethod
    def __jsonload__(cls, data):
        return [YourClass.__jsonload__(value) for value in data]


def test_moar_nesting():
    obj = YourClassList([YourClass(), YourClass()])
    encoded = dumps(obj)
    decoded = loads(YourClassList, encoded)
    assert obj[0] == decoded[0]
    assert obj[1] == decoded[1]
