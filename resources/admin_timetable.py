from flask_restful import Resource, reqparse
from db import query
import pymysql

#AdminTimeTable class is to interact with the Timetable table.
class AdminTimeTable(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('request_no', type=int, help="request_no cannot be left blank!")
        data = parser.parse_args()
        #create query string
        qstr = f""" SELECT * FROM timetable where request_no = { data['request_no'] };"""
        try:
            return query(qstr)
        except:
            return {
                "message" : "There was an error connecting to the timetable table while retrieving."
            }, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('b_id', type=int, required=True, help="b_id cannot be left blank!")
        parser.add_argument('d_id', type=int, required=True, help="d_id cannot be left blank!")
        parser.add_argument('s_code', type=str, required=True, help="s_code cannot be left blank!")
        parser.add_argument('exam_type', type=str, required=True, help="exam_type cannot be left blank!")
        parser.add_argument('subtype', type=str, required=True, help="subtype cannot be left blank!")
        data = parser.parse_args()

        qstr = f""" INSERT INTO timetable (b_id,d_id,s_code,exam_type,subtype)
                    values ({ data['b_id'] }, 
                    { data['d_id'] }, 
                    "{ data['s_code'] }", 
                    "{ data['exam_type'] }", 
                    "{ data['subtype'] }"); """
        
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
            "message" : "Succesfully inserted"
        }, 200