# Built-in Libraries
import ast
from flask import jsonify
import os
import pandas as pd
import sys

# Initially sys.path[0] will be './FinalYearProject/server'
sys.path.insert(0,os.path.dirname(sys.path[0]))
""" 
    After execution of the above statement 
    sys.path[0] will './FinalYearProject' and sys.path[1] will be './FinalYearProject/server' 
    
"""


# Third-party libraries
import gensim

# Local Libraries
from databases.mongodb import MongoDB
from databases.sqlitedb import Sqlite, tupleToDict
from dbrd.processing import cleaning, tokenize, removeStopwords, processDocument, wordStemming
from dbrd.scores import score1, score2, score3


db = None
skip_gram_model = None
db_type = None
FILE_PATH = os.path.join(sys.path[1] + os.sep,"uploads" + os.sep)


def initialize(args):
    global db, skip_gram_model,db_type


    if not skip_gram_model:
        try:
            skip_gram_model = gensim.models.Word2Vec.load(
                os.path.join(sys.path[0],"dbrd","trained_model","trained_sg.model"), mmap='r')
        except FileNotFoundError as err:
            print('Cannot find model:',err.filename)
            exit(0)

    if not db:
        if args["database_type"] == 1:
            db_type = 1
            db = MongoDB(args["database_url"], args["database_name"], args["collection_name"])
        else:
            db_type = 2
            db = Sqlite(args["database_url"], args["database_name"], args["collection_name"])


def process(bug_id):

    processed_bug_report = db.getProcessedReportById(bug_id)
    if processed_bug_report is None:
        bug_report = db.getReportById(bug_id)

        # If report with id=bug_id is not present in the database
        if bug_report is None:
            return jsonify({})

        # Preprocess the document
        processed_document = processDocument(bug_report)
    
        processed_bug_report = {
            "bug_id": bug_report['bug_id'],
            "data": processed_document,
            "product": bug_report['product'],
            "component": bug_report['component']
        }

        # Add the new report to processed collection
        db.addProcessedReport(processed_bug_report)

    possible_duplicate = findDuplicates(processed_bug_report)
    if not possible_duplicate:
        return None
    else:
        return possible_duplicate


def findDuplicates(processed_document):
    '''

        Fetching documents from processed collection based on the product and
        component value.

    '''
    cursor = db.getProcessedReportsWithProductAndComponent(processed_document['product'],
                                                           processed_document['component'])

    if db_type == 1:
        scores = [(calculateScore(processed_document, doc), doc['bug_id']) for doc in cursor]
    else:
        scores = []
        for doc in cursor:

            # Each row fetched from the database will be contained in a tuple
            # and needs to be converted to a dictionary for further processing
            doc = tupleToDict(doc,1)

            #Converting string list to python list
            doc['data'] = ast.literal_eval(doc['data'])

            scores.append((calculateScore(processed_document, doc), doc['bug_id']))

    # Sorting the similarity scores in descending order
    scores.sort(key=lambda i: i[0], reverse=True)

    # here we can apply top-k approach for better accuracy
    # print("Scores:",scores)
    # return scores[0][1] if scores[0][0][0][0] >= 1.5 else None
    return jsonify(
        result=[
                {score[1]:score[0][0][0]} for score in scores if score[0][0][0] >= 0.95 and
                score[1] != processed_document['bug_id']
            ])


def calculateScore(document1, document2):
    _score1 = score1(wordStemming(document1['data']), wordStemming(document2['data']))
    _score2 = score2(document1['data'], document2['data'], skip_gram_model)
    _score3 = score3(document1, document2)

    score = (_score1 + _score2) * _score3

    return score

def processDocument(document):
    content_of_interest = document['description'] + document['short_desc']  # COI

    cleanedCOI = cleaning(content_of_interest)
    tokenized_COI = tokenize(cleanedCOI)
    COI_without_sw = removeStopwords(tokenized_COI)

    return COI_without_sw

def getBugReport(bug_id):
    return db.getReportById(bug_id)

def handleFile(fileName):
    data = pd.read_csv(FILE_PATH + fileName, header=None)
    return list(data[0])

def closeConnections():
    print('Closing connections!!')
    db.close()