from unittest import TestCase
import os

from ailog import setup_logging, Loggable
import logging
import _jsonnet
import shutil
import json
from regra.common.util import resolve_config


class RegraTestCase(TestCase, Loggable):
    def setUp(self):
        self.mode = 'regra_test'
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(os.path.join(file_path, ".."))
        self.config_file = f'{os.environ["PWD"]}/conf/dev/dirs.jsonnet'
        self.config = resolve_config(self.config_file)
        # if os.path.exists(f'{os.environ["PWD"]}/tests/resources/explanation_bank/cache'):
        #     shutil.rmtree(
        #         f'{os.environ["PWD"]}/tests/resources/explanation_bank/cache')
        setup_logging("tests/resources/logging.conf")
        logging.getLogger(__name__).info(f"Working dir: {os.getcwd()}")
        self.logger.info('Setting up logging')
