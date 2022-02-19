from FinalYearProject.dbrd.processing import cleaning, tokenize, removeStopwords
import gensim

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
        "data": processed_document
    }
    _id = db.addProcessedReport(processed_bug_report)
    if not _id:
        return "Error"

    return "Success"


def processDocument(document):
    content_of_interest = document['description'] + document['short_desc']  # COI

    cleanedCOI = cleaning(content_of_interest)
    tokenized_COI = tokenize(cleanedCOI)
    COI_without_sw = removeStopwords(tokenized_COI)

    return COI_without_sw
