import os
import sys
sys.path.insert(1,os.getcwd())
from pymongo import MongoClient
from helper import processDocument

client = MongoClient('localhost',27017)
db = client['eclipse']
collection = db['initial']
processed_collection = db['initial_processed']

def process(bug_report):
    processed_document = processDocument(bug_report)
    
    processed_bug_report = {
        "bug_id": bug_report['bug_id'],
        "data": processed_document,
        "product": bug_report['product'],
        "component": bug_report['component']
    }

    processed_collection.insert_one(processed_bug_report)

cursor = collection.find().limit(400)
for doc in cursor:
    process(doc)
cursor.close()
client.close()