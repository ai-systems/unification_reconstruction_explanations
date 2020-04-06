import glob
import os
from functools import reduce
from typing import List

import msgpack
import numpy as np
import pandas as pd
from luigi import Parameter
from overrides import overrides
from tqdm import tqdm

from regra.dataset.abc import MsgPackDataset
from regra.common.util import custom_deserialize, custom_serialize

from regra.dataset.explanation_bank.instances import Table

UID = '[SKIP] UID'
EXPL_CACHE = 'table_store.mpk'


class TableStoreDataset(MsgPackDataset):

    table_store_path = Parameter(default=None)

    @overrides
    def requires(self):
        return []

    @overrides
    def run(self):
        self.logger.info(f'Loading table store from: {self.table_store_path}')
        # Get all tsv files
        os.chdir(self.table_store_path)
        table_store_files = glob.glob('*.tsv')
        table_stores = reduce(lambda store, file_name: {**store, **TableStoreDataset.process_store(
            f'{self.table_store_path}/{file_name}', file_name)}, tqdm(table_store_files), {})
        self.logger.info(f'Saving data into {self.path}')
        self.output().dump(table_stores)

    @staticmethod
    def process_store(file_name: str, table_name: str) -> Table:
        """Process individual file stores
        """
        table_df = pd.read_csv(file_name, sep='\t')
        table_items = {}
        for _, row in tqdm(table_df.iterrows(), total=table_df.shape[0]):
            id = row[UID]
            explanation = reduce(
                lambda expl, items: {**expl, items[0]: None} if pd.isna(items[1]) else {**expl, items[0]: items[1]}, row.items(), {})
            filtered_explanation = {
                k: v for k, v in explanation.items() if k != UID and 'SKIP' not in k}
            sentence_explanation = [str(text).strip() for text in list(filter(
                lambda val: not pd.isna(val), explanation.values()))[:-1]]
            table_items[id] = Table(id=id, explanation=explanation,
                                    sentence_explanation=sentence_explanation, table_name=table_name.split('.')[0], filtered_explanation=filtered_explanation)
        return table_items

    @property
    def cache_path(self):
        return f'{self.path}/{EXPL_CACHE}'
