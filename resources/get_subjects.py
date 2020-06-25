from flask_restful import Resource, reqparse
from db import query
import base64
import pymysql

"""
Using the resource in this module, admin can insert an image with select_status = 1.
The admin has to send just the request_no and the image.
"""

#GetSubjects class is for the users
class GetSubjects(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('branch_name', type=str, help="branch_name cannot be left blank!")
        parser.add_argument('sem_no', type=int, help="sem_no cannot be left blank!")
        parser.add_argument('exam_type', type=str, help="exam_type cannot be left blank!")
        parser.add_argument('subtype', type=str, help="subtype cannot be left blank!")
        data = parser.parse_args()
        #create query string
        qstr = f""" 
        select DISTINCT subject_name
        from timetable t 
        inner join details d on (t.d_id = d.d_id)
        inner join subject s on (t.s_code = s.s_code)
        inner join branch b on (b.b_id = t.b_id)
        WHERE branch_name = "{ data['branch_name'] }" AND 
        sem_no = { data['sem_no'] } AND 
        exam_type = "{ data['exam_type'] }" AND 
        subtype = "{ data['subtype'] }";
        """
        try:
            return query(qstr)
        except Exception as e:
            return {
                "message" : "There was an error connecting to the database while retrieving." + str(e)
            }, 500
