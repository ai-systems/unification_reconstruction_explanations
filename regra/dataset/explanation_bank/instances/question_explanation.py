from typing import List, Dict, Tuple
from regra.abc import Instance


class QuestionExplanation(Instance):
    def __init__(self,  **kwargs):
        """Defines the question explanation model in explanation bank 
        """
        self._id: str = kwargs.get('id')
        self._question = kwargs.get('question')
        self._explanation = kwargs.get('explanation')
        self._choices = kwargs.get('choices')
        self._answerKey = kwargs.get('answerKey')
        self._colling_explanation: List[str] = kwargs.get(
            'colling_explanation')
        self._knowledge_type: str = kwargs.get('knowledge_type')
        self._school_grade: str = kwargs.get('school_grade')

    def __call__(self):
        return {
            'id': self._id,
            'explanation': self._explanation,
            'question': self._question,
            'colling_explanation': self._colling_explanation,
            'knowledge_type': self._knowledge_type,
            'school_grade': self._school_grade,
            'choices': self._choices,
            'answerKey': self._answerKey,
        }

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return self._id == other._id
