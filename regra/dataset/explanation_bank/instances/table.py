from typing import List, Dict
from regra.abc import Instance


class Table(Instance):
    def __init__(self, **kwargs):
        """Defines the table stores in explanation bank
        """
        self._id: str = kwargs.get('id')
        self._explanation: List[Dict] = kwargs.get('explanation')
        self._sentence_explanation: List[str] = kwargs.get(
            'sentence_explanation')
        self._table_name: str = kwargs.get('table_name')
        self._filtered_explanation = kwargs.get('filtered_explanation')

    def __call__(self):
        return {
            'id': self._id,
            'explanation': self._explanation,
            'sentence_explanation': self._sentence_explanation,
            'table_name': self._table_name,
            'filtered_explanation': self._filtered_explanation
        }

    def __str__(self):
        return ' '.join(self._sentence_explanation).strip() + ' | ' + self._table_name

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return self._id == other._id
