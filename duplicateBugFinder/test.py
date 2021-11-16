from pymongo import MongoClient
#Sklearn
from sklearn.metrics.pairwise import cosine_similarity
from scores import score1, score3
from processing import processDocument

client = MongoClient('localhost',27017)
db = client['eclipse']
collection = db['initial']

bug1_document = collection.find_one({"bug_id":"21"})
bug2_document = collection.find_one({"bug_id":"22"})

processed_bug_1 = processDocument(bug1_document)
processed_bug_2 = processDocument(bug2_document)

matrix, tfidf= score1(processed_bug_1, processed_bug_2)

_score1 = cosine_similarity(matrix[0,:], matrix[1,:])

# Take input from function
_score2 = 1

_score3 = score3(bug1_document, bug2_document)

_score = (_score1 + _score2) * _score3

print("similarity: ", cosine_similarity(matrix[0,:], matrix[1,:]))
print("Score3: ", _score3)

print("Score: ", _score)
