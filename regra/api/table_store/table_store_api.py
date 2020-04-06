import os
import re
import sys
from collections import defaultdict
from functools import reduce
from string import punctuation
from typing import Dict

import msgpack
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
from tqdm import tqdm

from regra.abc import API
from regra.common.util import custom_deserialize, custom_serialize
from regra.dataset.explanation_bank.instances import Table
from regra.dataset.explanation_bank.table_store_dataset import \
    TableStoreDataset

from .instances import OverlapExplanation

stemmer = PorterStemmer()
stop = set([stemmer.stem(word) for word in set(stopwords.words('english'))])


TABLE_STORE_API_CONFIG = 'table_store'


def cache_file(path): return f'{path}/table_store_api.mpk'


class TableStoreAPI(API):
    """Defines the table store API
    """

    def __init__(self, mode: str, config_file: str, api_config: Dict = {}):
        self.api_config = api_config[TABLE_STORE_API_CONFIG]
        self.table_store_dataset, self.stemmed_explanations, self.string_map = self.setUp(
            mode, config_file, self.api_config['cache'])

    def setUp(self, mode: str, config_file: str, path: str):
        """Setting up API
        """
        if os.path.exists(cache_file(path)):
            self.logger.info('Retrieving data from cache')
        else:
            self.logger.info('Caching data')
            task = TableStoreDataset(mode=mode,
                                     config_file=config_file)
            data = task.output().load()
            stemmed_explanations = {}
            string_map = defaultdict(lambda: set())
            for id, val in tqdm(data.items(), desc='Preparing table store API'):
                stemmed_explanations[id] = TableStoreAPI.stem_explanations(val)
                for role, val_list in stemmed_explanations[id]:
                    for text in val_list:
                        string_map[text].add((id, role))
            return data, stemmed_explanations, string_map

    @staticmethod
    def stem_explanations(table: Table):
        filtered = list(filter(
            lambda text: 'FILL*' not in text[0], table._filtered_explanation.items()))
        stemmed = list(filter(lambda values: values[1] != None, [
            (t[0], TableStoreAPI.stem_phrase(t[1])) for t in filtered]))
        return stemmed

    @staticmethod
    def stem_phrase(text: str):
        if text is None:
            return None
        return list(filter(lambda t: t not in punctuation and t not in stop and not t.startswith("'"), [stemmer.stem(t) for t in word_tokenize(str(text))]))

    def query_question(self, question: str, **kwargs):
        """Querying based on question
        """
        stemmed_question = TableStoreAPI.stem_phrase(question)
        overlap_explanations = defaultdict(lambda: {})
        for text in stemmed_question:
            if text in self.string_map:
                for id, role in self.string_map[text]:
                    role = self.convert_role(role)
                    if role not in overlap_explanations[id]:
                        overlap_explanations[id][role] = []
                    overlap_explanations[id][role].append(text)
                    # for elm in stemmed_exp:
                    #     if text in elm[1]:
                    #         overlap_explanations[id].append({
                    #             'word': text,
                    #             'role': elm[0]
                    #         })
        return overlap_explanations, stemmed_question

    @staticmethod
    def convert_role(role: str):
        return re.sub('\d', '', role.split('.')[0])

    def query_table(self, table: Table, **kwargs):
        """Querying based on Table
        """
        stemmed_explanation = TableStoreAPI.stem_explanations(table)
        overlap_explanations = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: [])))
        # Get stemmed explanations
        for src_role, stemmed_words in stemmed_explanation:
            src_role = self.convert_role(src_role)
            # Get stemmed words
            for word in stemmed_words:
                for id, tgt_role in self.string_map[word]:
                    tgt_role = self.convert_role(tgt_role)
                    if (self.table_store_dataset[id]._table_name == table._table_name and 'FILL' in tgt_role) or id == table._id:
                        continue
                    overlap_explanations[id][src_role][tgt_role].append(word)
        return overlap_explanations

    def query_table_token(self, table: Table, **kwargs):
        """Querying based on Table
        """
        stemmed_explanation = TableStoreAPI.stem_explanations(table)
        overlap_explanations = {}
        # Get stemmed explanations
        for role, stemmed_words in stemmed_explanation:
            # Get stemmed words
            for word in stemmed_words:
                ids = list(self.string_map[word])
                stemmed_exp = [self.stemmed_explanations[id] for id in ids]
                for index, exp in enumerate(stemmed_exp):
                    for elm in exp:
                        target_id = ids[index]
                        if word in elm[1]:
                            if target_id in overlap_explanations:
                                overlap_explanations[target_id]['tgt_role'].append(
                                    elm[0])
                                overlap_explanations[target_id]['tgt_word'].append(
                                    elm[1])
                                overlap_explanations[target_id]['src_word'].append(
                                    word)
                                overlap_explanations[target_id]['src_role'].append(
                                    role)
                            else:
                                overlap_explanations[target_id] = {
                                    'tgt_role': [elm[0]],
                                    'tgt_word': [elm[1]],
                                    'src_word': [word],
                                    'src_role': [role]
                                }
        return overlap_explanations
