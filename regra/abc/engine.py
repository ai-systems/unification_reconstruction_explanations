import os
from abc import ABC, abstractmethod
from ailog import Loggable
from collections import defaultdict
from .register import Register


class RegraEngine(ABC, Loggable, Register):
    """Abstract class for RegraEngine which performs the following training, evaluation and inference
    """

    def __init__(self, from_cache=False, **kwargs):
        if not from_cache:
            os.makedirs(kwargs.get('path'), exist_ok=True)
            self.cache(**kwargs)
        else:
            self.from_cache(**kwargs)

    @abstractmethod
    def cache(self, **kwargs):
        """Caching dataset
        """

    @abstractmethod
    def from_cache(self, **kwargs):
        """Retrieve data from cache
        """
    @abstractmethod
    def train(self, **kwargs):
        """Train the engine
        """

    @abstractmethod
    def evaluate(self, **kwargs):
        """Evaluate the engine
        """

    @abstractmethod
    def infer(self, **kwargs):
        """Infer from the engine
        """
