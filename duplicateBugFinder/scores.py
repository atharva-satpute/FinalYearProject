import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer

def score1(document1, document2):
    
    combined = []
    combined.append(' '.join(document1))
    combined.append(' '.join(document2))
    
    tfidf = TfidfVectorizer(stop_words='english')
    result = tfidf.fit_transform(combined)
    
    return result,tfidf
