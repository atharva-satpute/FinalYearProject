from pymongo import MongoClient
from processing import processDocument

client = MongoClient('localhost',27017)
db = client['eclipse']
collection = db['initial']

fields = {'_id': 0,'bug_id':1,'product':1,'description':1,'short_desc':1,'component':1}
BATCH_SIZE = 1000    

with open('sentences1.txt','w') as file:
    cursor = collection.find({},fields,no_cursor_timeout=True)
    doc = None
    string = ""
    count = 1
    while True:
        string = ""
        for _ in range(BATCH_SIZE):
            doc = next(cursor,None)
            if doc:
                string += str({doc["bug_id"]:list(processDocument(doc,2))}) + '\n'
            else:
                break
        file.write(string)
        print("Batch {} done!".format(count))
        count += 1
        if doc == None:
            break
    cursor.close()
file.close
client.close()