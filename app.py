from flask import Flask
from flask_restful import Api
from resources.imgdat import Imgdat
from resources.qp_request import QpRequest #to interact with requests table

app = Flask(__name__)
#initialize api
api = Api(app)
#api.add_resource(Imgdat,'/img')
api.add_resource(QpRequest,'/qpreq')

@app.route('/')
def home():
    return("<h1 style='font-family: sans-serif;'>This is an API to interact with the imgdat table</h1>")

if __name__ == '__main__':
    app.run(debug=True)
