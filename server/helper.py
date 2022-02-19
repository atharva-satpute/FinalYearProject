from FinalYearProject.dbrd.processing import cleaning, tokenize, removeStopwords, processDocument, wordStemming
import gensim
from FinalYearProject.dbrd.scores import score1, score2, score3

from databases.mongodb import MongoDB

db = None
skip_gram_model = None


def initialize(args):
    global db, skip_gram_model

    if not skip_gram_model:
        skip_gram_model = gensim.models.Word2Vec.load(
            "../dbrd/trained_model/trained_sg_270122_2_corpus_ds.model", mmap='r')

    if not db:
        if args["database_type"] == 1:
            db = MongoDB(args["database_url"], args["database_name"], args["collection_name"])
        else:
            pass


def process(bug_report):
    _id = db.addReport(bug_report)
    if not _id:
        return "Error"

    processed_document = processDocument(bug_report)
    processed_bug_report = {
        "bug_id": bug_report['bug_id'],
        "data": processed_document,
        "product": bug_report['product'],
        "component": bug_report['component']
    }
    _id = db.addProcessedReport(processed_bug_report)
    if not _id:
        return "Error"

    findDuplicates(processed_bug_report)
    return "Success"


def findDuplicates(processed_document):
    cur = db.getProcessedReportsWithProductAndComponent(processed_document['product'], processed_document['component'])

    for doc in cur:
        score = calculateScore(processed_document, doc)
        print(doc['_id'], score)
        # print("Score with {} is {}".format(doc['_id'], score))


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
