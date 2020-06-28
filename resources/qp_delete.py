from flask_restful import Resource, reqparse
from db import connectToHost
import base64
import pymysql

def convertToBlob(value):
    return base64.b64decode(value.encode('utf-8'))


class QpDelete(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('request_no', type=int, required=True, help="request_no cannot be left blank!")
        parser.add_argument('uname', type=str, required=True, help="uname cannot be left blank!")
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

            qstr = f"""
            SELECT r_id FROM User.submissions WHERE 
            request_no = "{ data['request_no'] }" AND 
            uname = "{ data['uname'] }" LIMIT 1;
            """
            
            cursor.execute(qstr)
            result = cursor.fetchall()
            insert_rid = list(result[0].values())[0]    

            qstr = f""" DELETE FROM REQUESTS
                    WHERE request_no = '{ data['request_no'] }' AND  
                    r_id = '{ insert_rid }';"""


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
                "message" : "There was an error connecting to the requests table while deleting." + str(e)
            }, 500
        
        return {
            "message" : "Succesfully deleted."
        }, 200