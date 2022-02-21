# Built-in Libraries
import argparse
import sys

# Third-party Libraries
from flask import Flask, jsonify, request

# Local Libraries
from Constants.Codes import error_codes
from helper import process, initialize
from models.Response import Response


ap = argparse.ArgumentParser()
ap.add_argument("-db_url", "--database_url", required=True, help="URL to connect to database")
ap.add_argument("-db_type", "--database_type", default=1, help="1 for NOSQL, 2 for RDBMS")
ap.add_argument("-db_name", "--database_name", required=True, help="Name of the database to deal with")
ap.add_argument("-col_name", "--collection_name", required=True, help="Name of the collection")

args = vars(ap.parse_args())
app = Flask(__name__)


@app.route("/status", methods=['GET'])
def hello_world():
    return vars(Response(error_codes['LP'], "Application is running...! Everything looks fine."))


@app.route("/insert", methods=['POST'])
def insertIntoDB():
    #try:
        data = request.json
        print(data)
        return process(data)
    #except:
        return vars(Response(error_codes['ISE'], "Something wrong happened at server side"))


if __name__ == "__main__":
    initialize(args)
    app.run()
