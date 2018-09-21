#!/usr/bin/python3
# app.py

from flask import Flask
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)


def index():
    return("Hello World")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)