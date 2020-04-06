from typing import Any
from ailog import Loggable
from abc import ABC, abstractmethod
from .dataset import Dataset
from .register import Register
from luigi import Task, Target


class Process(ABC, Loggable, Register, Task):
    """Abstract module for process. Extends Luigi Task module
    """
