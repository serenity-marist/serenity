#!/usr/bin/python3
# app.py

from flask import Flask
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    import DegreeWorksStudentView
    return 'Hello World'


def index(req):
    postData = req.form
    json = str(postData['param'].value)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
