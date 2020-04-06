from abc import ABC, abstractmethod
from ailog import Loggable
from .register import Register


class Visualizer(ABC, Loggable, Register):
    """Abstract class for the visualizer module
    """

    def __init__(self, app):
        self.app = app

    @abstractmethod
    def preprocess(self, **kwargs):
        """Preprocess the data to visualize
        """

    @abstractmethod
    def setup_layout(self, **kwargs):
        """Setting up layout of visualization
        """
