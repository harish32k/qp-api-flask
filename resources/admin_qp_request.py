from flask_restful import Resource, reqparse
from db import query
import base64
import pymysql
from flask_jwt_extended import jwt_required

def convertToBlob(value):
    return base64.b64decode(value.encode('utf-8'))

"""
Using the resource in this module, admin can insert an image with select_status = 1.
The admin has to send just the request_no and the image.
"""

#AdminQpRequest class is for the admin to interact with the requests table.
class AdminQpRequest(Resource):
    
    @jwt_required
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

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('b_id', type=int, required=True, help="b_id cannot be left blank!")
        parser.add_argument('sem_no', type=int, required=True, help="sem_no cannot be left blank!")
        parser.add_argument('exam_type', type=str, required=True, help="exam_type cannot be left blank!")
        parser.add_argument('subtype', type=str, required=True, help="request_no cannot be left blank!")
        parser.add_argument('s_code', type=str, required=True, help="s_code cannot be left blank!")
        parser.add_argument('year', type=int, required=True, help="year cannot be left blank!")
        parser.add_argument('image', type=str, required=True, help="image cannot be left blank!")
        
        #parser.add_argument('select_status', type=int, required=False, default = 0)
        
        data = parser.parse_args()
        #creating a tuple of values to be inserted because a formatted string is used
        #here its useful to avoid SQL syntax errors while inserting BLOB value into table

        # a transaction is made, so not connecting from db.py module.
        # here we execute several queries then commit.
        try:
            connection = pymysql.connect(host='localhost',
                                    user='harish',
                                    password='',
                                    db='testapi',
                                    cursorclass=pymysql.cursors.DictCursor)

            #start connection, create cursor and execute query from cursor
            connection.begin()
            cursor = connection.cursor()

            #obtain request_no from the details provided, store in req_no

            qstr = f"""
            select DISTINCT request_no
            from timetable t 
            inner join details d on (t.d_id = d.d_id)
            WHERE b_id = '{data['b_id']}' AND 
            sem_no = '{data['sem_no']}' AND 
            exam_type = '{data['exam_type']}' AND 
            subtype = '{data['subtype']}' AND 
            year = '{data['year']}' AND
            s_code = '{data['s_code']}'
            LIMIT 1;
            """

            cursor.execute(qstr)
            cursor.execute(qstr)
            result = cursor.fetchall()
            req_no = list(result[0].values())[0]
            
            # delete all the other entries in requests table 
            # with the same request_no, whether selected or not
            qstr = f"""
            delete from requests
            where request_no = {req_no};
            """
            
            cursor.execute(qstr)

            vals_tuple = (req_no, convertToBlob(data['image']), 1 ) #set select status to 1
            #convertToBlob is used to convert base64 string to BLOB data

            qstr = f""" INSERT INTO requests (request_no, image, select_status)
                        values (%s, %s, %s); """

            cursor.execute(qstr, vals_tuple)

            connection.commit() #commit the changes made
    
            #close the cursor and connection
            cursor.close()
            connection.close()
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