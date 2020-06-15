from flask import Flask
from flask_restful import Api

app = Flask(__name__)
#initialize api
api = Api(app)


if __name__ == '__main__':
    app.run(debug=True)
