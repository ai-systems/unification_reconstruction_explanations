from abc import ABC, abstractmethod

from ailog import Loggable

from .register import Register


class API(Loggable, Register, ABC):
    """Defines the abstract class for API
    """
