class DB:

    def __init__(self, connection_url, database, collection):
        self.CONNECTION_URL = connection_url
        self.database_name = database
        self.collection = collection
        self.processed_collection = collection + "_processed"

    def getReportById(self, bug_id):
        pass

    def addReport(self, bug_report):
        pass

    def addProcessedReport(self, processed_bug_report):
        pass

    def getProcessedReportById(self, bug_id):
        pass

    def getProcessedReportsWithProductAndComponent(self, product, component):
        pass

