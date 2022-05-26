# Built-in Libraries
import argparse
import json
import os
import sys
import yaml
from werkzeug.utils import secure_filename

# Third-party Libraries
from flask_cors import CORS
from flask import Flask, jsonify, request

# Local Libraries
from helper import process, initialize, getBugReport, handleFile, closeConnections

# This file's directory path
PATH = sys.path[1] + os.sep
UPLOAD_FILE_PATH = PATH + 'uploads'
os.makedirs(UPLOAD_FILE_PATH, exist_ok=True)


# Loading configurations
"""
    os.sep used to so that program can run on different OSs
    Windows: '\\'
    MacOS & Linux: '/'

"""
with open(PATH + 'config.yaml','r') as configFile:
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

# React Routes (.csv files)
@app.route('/upload', methods=['POST'])
def fileUpload():
    uploadedFile = request.files['file']
    if uploadedFile.filename != '':
        fileName = secure_filename(uploadedFile.filename)
        uploadedFile.save(os.path.join(UPLOAD_FILE_PATH,fileName))
        return jsonify(handleFile(fileName))

@app.route('/search/<bug_id>', methods=['GET','POST'])
def searchFile(bug_id):
    if request.method == 'GET':
        return json.dumps(getBugReport(bug_id),default=str)
    return process(bug_id)


if __name__ == "__main__":
    initialize(args)
    app.run(
        host = config['flaskserver']['host'],
        port = config['flaskserver']['port'],
        debug=True
    )
    closeConnections()