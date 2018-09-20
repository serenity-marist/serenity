from flask import Flask
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)


def index(req):
    postData = req.form
    json = str(postData['param'].value) 
