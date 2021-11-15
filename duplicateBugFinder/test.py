from pymongo import MongoClient
#Sklearn
from sklearn.metrics.pairwise import cosine_similarity
from scores import score1
from processing import processDocument

client = MongoClient('localhost',27017)
db = client['eclipse']
collection = db['initial']

bug1_document = collection.find_one({"bug_id":"214301"})
bug2_document = collection.find_one({"bug_id":"214611"})

processed_bug_1 = processDocument(bug1_document)
processed_bug_2 = processDocument(bug2_document)

matrix, tfidf= score1(processed_bug_1, processed_bug_2)

_score1 = cosine_similarity(matrix[0,:], matrix[1,:])

print("similarity: ", cosine_similarity(matrix[0,:], matrix[1,:]))
