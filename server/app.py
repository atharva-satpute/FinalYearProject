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
    "bug_id": "19",
    "product": "Platform",
    "description": "I should be able to pick a stream from the respository and catchup to the stream.\nInstead I must select projects within the stream and \"add to workspace\".\nThis is annoying because it doesn't merge it bashes, and besides it warns you\nabout every project that you already have loaded.\n\nBasically, it should work the same as picking the individual projects from the navigator\nand catching up, except instead I'm picking the stream to denote the set of projects.\n\nNOTES:\n\nBB (17/04/2001 9:57:55 PM)\n\tNote that the lineup of projects in a stream (at least for CVS) is not necessarily\n\tmeaningful, because projects added to one stream will show up in all other\n\tstreams in the same repository. A new project in a stream is also not an incoming\n\tcreation of the project; you would have to use project references for transitive\n\tloading or transitive catching up.\n\tIt would be useful, though, to have a global toolbar button which does a catchup\n\ton all shared projects.\n\nJean-Michel (4/25/01 9:14:46 AM)\n\t1GCQK5Y: ITPVCM:WINNT - Should be able to add HEAD to workspace\n\tMoving to time permitting.",
    "bug_severity": "normal",
    "dup_id": [],
    "short_desc": "[CVS Repo View] Should be able to pick a branch and catchup to it",
    "priority": "P4",
    "version": "2.0",
    "component": "Team",
    "delta_ts": "2004-11-09 21:38:05 -0500",
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
