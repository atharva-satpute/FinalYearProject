import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def score1(document1, document2):
    
    combined = []
    combined.append(' '.join(document1))
    combined.append(' '.join(document2))
    
    tfidf = TfidfVectorizer(stop_words='english')
    result = tfidf.fit_transform(combined)
    
    return result,tfidf

def score2(document1:list, document2:list):
    model = Word2Vec.load('./trained_sg.model')
    
    def mean_vector(model,wordsTokens:list):
        return np.mean(model.wv[wordsTokens],axis = 0)
    
    meanVector1, meanVector2 = mean_vector(model,document1),mean_vector(model,document2)
    return cosine_similarity([meanVector1],[meanVector2])

def score3(document1, document2):
    
    product1 = document1['product']
    product2 = document2['product']
    
    component1 = document1['component']
    component2 = document2['component']
    
    score = 0
    if product1==product2 and component1==component2:
        score = 1.0
    elif product1==product2 or component1==component2:
        score = 0.5
    else:
        score = 0.0
        
    return score
