import inspect
import json
import os
from abc import ABC, abstractmethod

import _jsonnet
from luigi import Parameter
from overrides import overrides

from regra.abc import Dataset
from regra.common.util import resolve_config, check_module

from .msgpack_target import MsgPackTarget


class MsgPackDataset(Dataset):
    """Defines the dataset model. This is a Safe luigi Task
    """
    mode = Parameter(default=None)
    config_file = Parameter(default=None)

    def __init__(self, **kwargs):
        super(MsgPackDataset, self).__init__(**kwargs)
        class_file = inspect.getfile(self.__class__)
        task_config_path = "/".join(class_file.split('/')
                                    [:-1])+'/config.jsonnet'
        self.logger.info(f'Looking for {task_config_path}')
        if os.path.isfile(task_config_path) and self.mode is not None:
            self.logger.info(f'Config file found for {self.__class__}')
            with open(task_config_path, 'r') as task_file:
                config = task_file.read()
                with open(self.config_file, 'r') as f:
                    config = f'{f.read()},\n {config}'
                self.path_config = resolve_config(self.config_file)
                config = '{'+config+'}'
                config = json.loads(_jsonnet.evaluate_snippet(
                    'log', config, ext_vars={
                        'PWD': os.environ['PWD']}))[self.mode]
                config = {key: check_module(
                    config[key]) for key in config}
                self.logger.info(f'Loading config {config}')
                for v_name, variable in self.__dict__.items():
                    if variable is None and v_name in config:
                        setattr(self, v_name, config[v_name])

    @overrides
    def output(self, **kwargs):
        transform = kwargs.get('transform')
        os.makedirs(self.path, exist_ok=True)
        return MsgPackTarget(path=self.cache_path, transform=transform)

    @property
    @abstractmethod
    def cache_path(self):
        """Returns the dataset path
        """
