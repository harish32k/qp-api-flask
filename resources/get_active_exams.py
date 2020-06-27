from flask_restful import Resource, reqparse
from db import query
import pymysql

#GetActiveExams class is for the user to get info about the entries in active_exams
class GetActiveExams(Resource):
    
    def get(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('branch_name', type=str, help="branch_name cannot be left blank!")
        # parser.add_argument('sem_no', type=int, help="sem_no cannot be left blank!")
        # parser.add_argument('exam_type', type=str, help="exam_type cannot be left blank!")
        # parser.add_argument('subtype', type=str, help="subtype cannot be left blank!")
        # parser.add_argument('subject_name', type=str, help="subject_name cannot be left blank!")
        # data = parser.parse_args()
        #create query string
        qstr = f""" 
        SELECT * FROM active_exams;
        """
        try:
            return query(qstr)
        except Exception as e:
            return {
                "message" : "There was an error connecting to the database while retrieving." + str(e)
            }, 500
