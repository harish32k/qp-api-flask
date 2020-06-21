from flask_restful import Resource, reqparse
from db import query
import pymysql

"""
This module is used to retrieve the data 
for all the request_no's which have a false or a 0 select_status.
This is done by selecting distinct request_no's from requests table 
for those rows where select_status = 0
"""

#AdminReqNoDetails class is to interact with the requests table.
class AdminReqNoDetails(Resource):
    
    def get(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('request_no', type=int, required=True, help="request_no cannot be left blank!")
        data = parser.parse_args()
        #create query string
        qstr = f""" SELECT r_id,request_no,image FROM requests WHERE request_no = {data['request_no']}; """
        try:
            return query(qstr)
        except:
            return {
                "message" : "There was an error connecting to the requests table while retrieving."
            }, 500
