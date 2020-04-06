import glob
import os
import re
from collections import defaultdict
from functools import partial, reduce
from typing import Dict, List

import luigi
import msgpack
import numpy as np
import pandas as pd
from overrides import overrides
from tqdm import tqdm

from regra.common.util import custom_deserialize, custom_serialize
from regra.dataset.abc import MsgPackDataset

from .instances import QuestionExplanation, Table
from .table_store_dataset import TableStoreDataset

# row header constants
QID = 'questionID'
EXPLANATION = 'explanation'
QUESTION = 'Question'
# COLLING_EXPLANATION = 'notes (COLING2016 explanations)'
# KNOWLEDGE_TYPE = 'knowledgetype'
# SCHOOL_GRADE = 'schoolGrade'
ANSWER_KEY = 'AnswerKey'


QUESTION_CACHE = 'explanationbank.mpk'


class ExplanationBankDataset(MsgPackDataset):

    question_explanation_path = luigi.Parameter(default=None)

    def output(self):
        table_store_dataset = self.input().load()
        return super(ExplanationBankDataset, self).output(transform=partial(ExplanationBankDataset.map_explanations, table_store_dataset))

    @overrides
    def requires(self):
        return TableStoreDataset(mode=self.mode, config_file=self.config_file)

    @overrides
    def run(self):
        """Cache table store and expalnation bank path
        """
        table_store_dataset = self.input().load()
        self.logger.info(
            f'Loading explanation bank dataset from {self.question_explanation_path}')
        expl_dataset = ExplanationBankDataset.process_sheet(
            self.question_explanation_path, table_store_dataset)
        self.logger.info('Caching explanation bank')
        self.output().dump(expl_dataset)

    @property
    def cache_path(self):
        return f'{self.path}/{QUESTION_CACHE}'

    @staticmethod
    def process_sheet(question_explanation_path: str, table_store_dataset: TableStoreDataset) -> Dict[str, QuestionExplanation]:
        expl_df = pd.read_csv(question_explanation_path,
                              sep='\t', encoding='utf-8')
        expl_items = {}
        choices_re = [('A', re.compile('(?<=\([A]\)).*(?=\([B]\))')), ('B', re.compile('(?<=\([B]\)).*(?=\([C]\))')),
                      ('C', re.compile('(?<=\([C]\)).*(?=\([D]\))')), ('D', re.compile('(?<=\([D]\)).*'))]
        question_re = re.compile('\([ABCD]\).*')
        for _, row in tqdm(expl_df.iterrows(), total=expl_df.shape[0]):
            # Check for nan values.
            # WARNING: Sometimes explanation is empty
            if not pd.isna(row[EXPLANATION]) and not pd.isna(row[QUESTION]):
                id = row[QID]
                question = row[QUESTION]
                choices = {choice_re[0]: choice_re[1].findall(question)[0].strip() if len(choice_re[1].findall(question)) > 0 else ''
                           for choice_re in choices_re}
                answerkey = row[ANSWER_KEY]
                # List of explanation ids
                explanation = {expl.split('|')[0]: expl.split('|')[1]
                               for expl in row[EXPLANATION].split(' ') if table_store_dataset[expl.split('|')[0]] is not None}
                # Filter to those only exisiting in table stores

                # colling_expalanation = row[COLLING_EXPLANATION].split(
                # ' ') if not pd.isna(row[COLLING_EXPLANATION]) else []
                # knowledge_type = row[KNOWLEDGE_TYPE]
                # school_grade = row[SCHOOL_GRADE]
                question_explanation = QuestionExplanation(
                    id=id,
                    question=question_re.sub('', question).strip(),
                    explanation=explanation,
                    # colling_expalanation=colling_expalanation,
                    # knowledge_type=knowledge_type,
                    # school_grade=school_grade,
                    choices=choices,
                    answerKey=answerkey)
                expl_items[id] = question_explanation
        return defaultdict(lambda: None, expl_items)

    @staticmethod
    def map_explanations(table_store_dataset: TableStoreDataset, expl_dataset: Dict[str, QuestionExplanation]) -> Dict[str, QuestionExplanation]:
        """Mapping explanations id to Tables
        """
        return reduce(lambda dataset, q_expl: {**dataset,
                                               q_expl[0]: QuestionExplanation(**{**q_expl[1](),
                                                                                 'explanation': {table_store_dataset[id]: role for id, role in q_expl[1]()['explanation'].items()}})},

                      expl_dataset.items(), {})
