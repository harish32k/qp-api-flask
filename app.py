from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

#import resources
from resources.qp_request import QpRequest
from resources.admin_qp_request import AdminQpRequest
from resources.admin_timetable import AdminTimeTable
from resources.admin_false_select import AdminFalseSelect
from resources.admin_reqno_details import AdminReqNoDetails 
from resources.admin_delete_req import AdminDeleteReq
#user part
from resources.get_subjects import GetSubjects
from resources.get_yearwise import GetYearwise

#authentication
from resources.admin_login import AdminLogin

app = Flask(__name__)

#set config for jwt
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_SECRET_KEY'] = 'qp-cbit'

#initialize api
api = Api(app)

api.add_resource(QpRequest,'/qpreq') #for user to upload paper
api.add_resource(AdminQpRequest,'/admin-qpreq')#for admin to upload paper with an optional feature to set select_status=1
api.add_resource(AdminTimeTable,'/admin-timetable') #for admin to upload timetable
api.add_resource(AdminFalseSelect,'/admin-false-select') #for admin to retrieve papers with false or 0 select_status
api.add_resource(AdminReqNoDetails,'/admin-reqno-details') #for admin to get details for a particular request_no
# the below one is for admin to delete question papers with select_status=0 having a particular request_no
# other than the ones with same request_number and a particular r_id  
api.add_resource(AdminDeleteReq,'/admin-delete-req')

#user endpoints
api.add_resource(GetSubjects, '/get-subjects')
api.add_resource(GetYearwise, '/get-yearwise')

#authentication endpoints
api.add_resource(AdminLogin, '/admin-login')

jwt=JWTManager(app)

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'authorization_required',
        "description": "Request does not contain an access token."
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'message': 'Signature verification failed.'
    }), 401

#a route to test if the flask app is working.
@app.route('/')
def home():
    return("<h1 style='font-family: sans-serif;'>This is an API to interact with the imgdat table</h1>")

if __name__ == '__main__':
    app.run(debug=True)
