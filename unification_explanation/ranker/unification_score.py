
class UnificationScore():

    def __init__(self, ranker, explanation_KB):
        self.ranker = ranker
        self.EKB = explanation_KB

    def compute(self, q_id:str, query:str, sim_questions_limit:int, facts_limit:int):
        similar_questions = self.ranker.question_similarity([query])[:sim_questions_limit]
        unification_score = {}
        for i in range(len(similar_questions)):
            if similar_questions[i]["id"] == q_id:
                continue
            for exp in self.EKB[similar_questions[i]["id"]]['_explanation']:
                if not exp in unification_score:
                    unification_score[exp] = 0
                unification_score[exp] += similar_questions[i]["score"]
        filtered_unification_score = {}
        for key in sorted(unification_score, key=unification_score.get, reverse=True)[:facts_limit]:
            filtered_unification_score[key] = unification_score[key]
        return filtered_unification_score
