# Built-in Libraries
from flask import jsonify
import json
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
from Constants.Codes import error_codes
from databases.mongodb import MongoDB
from dbrd.processing import cleaning, tokenize, removeStopwords, processDocument, wordStemming
from dbrd.scores import score1, score2, score3
from models.Response import Response


db = None
skip_gram_model = None
FILE_PATH = os.path.join(sys.path[1] + os.sep,"uploads" + os.sep)


def initialize(args):
    global db, skip_gram_model


    if not skip_gram_model:
        skip_gram_model = gensim.models.Word2Vec.load(
            os.path.join(sys.path[0],"dbrd","trained_model","trained_sg.model"), mmap='r')

    if not db:
        if args["database_type"] == 1:
            db = MongoDB(args["database_url"], args["database_name"], args["collection_name"])
        else:
            pass


def process(bug_id):
    # _id = db.addReport(bug_report)
    # if not _id:
    #     return "Error"
    processed_bug_report = db.getProcessedReportById(bug_id)
    if processed_bug_report is None:
        bug_report = db.getReportById(bug_id)

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
        res = vars(Response(error_codes['SS'], "No duplicate found. The bug report has been added into the database."))
        print(res)
        return res
    else:
        # res = vars(
        #     Response(error_codes['SS'], "Bug report with id {}, is a possible duplicate.".format(possible_duplicate)))
        # print(res)
        # return res
        return possible_duplicate


def findDuplicates(processed_document):
    '''

        Fetching documents from processed collection based on the product and
        component value.

    '''
    cursor = db.getProcessedReportsWithProductAndComponent(processed_document['product'],
                                                           processed_document['component'])

    scores = [(calculateScore(processed_document, doc), doc['bug_id']) for doc in cursor]

    # Sorting the similarity scores in descending order
    scores.sort(key=lambda i: i[0], reverse=True)

    # here we can apply top-k approach for better accuracy
    # print("Scores:",scores)
    # return scores[0][1] if scores[0][0][0][0] >= 1.5 else None
    return jsonify(
        result=[
                {score[1]:score[0][0][0]} for score in scores if score[0][0][0] >= 0.95
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