# Built-in Libraries
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def score1(document1, document2):
    combined = [' '.join(document1), ' '.join(document2)]

    tfidf = TfidfVectorizer(stop_words='english')
    result = tfidf.fit_transform(combined)

    return cosine_similarity(result[0, :], result[1, :])[0]


def mean_vector(model, words_tokens: list):
    return np.mean(model.wv[words_tokens], axis=0)


def score2(document1: list, document2: list, model):
    meanVector1, meanVector2 = mean_vector(model, document1), mean_vector(model, document2)
    return cosine_similarity([meanVector1], [meanVector2])


def score3(document1, document2):
    product1 = document1['product']
    product2 = document2['product']

    component1 = document1['component']
    component2 = document2['component']

    score = 0.0
    if product1 == product2 and component1 == component2:
        score = 1.0
    elif product1 == product2 and component1 != component2:
        score = 0.75

    return score
