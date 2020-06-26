from flask_restful import Resource, reqparse
import pymysql
import db
from flask_jwt_extended import jwt_required

#AdminTimeTable class is to interact with the Timetable table.
class AdminTimeTableUpdate(Resource):

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('request_no', type=int, required=True, help="request_no cannot be left blank!")
        parser.add_argument('b_id', type=int, required=True, help="b_id cannot be left blank!")
        parser.add_argument('s_code', type=str, required=True, help="s_code cannot be left blank!")
        parser.add_argument('exam_type', type=str, required=True, help="exam_type cannot be left blank!")
        parser.add_argument('subtype', type=str, required=True, help="subtype cannot be left blank!")
        parser.add_argument('start_at', type=str, required=True, help="start_at cannot be left blank!")
        parser.add_argument('end_at', type=str, required=True, help="end_at cannot be left blank!")
        parser.add_argument('date', type=str, required=True, help="date cannot be left blank!")
        parser.add_argument('year', type=int, required=True, help="year cannot be left blank!")
        parser.add_argument('sem_no', type=int, required=True, help="sem_no cannot be left blank!")
        data = parser.parse_args()
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

            # obtain the d_id so that if the current timings change, d_id for the row which is to
            # be updated should have d_id changed.
            qstr = f"""SELECT d_id from timetable where request_no = "{ data['request_no'] }";"""
            cursor.execute(qstr)
            result = cursor.fetchall()
            old_did = list(result[0].values())[0]
            
            # the timings sent in the request are added if not already there in the details table
            qstr = f"""INSERT INTO DETAILS (start_at, end_at, date, year, sem_no)
            SELECT * FROM 
            (SELECT "{ data['start_at'] }", 
            "{ data['end_at'] }", 
            "{ data['date'] }", 
            "{ data['year'] }", 
            "{ data['sem_no'] }") AS TEMP

            WHERE NOT EXISTS(
            SELECT d_id from details 
            where start_at = " {data['start_at']} " AND
            end_at = "{ data['end_at'] }" AND
            date = "{ data['date'] }" AND
            sem_no = "{ data['sem_no'] }"
            ) LIMIT 1 ;"""

            cursor.execute(qstr)

            # the d_id with the timings is obtained from the table comparing with the timings provided
            # in the json
            qstr = f"""
            SELECT d_id from details 
            where start_at = " {data['start_at']} " AND
            end_at = "{ data['end_at'] }" AND
            date = "{ data['date'] }" AND
            sem_no = "{ data['sem_no'] }" ;
            """
            #lets call the d_id as new_did, it could be the same d_id as before if timings aren't updated.
            cursor.execute(qstr)
            result = cursor.fetchall()
            new_did = list(result[0].values())[0]
            
            #update timetable with the fields provided
            qstr = f"""
            update timetable
            
            set d_id = "{ new_did }", 
            exam_type = "{ data['exam_type'] }", 
            subtype = "{ data['subtype'] }" , 
            s_code = "{ data['s_code'] }" , 
            b_id = { data['b_id'] }

            where request_no = "{ data['request_no'] }"; 
            """
            cursor.execute(qstr)

            # if timings are changed, then old_did and new_did will differ. 
            # so delete the old_did if no other row has old_did value in d_id column
            # of timetable table.
            if old_did != new_did:
                qstr = f""" 
                delete from details
                where d_id = "{ old_did }"
                AND NOT EXISTS (select d_id from timetable where d_id = "{ old_did }");
                """
                cursor.execute(qstr)

            
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
            "message" : "Succesfully updated."
        }, 200