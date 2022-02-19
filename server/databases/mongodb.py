
from pymongo import MongoClient
from FinalYearProject.server.databases.base_db import DB


class MongoDB(DB):

    def __init__(self, connection_url, database, collection):
        super().__init__(connection_url, database, collection)
        self.client = MongoClient(connection_url)
        self.db = self.client.get_database(self.database_name)

    def getReportById(self, bug_id):
        query = {"bug_id": bug_id}
        query_report = self.db[self.collection].find_one(query)
        return query_report

    def addReport(self, bug_report):
        _id = self.db[self.collection].insert_one(bug_report)
        return _id

    def addProcessedReport(self, processed_bug_report):
        _id = self.db[self.processed_collection].insert_one(processed_bug_report)
        return _id

    def getProcessedReportById(self, bug_id):
        query = {"bug_id": bug_id}
        query_report = self.db[self.processed_collection].find_one(query)
        return query_report

    def getProcessedReportsWithProductAndComponent(self, product, component):
        query = {"product" : product,
                 "component": component}
        query_reports = self.db[self.processed_collection].find(query)
        return query_reports
