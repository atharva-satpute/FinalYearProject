# Built-in Libraries
import argparse
import os
import sys
import yaml

# Third-party Libraries
from flask_cors import CORS
from flask import Flask, jsonify, request

# Local Libraries
from Constants.Codes import error_codes
from helper import process, initialize
from models.Response import Response

# This file's directory path
PATH = sys.path[1]


# Loading configurations
"""
    os.sep used to so that program can run on different OSs
    Windows: '\\'
    MacOS & Linux: '/'

"""
with open(os.path.join(PATH + os.sep,'config.yaml'),'r') as configFile:
    config = yaml.safe_load(configFile)
configFile.close()


ap = argparse.ArgumentParser()
ap.add_argument("-db_url", "--database_url", required=True, help="URL to connect to database")
ap.add_argument("-db_type", "--database_type", default=1, help="1 for NOSQL, 2 for RDBMS")
ap.add_argument("-db_name", "--database_name", required=True, help="Name of the database to deal with")
ap.add_argument("-col_name", "--collection_name", required=True, help="Name of the collection")

args = vars(ap.parse_args())

# Initializing
app = Flask(__name__)
CORS(app)

# Back-end Routes
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


# React Routes
@app.route('/upload', methods=['POST'])
def fileUpload():
    uploadedFile = request.files['file']
    if uploadedFile.name != '':
        uploadedFile.save('./uploads' + uploadedFile.filename)
        return jsonify({"Success": 200})


if __name__ == "__main__":
    initialize(args)
    app.run(
        host = config['flaskserver']['host'],
        port = config['flaskserver']['port']
    )