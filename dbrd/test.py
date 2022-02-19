from pymongo import MongoClient
#Sklearn
from sklearn.metrics.pairwise import cosine_similarity
from scores import score1, score2, score3
from processing import processDocument

import warnings
warnings.filterwarnings('ignore')

client = MongoClient('localhost',27017)
db = client['eclipse']
collection = db['initial']

bug1_document = collection.find_one({"bug_id":"20"})
bug2_document = collection.find_one({"bug_id":"40"})

processed_bug_1 = processDocument(bug1_document,1)
processed_bug_2 = processDocument(bug2_document,1)

matrix, tfidf = score1(processed_bug_1, processed_bug_2)

_score1 = cosine_similarity(matrix[0,:], matrix[1,:])[0]

# Take input from function
processed_bug_1_s2 = list(processDocument(bug1_document,2))
processed_bug_2_s2 = list(processDocument(bug2_document,2))

_score2 = score2(processed_bug_1_s2,processed_bug_2_s2)[0]

_score3 = score3(bug1_document, bug2_document)

_score = (_score1 + _score2) * _score3

print("Score 1: ", _score1)
print("Score 2:", _score2)
print("Score 3: ", _score3)
print("Final Score: ", _score)
