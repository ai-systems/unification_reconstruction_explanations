import os
import inspect
from collections import defaultdict
from abc import ABC, abstractmethod


from ailog import Loggable
from .register import Register


class Instance(ABC, Loggable, Register):
    """Abstract class for model

    Args:
        ABC (class): abstract definition
        Loggable (class): logger modules. Classes inheriting this class can access logger with `self.logger`
    """

    @abstractmethod
    def __call__(self):
        """Implement this method to serialize data with msgpack
        """

    def serialize(self) -> None:
        """Used to serialize by MsgPack
        """
        return self.__call__()

    @classmethod
    def de_serialize(cls, as_str):
        """Used to de-serialize by MsgPack
        """
        return cls(**as_str)
