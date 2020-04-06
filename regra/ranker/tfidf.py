from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
from nltk.corpus import stopwords
import numpy as np

class TFIDF: 
 
    def fit(self, corpus, question_train, ids, question_train_ids): 
        self.corpus = corpus
        self.ids = ids 
        self.question_ids = question_train_ids 
        self.stopWords = stopwords.words('english')
        self.joined_corpus = []
        self.question_train = question_train
        for fact in corpus:
            self.joined_corpus.append(" ".join(fact))
        self.vectorizer = TfidfVectorizer(stop_words = self.stopWords).fit(self.joined_corpus + self.question_train) 
        self.vectorizer_questions = TfidfVectorizer(stop_words = self.stopWords).fit(self.joined_corpus + self.question_train) 
        self.transformed_corpus = self.vectorizer.transform(self.joined_corpus)
        self.transformed_corpus_questions = self.vectorizer_questions.transform(self.question_train)

    def query(self, query):    
        ordered_ids = []
        scores = []
            
        transformed_query = self.vectorizer.transform(query)
        TFIDF_dist = cosine_distances(transformed_query, self.transformed_corpus)
        res = []

        for index in np.argsort(TFIDF_dist)[0]:
            t_id = self.ids[index]
            score = 1 - TFIDF_dist[0][index]
            res.append({"id": t_id, "score": score})

        return res

    def question_similarity(self, query):    
        ordered_ids = []
        scores = []
            
        transformed_query = self.vectorizer_questions.transform(query)
        TFIDF_dist = cosine_distances(transformed_query, self.transformed_corpus_questions)
        res = []

        for index in np.argsort(TFIDF_dist)[0]:
            t_id = self.question_ids[index]
            score = 1 - TFIDF_dist[0][index]
            res.append({"id": t_id, "score": score})

        return res