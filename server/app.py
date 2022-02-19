import argparse
from flask import Flask, jsonify
from helper import process, initialize
import sys

sys.path.append(".")

ap = argparse.ArgumentParser()
ap.add_argument("-db_url", "--database_url", required=True, help="URL to connect to database")
ap.add_argument("-db_type", "--database_type", default=1, help="1 for NOSQL, 2 for RDBMS")
ap.add_argument("-db_name", "--database_name", required=True, help="Name of the database to deal with")
ap.add_argument("-col_name", "--collection_name", required=True, help="Name of the collection")

args = vars(ap.parse_args())
app = Flask(__name__)


data = {
    "bug_id": "22",
    "product": "Platform",
    "description": "Project descriptions don't store sharing recommendations and project version references yet, but they should.\n\nNOTES:\n\nJean-Michel (4/6/01 12:39:12 PM)\n\tWe will live with unqualified project references for now.",
    "bug_severity": "normal",
    "dup_id": [],
    "short_desc": "persist sharing recommendations and project version references (1GBOA19)",
    "priority": "P3",
    "version": "2.0",
    "component": "Team",
    "delta_ts": "2002-04-08 14:42:00 -0400",
    "bug_status": "RESOLVED",
    "creation_ts": "2001-10-10 21:35:00 -0400",
    "resolution": "WONTFIX"
}


@app.route("/")
def hello_world():
    return jsonify("Hello, World!!")


@app.route("/insert")
def insertIntoDB():
    res = process(data)
    print("Added successfully!!" + res)
    return jsonify("Added successfully!!" + res)


if __name__ == "__main__":
    initialize(args)
    app.run()
