import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer

def score1(document):
    # Combining title and description as one string
    string = [document['short_desc'] +' ' + document['description']]
    
    # Initializing tfid
    tfidf = TfidfVectorizer(stop_words='english')
    result = tfidf.fit_transform(string)
    return result,tfidf