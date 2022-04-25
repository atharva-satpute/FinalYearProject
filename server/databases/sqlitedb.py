# Build-in imports
import ast
import os
import sqlite3
from sqlite3 import Error
from threading import Lock

#Local imports
from databases.base_db import DB


lock = Lock()

columnNames = [
    'bug_id','product','description','bug_severity','short_desc',
    'priority','version','component','delta_ts','bug_status',
    'creation_ts','resolution'
    ]

processedColumnNames = ['bug_id','data','product','component']

# 0-> original table   1-> processed table
def tupleToDict(row,type):
    if row is None:
        return None
    if type == 0:
        return dict(zip(columnNames,list(row)))
    return dict(zip(processedColumnNames,list(row)))

class Sqlite(DB):
    
    def __init__(self, connection_url, database, collection):
        super().__init__(connection_url, database, collection)
        self.collection = collection
        self.processed_collection = self.collection + 'Processed'
        try:
            self.conn = sqlite3.connect(
                os.path.join(connection_url,database + '.db'),
                check_same_thread=False
            )
            self.cursor = self.conn.cursor()
        except Error as e:
            print("Connection Error:",e)
        else:
            # Change the variable names according to the requirements.
            # queryDrop = f"drop table if exists {self.processed_collection}"
            # self.cursor.execute(queryDrop)
            # print('Table Dropped')
            processedDataTable = f""" 
                CREATE TABLE {self.processed_collection} (
                    bug_id VARCHAR(255) NOT NULL,
                    data TEXT NOT NULL, 
                    product VARCHAR(255) NOT NULL,
                    component VARCHAR(255) NOT NULL
                );"""
            try:
                lock.acquire(True)
                self.cursor.execute(processedDataTable)
            except Error as e:
                print("Processed table not created",e)
            else:
                print(self.processed_collection, ' table created!!')
            finally:
                lock.release()
            

    def getReportById(self, bug_id):
        query = f"""
                    SELECT * 
                    FROM {self.collection} 
                    WHERE bug_id = '{bug_id}'
                """
        try:
            lock.acquire(True)
            result = self.cursor.execute(query).fetchone()
        finally:
            lock.release()
        return tupleToDict(result,0) if result is not None else None

    def addProcessedReport(self, processed_bug_report):
        query = """
            INSERT INTO %s (bug_id,data,product,component)
            VALUES (?,?,?,?)
        """ % (self.processed_collection)
        params = (processed_bug_report['bug_id'],str(processed_bug_report['data']),processed_bug_report['product'],processed_bug_report['component'])
        try:
            lock.acquire(True)
            self.cursor.execute(query,params)
            self.conn.commit()
        except Error as e:
            print(f'Failed to insert data into {self.processed_collection} table',e)
        else:
            print(self.cursor.rowcount," rows inserted!!!")
        finally:
            lock.release()

    def getProcessedReportById(self, bug_id):
        query = """
                    SELECT * 
                    FROM %s
                    WHERE bug_id = %s
                """ % (self.processed_collection,bug_id)
        try:
            lock.acquire(True)
            result = self.cursor.execute(query).fetchone()
            result_dict = None
            if result is not None:
                result_dict = tupleToDict(result,1)
                result_dict['data'] = ast.literal_eval(result_dict['data'])
        finally:
            lock.release()
        return result_dict

    def getProcessedReportsWithProductAndComponent(self, product, component):
        query = """
                    SELECT * 
                    FROM %s
                    WHERE (product = ? AND component = ?)
                """ % (self.processed_collection)
        params = (product,component)
        try:
            lock.acquire(True)
            result = self.cursor.execute(query,params)
        finally:
            lock.release()
        return result
    
    def close(self):
        self.conn.close()