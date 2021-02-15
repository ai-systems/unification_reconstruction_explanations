import msgpack
import nltk
from nltk.corpus import stopwords
from tqdm import tqdm

from unification_explanation.ranker.bm25 import BM25
from unification_explanation.ranker.relevance_score import RelevanceScore
from unification_explanation.ranker.tfidf import TFIDF
from unification_explanation.ranker.unification_score import UnificationScore
from unification_explanation.ranker.utils import Utils

# Load table-store
with open("data/cache/table_store.mpk", "rb") as f:
    ts_dataset = msgpack.unpackb(f.read(), raw=False)

# Load train and dev set
with open("data/cache/eb_train.mpk", "rb") as f:
    eb_dataset_train = msgpack.unpackb(f.read(), raw=False)


with open("data/cache/eb_dev.mpk", "rb") as f:
    eb_dataset_dev = msgpack.unpackb(f.read(), raw=False)

# open output file
pred_q = open("prediction.txt", "w")

# Parameters
K = 5000  # relevance facts limit
Q = 100  # similar questions limit
QK = 85  # unification facts limit
weights = [0.83, 0.17]  # relevance and unification score weigths
eb_dataset = eb_dataset_dev  # test dataset
f_retriever = BM25()  # relevance model
q_retriever = BM25()  # question similarity model

utils = Utils()
utils.init_explanation_bank_lemmatizer()

# fitting the models
corpus = []
original_corpus = []
question_train = []
ids = []
q_ids = []

for t_id, ts in tqdm(ts_dataset.items()):
    # facts lemmatization
    if "#" in ts["_sentence_explanation"][-1]:
        fact = ts["_sentence_explanation"][:-1]
    else:
        fact = ts["_sentence_explanation"]
    lemmatized_fact = []
    original_corpus.append(fact)
    for chunck in fact:
        temp = []
        for word in nltk.word_tokenize(
            chunck.replace("?", " ")
            .replace(".", " ")
            .replace(",", " ")
            .replace(";", " ")
            .replace("-", " ")
        ):
            temp.append(utils.explanation_bank_lemmatize(word.lower()))
        if len(temp) > 0:
            lemmatized_fact.append(" ".join(temp))
    corpus.append(lemmatized_fact)
    ids.append(t_id)

for q_id, exp in tqdm(eb_dataset_train.items()):
    # concatenate question with candidate answer
    if exp["_answerKey"] in exp["_choices"]:
        question = (
            exp["_question"]
            .replace("?", " ")
            .replace(".", " ")
            .replace(",", " ")
            .replace(";", " ")
            .replace("-", " ")
            .replace("'", "")
            .replace("`", "")
        )
        candidate = (
            exp["_choices"][exp["_answerKey"]]
            .replace("?", " ")
            .replace(".", " ")
            .replace(",", " ")
            .replace(";", " ")
            .replace("-", " ")
            .replace("'", "")
            .replace("`", "")
        )
    else:
        question = (
            exp["_question"]
            .replace("?", " ")
            .replace(".", " ")
            .replace(",", " ")
            .replace(";", " ")
            .replace("-", " ")
            .replace("'", "")
            .replace("`", "")
        )
        candidate = ""
    question = question + " " + candidate
    temp = []
    # question lemmatization
    for word in nltk.word_tokenize(question):
        temp.append(utils.explanation_bank_lemmatize(word.lower()))
    lemmatized_question = " ".join(temp)
    question_train.append(lemmatized_question)
    q_ids.append(q_id)

f_retriever.fit(corpus, question_train, ids, q_ids)
q_retriever.fit(corpus, question_train, ids, q_ids)

# compute the explanation ranking for each question
for q_id, exp in tqdm(eb_dataset.items()):
    # concatenate question with the answer
    if exp["_answerKey"] in exp["_choices"]:
        question = (
            exp["_question"]
            .replace("?", " ")
            .replace(".", " ")
            .replace(",", " ")
            .replace(";", " ")
            .replace("-", " ")
            .replace("'", "")
            .replace("`", "")
        )
        candidate = (
            exp["_choices"][exp["_answerKey"]]
            .replace("?", " ")
            .replace(".", " ")
            .replace(",", " ")
            .replace(";", " ")
            .replace("-", " ")
            .replace("'", "")
            .replace("`", "")
        )
    else:
        question = (
            exp["_question"]
            .replace("?", " ")
            .replace(".", " ")
            .replace(",", " ")
            .replace(";", " ")
            .replace("-", " ")
            .replace("'", "")
            .replace("`", "")
        )
        candidate = ""
    question = question + " " + candidate

    # lemmatization and stopwords removal
    temp = []
    for word in nltk.word_tokenize(question):
        if not word.lower() in stopwords.words("english"):
            temp.append(utils.explanation_bank_lemmatize(word.lower()))
    lemmatized_question = " ".join(temp)

    # compute the explanation ranking
    RS = RelevanceScore(f_retriever)
    US = UnificationScore(q_retriever, eb_dataset_train)

    relevance_scores = RS.compute(lemmatized_question, K)
    unification_scores = US.compute(q_id, lemmatized_question, Q, QK)
    combined_scores = {}

    for t_id, ts in ts_dataset.items():
        if t_id in relevance_scores.keys() and t_id in unification_scores.keys():
            combined_scores[t_id] = (weights[0] * relevance_scores[t_id]) + (
                weights[1] * unification_scores[t_id]
            )
        elif t_id in relevance_scores.keys():
            combined_scores[t_id] = weights[0] * relevance_scores[t_id]
        elif t_id in unification_scores.keys():
            combined_scores[t_id] = weights[1] * unification_scores[t_id]
        else:
            combined_scores[t_id] = 0

    # save the final output
    for fact in sorted(combined_scores, key=combined_scores.get, reverse=True):
        to_write = q_id + "\t" + fact
        print(to_write, file=pred_q)

pred_q.close()
