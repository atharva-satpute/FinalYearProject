import os
import sqlite3
from pymongo import MongoClient
from sqlite3 import Error
import sys
sys.path.insert(1,os.getcwd())
from helper import processDocument

FILE_PATH = os.path.join(sys.path[1],'databases') + os.sep
    
try:
    conn = sqlite3.connect(FILE_PATH + 'reports.db')
except Error as e:
    print(e)
else:
    sqlCursor = conn.cursor()


# MongoDB connection
client = MongoClient('localhost',27017)
db = client['eclipse']
collection = db['initial']

table1 = """ CREATE TABLE IF NOT EXISTS initial (
            bug_id  VARCHAR(255) NOT NULL,
            product VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            bug_severity VARCHAR(255) NOT NULL,
            short_desc TEXT NOT NULL,
            priority VARCHAR(255) NOT NULL,
            version VARCHAR(255) NOT NULL,
            component VARCHAR(255) NOT NULL,
            delta_ts VARCHAR(255) NOT NULL,
            bug_status VARCHAR(255) NOT NULL,
            creation_ts VARCHAR(255) NOT NULL,
            resolution VARCHAR(255) NOT NULL
        ); """

table2 = """ CREATE TABLE IF NOT EXISTS initialProcessed (
            bug_id  VARCHAR(255) NOT NULL,
            data    TEXT NOT NULL, 
            product VARCHAR(255) NOT NULL,
            component VARCHAR(255) NOT NULL
        ); """
    
if sqlCursor.execute("Drop table if exists initial") is not None:
    print("Table1 initially created dropped!!")

if sqlCursor.execute("Drop table if exists initialProcessed") is not None:
    print("Table2 initially created dropped!!")

if sqlCursor.execute(table1) is not None:
    print("Table1 Created!!")

if sqlCursor.execute(table2) is not None:
    print("Table2 Created!!")


cursor = collection.find().batch_size(1000)
records = [
    (
        str(doc['bug_id']),
        str(doc['product']),
        str(doc['description']),
        str(doc['bug_severity']),
        str(doc['short_desc']),
        str(doc['priority']),
        str(doc['version']),
        str(doc['component']),
        str(doc['delta_ts']),
        str(doc['bug_status']),
        str(doc['creation_ts']),
        str(doc['resolution'])
    )
    for doc in cursor
]

query = "INSERT INTO 'initial' VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
sqlCursor.executemany(query,records)
conn.commit()

print("Inserted",sqlCursor.rowcount,'rows successfully')


def process(bug_report):
    processed_document = processDocument(bug_report)
    
    processed_bug_report = {
        "bug_id": bug_report['bug_id'],
        "data": processed_document,
        "product": bug_report['product'],
        "component": bug_report['component']
    }

    query = """
            INSERT INTO initialProcessed (bug_id,data,product,component)
            VALUES (?,?,?,?)
        """
    params = (processed_bug_report['bug_id'],str(processed_bug_report['data']),processed_bug_report['product'],processed_bug_report['component'])
    try:
        sqlCursor.execute(query,params)
        conn.commit()
    except Error as e:
        print(f'Failed to insert data into initialProcessed table',e)

client = MongoClient('localhost',27017)
db = client['eclipse']
collection = db['initial']
cursor = collection.find().limit(2000)
for doc in cursor:
    process(doc)
    print(doc['bug_id'],'\r',end='')

conn.close()
cursor.close()
client.close()