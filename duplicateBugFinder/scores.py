import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer

def score1(document1, document2):
    
    combined = []
    combined.append(' '.join(document1))
    combined.append(' '.join(document2))
    
    tfidf = TfidfVectorizer(stop_words='english')
    result = tfidf.fit_transform(combined)
    
    return result,tfidf

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
        
    return score;
