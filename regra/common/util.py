import json
import os
import sys
from enum import Enum
from typing import List
from importlib import import_module
import _jsonnet
from aiconf import load_class

from regra.abc import Instance


def custom_serialize(obj):
    """Custom serialization function to be used with msgpack.

    Provides serialization for Vocabulary and Enums.

    Args:
      obj: Object to serialize.

    Returns:
      Serialized object.

    """
    if isinstance(obj, Instance):
        name = obj.__class__.__module__+'.'+obj.__class__.__qualname__
        return {'__model__': True, 'cls': name,  'as_str': {custom_serialize(key): custom_serialize(val) for key, val in obj.__dict__.items()}}
    if isinstance(obj, Enum):
        return {
            '__enum__':
            True,
            '__class__':
            '.'.join((obj.__class__.__module__, obj.__class__.__name__)),
            'name':
            obj.name
        }
    if isinstance(obj, frozenset):
        return {'__frozenset__': True, 'as_str': [val for val in obj]}

    return obj


def custom_web_serialize(obj):
    """Custom serialization function to be used with msgpack.

    Provides serialization for Vocabulary and Enums.

    Args:
      obj: Object to serialize.

    Returns:
      Serialized object.

    """
    if isinstance(obj, Instance):
        name = obj.__class__.__module__+'.'+obj.__class__.__qualname__
        return {key: custom_web_serialize(val) for key, val in obj.serialize().items()}
    if isinstance(obj, Enum):
        return {
            '__enum__':
            True,
            '__class__':
            '.'.join((obj.__class__.__module__, obj.__class__.__name__)),
            'name':
            obj.name
        }
    if isinstance(obj, list):
        return [custom_web_serialize(item) for item in obj]
    if isinstance(obj, tuple):
        return [custom_web_serialize(item) for item in obj]
    if isinstance(obj, dict):
        return {key: custom_web_serialize(val) for key, val in obj.items()}

    return obj


def custom_deserialize(obj):
    """Custom deserialization function to be used with msgpack.

    Provides deserialization for Vocabulary and Enums.

    Args:
      obj: Object to deserialize.

    Returns:
      Deserialized object.

    """
    if '__model__' in obj:
        instance = Instance.subclasses[obj['cls']]()
        for key, val in obj['as_str'].items():
            setattr(instance, key, val)
        return instance
        return Instance.subclasses[obj['cls']].de_serialize(obj['as_str'])
    if '__enum__' in obj:
        return load_class(obj['__class__'])[obj['name']]
    if '__frozenset__' in obj:
        return frozenset(obj['as_str'])

    return obj


def chunks(l: List, size: int):
    """Yield successive `size`-sized chunks from `list`.

    Args:
      l: List to chunk
      size: Size of the chunks.

    Returns:

    """
    for i in range(0, len(l), size):
        yield [(index, l[index]) for index in range(i, min(i+size, len(l)))]
        # , l[i:i + size]


def resolve_config(config_file):
    """Resolving config file
    """
    with open(config_file) as f:
        path_config = f'{{ {f.read()} }}'
        config = json.loads(_jsonnet.evaluate_snippet(
            'log', path_config, ext_vars={
                'PWD': os.environ['PWD']}))
        return config


def check_module(process):
    if isinstance(process, dict) and 'module' in process.keys() and 'class_name' in process.keys():
        cls = getattr(import_module(process.pop('module')),
                      process.pop('class_name'))
        return cls
    return process
