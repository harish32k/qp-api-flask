from flask_restful import Resource, reqparse
from db import query
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import safe_str_cmp
import pymysql

#UserRegister resource is defined for the user-register endpoint
#UserRegister class is for the admin to interact with the user table.
class UserRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uname', type=str, required=True, help="uname cannot be left blank!")
        parser.add_argument('password', type=str, required=True, help="password cannot be left blank!")
        parser.add_argument('rno', type=str, required=True, help="rno cannot be left blank!")
        data = parser.parse_args()
        
        try:
            qstr = f""" 
            SELECT uname from user where uname = "{ data['uname'] }";
            """
            usersWithUname = query(qstr, return_json=False)
            
            qstr = f""" 
            SELECT uname from user where rno = "{ data['rno'] }";
            """
            usersWithRoll = query(qstr, return_json=False)
        
        except Exception as e:
            return {
                "message" : "There was an error connecting to the User table while checking for an existing user."  + str(e)
            }, 500

        if len(usersWithUname)>0:
            return {
                "message" : "A user with the same username exists."
            }, 400

        if len(usersWithRoll)>0:
            return {
                "message" : "A user with the same roll number exists."
            }, 400


        qstr = f""" INSERT INTO user values("{ data['uname'] }", "{ data['password'] }", "{ data['rno'] }"); """

        try:
            query(qstr)
        except (pymysql.err.InternalError, pymysql.err.ProgrammingError, pymysql.err.IntegrityError) as e:
            return {
                "message" : "MySQL error: " + str(e)
            }, 500
        except Exception as e:
            return {
                "message" : "There was an error connecting to the User table while inserting." + str(e)
            }, 500
        
        return {
            "message" : "Succesfully registered(inserted)"
        }, 200