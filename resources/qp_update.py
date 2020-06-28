from flask_restful import Resource, reqparse
from db import connectToHost
import base64
import pymysql

def convertToBlob(value):
    return base64.b64decode(value.encode('utf-8'))

# this resource is used by the user to update an image uploaded. 
class QpUpdate(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('request_no', type=int, required=True, help="request_no cannot be left blank!")
        parser.add_argument('image', type=str, required=True, help="image cannot be left blank!")
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

            qstr = f""" UPDATE requests
                    SET image = (%s)
                    WHERE request_no = '%s' AND  
                    r_id = '%s';"""


            #creating a tuple of values to be inserted because a formatted string is used
            #here its useful to avoid SQL syntax errors while inserting BLOB value into table
            vals_tuple = (convertToBlob(data['image']), data['request_no'], insert_rid)
            #convertToBlob is used to convert base64 string to BLOB data
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