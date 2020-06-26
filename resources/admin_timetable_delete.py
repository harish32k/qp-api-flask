from flask_restful import Resource, reqparse
import pymysql
from db import connectToHost
from flask_jwt_extended import jwt_required

#AdminTimeTable class is to interact with the Timetable table.
class AdminTimeTableDelete(Resource):

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('request_no', type=int, required=True, help="request_no cannot be left blank!")
        data = parser.parse_args()
        
        # a transaction is made, so not using query function from db module
        # we use connectToHost function from db module and commit explicitly
        # the query function from db module commits for each query which is not desirable in 
        # a transaction sequence as follows.
        # here we execute several queries then commit.
        try:
            connection = connectToHost()
            
            #start connection, create cursor and execute query from cursor
            connection.begin()
            cursor = connection.cursor()

            # obtain d_id for the provided request_no, so that we can delete 
            # an entry in details if no other rows in timetable have have the same d_id
            qstr = f"""SELECT d_id from timetable 
            where request_no = "{ data['request_no'] }";"""
            cursor.execute(qstr)
            result = cursor.fetchall()
            del_did = list(result[0].values())[0]
            
            # delete requests entries with the request_no
            qstr = f"""delete from requests
            where request_no = "{ data['request_no'] }";"""
            cursor.execute(qstr)

            # delete timetable entry with the request_no
            qstr = f"""delete from timetable
            where request_no = "{ data['request_no'] }";"""
            cursor.execute(qstr)

            # delete an entry in details if no other row in timetable table has d_id
            qstr = f"""delete from details
            where d_id = "{ del_did }"
            AND NOT EXISTS (select d_id from timetable where d_id = "{ del_did }");"""
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
            "message" : "Succesfully deleted."
        }, 200