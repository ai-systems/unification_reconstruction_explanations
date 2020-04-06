from abc import ABC, abstractmethod

from ailog import Loggable
from luigi import BoolParameter, Parameter, Task
from luigi.task import flatten
from overrides import overrides

from .register import Register


class Dataset(ABC, Loggable, Register, Task):
    """Defines the dataset model. This is a Safe luigi Task
    """
    path = Parameter(default=None)
    force = BoolParameter(default=False)

    def complete(self) -> bool:
        return not self.force and all(
            dependency.complete() for dependency in self._dependencies
        ) and all(output.exists() for output in self._outputs)

    @property
    def _dependencies(self):
        return flatten(self.requires())

    @property
    def _outputs(self):
        return flatten(self.output())

    @abstractmethod
    def run(self):
        """Process logic
        """
