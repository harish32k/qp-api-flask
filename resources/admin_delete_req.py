from flask_restful import Resource, reqparse
from db import query
import pymysql

""" 
The resource in this module is used to delete all the entries(requests) in the requests table 
having a particular 'request_no' with a 'select_status' = 0, 
other than the one with the same 'request_no' having a particular 'r_id'
"""

#AdminDeleteReq class is to interact with the requests table.
class AdminDeleteReq(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('request_no', type=int, required=True, help="request_no cannot be left blank!")
        parser.add_argument('r_id', type=int, required=True, help="r_id cannot be left blank!")
        data = parser.parse_args()
        
        qstr = f""" DELETE FROM requests
                    WHERE request_no = { data['request_no'] } AND 
                    r_id <> { data['r_id'] } AND 
                    select_status = 0; """
        
        try:
            query(qstr)
        except (pymysql.err.InternalError, pymysql.err.ProgrammingError, pymysql.err.IntegrityError) as e:
            return {
                "message" : "MySQL error: " + str(e)
            }, 500
        except Exception as e:
            return {
                "message" : "There was an error connecting to the requests table while inserting." + str(e)
            }, 500
        
        return {
            "message" : "Succesfully deleted."
        }, 200