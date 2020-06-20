from flask_restful import Resource, reqparse
from db import query
import base64

def convertToBlob(value):
    return base64.b64decode(value.encode('utf-8'))

#Imgdat class is to interact with the imgdat table.
class Imgdat(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, help="id cannot be left blank!")
        data = parser.parse_args()
        #create query string
        qstr = f""" SELECT * FROM imgdat where id = { data['id'] }"""
        try:
            return query(qstr)
        except:
            return {
                "message" : "There was an error connecting to the imgdat table while retrieving."
            }, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="id cannot be left blank!")
        parser.add_argument('image', type=str, required=True, help="id cannot be left blank!")
        data = parser.parse_args()
        
        vals_tuple = (data['id'], convertToBlob(data['image']))
        qstr = f""" INSERT INTO imgdat
                    values (%s, %s); """
        
        try:
            query(qstr,args_tuple=vals_tuple)
        except:
            return {
                "message" : "There was an error connecting to the imgdat table while inserting."
            }, 500
        
        return {
            "message" : "Succesfully inserted"
        }, 200