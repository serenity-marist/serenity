from flask import Flask, render_template
from flask import request
from flask import render_template, redirect, url_for, request, jsonify
import settings
import json


app = Flask(__name__)

@app.route('/')
def home():
 return render_template('landing.html')

# @app.route('/webScraperTool.html')
# def webScraperTool():
#  import DegreeWorksStudentView
#  return render_template('webScraperTool.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/test', methods =['GET','POST'])
def test():
    return "data"
    # return _test(request.form["test"])

# @app.route("toolPage", methods = ['POST'])
#  def toolPage():


@app.route('/webScraperTool', methods =['POST'])
def webScraperTool():
 settings.email = request.form['email'];
 settings.password = request.form['password'];
 import DegreeWorksTotalScrape
 print(settings.jsonObject)
 return jsonify(settings.jsonObject)

if __name__ == '__main__':
    app.run(debug=True)
