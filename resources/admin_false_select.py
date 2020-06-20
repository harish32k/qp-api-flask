from flask_restful import Resource, reqparse
from db import query
import pymysql

"""
This module is used to retrieve the data 
for all the request_no's which have a false or a 0 select_status.
This is done by selecting distinct request_no's from requests table 
for those rows where select_status = 0
"""

#AdminFalseSelect class is to interact with the requests table.
class AdminFalseSelect(Resource):
    
    def get(self):
        
        #create query string
        qstr = f""" select DISTINCT request_no FROM requests WHERE select_status = 0; """
        try:
            return query(qstr)
        except:
            return {
                "message" : "There was an error connecting to the requests table while retrieving."
            }, 500
