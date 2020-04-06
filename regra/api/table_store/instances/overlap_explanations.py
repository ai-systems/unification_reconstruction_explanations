from regra.abc import Instance


class OverlapExplanation(Instance):
    def __init__(self, tgt_role: str, word: str, src_role: str = None):
        self.src_role = src_role
        self.tgt_role = tgt_role
        self.word = word

    def __eq__(self, other):
        return self.src_role == other.src_role and self.tgt_role == other.tgt_role and self.word == other.word
