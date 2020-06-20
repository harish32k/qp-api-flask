from flask import Flask
from flask_restful import Api
from resources.qp_request import QpRequest #to interact with requests table
from resources.admin_timetable import AdminTimeTable
from resources.admin_false_select import AdminFalseSelect

app = Flask(__name__)
#initialize api
api = Api(app)
api.add_resource(QpRequest,'/qpreq')
api.add_resource(AdminTimeTable,'/admin-timetable')
api.add_resource(AdminFalseSelect,'/admin-false-select')

@app.route('/')
def home():
    return("<h1 style='font-family: sans-serif;'>This is an API to interact with the imgdat table</h1>")

if __name__ == '__main__':
    app.run(debug=True)
