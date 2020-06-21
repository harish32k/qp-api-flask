from flask import Flask
from flask_restful import Api

#import resources
from resources.qp_request import QpRequest
from resources.admin_qp_request import AdminQpRequest
from resources.admin_timetable import AdminTimeTable
from resources.admin_false_select import AdminFalseSelect
from resources.admin_reqno_details import AdminReqNoDetails 
from resources.admin_delete_req import AdminDeleteReq

app = Flask(__name__)

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

#a route to test if the flask app is working.
@app.route('/')
def home():
    return("<h1 style='font-family: sans-serif;'>This is an API to interact with the imgdat table</h1>")

if __name__ == '__main__':
    app.run(debug=True)
