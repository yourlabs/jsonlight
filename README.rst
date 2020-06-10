jsonlight: json with rudimentary type encoding/decoding for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adds support for a couple of new Python magic methods to make Python object
JSON encoding and decoding a bit easier.

Tutorial
========

Instead of:

.. code:: python

    from json import loads, dumps
    from uuid import UUID, uuid4

    obj = uuid4()
    encoded = dumps(str(obj))
    decoded = UUID(loads(encoded))

    assert obj == decoded

You can do:

.. code:: python

    from jsonlight import loads, dumps
    from uuid import UUID, uuid4

    obj = uuid4()
    encoded = dumps(obj)
    decoded = loads(UUID, encoded)
    assert obj == decoded

This is because jsonlight patches uuid.UUID class to add the following methods:

- ``__jsondump__``: return a representation of self with JSON data types
- ``__jsonload__``: instanciate an object based on the result from __jsondump__

You can see that the main difference with ``json.loads`` is that
``jsonlight.loads`` requires a type as first argument. This is because
``jsonlight.loads`` will first call ``json.loads`` to convert the string into a
Python object with basic JSON tyes, and then pass that to the type's
``__jsonload__`` function.

Other types can't be monkey patched, so you have to import them from jsonlight
instead, which is the sad case of datetime:

.. code:: python

    from jsonlight import loads, dumps, datetime
    obj = datetime.now()
    assert obj == loads(datetime, dumps(obj))

You may also define ``__jsondump__`` and ``__jsonload__`` methods on your own
classes, example:

.. code-block:: python

    from jsonlight import load

    class YourClass:
        def __init__(self, uuid=None):
            self.uuid = uuid or uuid4()

        def __jsondump__(self):
            return dict(uuid=self.uuid)

        @classmethod
        def __jsonload__(cls, data):
            return cls(load(UUID, data['uuid'])

            # This also works, but would not illustrate how to support recursion
            # return cls(UUID(data['uuid']))

As you can see:

- you don't have to worry about calling ``__jsondump__`` on return values of
  your own ``__jsondump__`` because ``jsonlight.dumps`` will do that
  recursively,
- you have full control on deserialization just like with ``__setstate__``,

Monkey-patches
--------------

Monkey-patched stdlib objects are:

- UUID
- Path

Feel free to add more.

Stdlib objects that couldn't be monkey patched, and that you have to import
from jsonlight instead are:

- datetime
