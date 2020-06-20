from flask_restful import Resource, reqparse
from db import query
import base64

def convertToBlob(value):
    return base64.b64decode(value.encode('utf-8'))

#QpRequest class is to interact with the requests table.
class QpRequest(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('r_id', type=int, help="r_id cannot be left blank!")
        data = parser.parse_args()
        #create query string
        qstr = f""" SELECT * FROM requests where r_id = { data['r_id'] };"""
        try:
            return query(qstr)
        except:
            return {
                "message" : "There was an error connecting to the requests table while retrieving."
            }, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('request_no', type=int, required=True, help="request_no cannot be left blank!")
        parser.add_argument('image', type=str, required=True, help="image cannot be left blank!")
        data = parser.parse_args()
        
        #creating a tuple of values to be inserted because a formatted string is used
        #here its useful to avoid SQL syntax errors while inserting BLOB value into table
        vals_tuple = (data['request_no'], convertToBlob(data['image']))
        #convertToBlob is used to convert base64 string to BLOB data

        qstr = f""" INSERT INTO requests (request_no, image)
                    values (%s, %s); """
        
        try:
            query(qstr,args_tuple=vals_tuple)
        except:
            return {
                "message" : "There was an error connecting to the requests table while inserting."
            }, 500
        
        return {
            "message" : "Succesfully inserted"
        }, 200