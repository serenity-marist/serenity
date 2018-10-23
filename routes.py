from flask import Flask, render_template
from flask import request
from flask import render_template, redirect, url_for, request, jsonify
import settings
import json
import DegreeWorksTotalScrape


app = Flask(__name__)

@app.route('/')
def home():
 return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
 return render_template('dashboard.html')


# return _test(request.form["test"])
# @app.route("toolPage", methods = ['POST'])
#  def toolPage():


@app.route('/webScraperTool', methods =['POST'])
def webScraperTool():
 # settings.email = request.form['email'];
 # settings.password = request.form['password'];
 # import DegreeWorksTotalScrape
 DegreeWorksTotalScrape.runScrape()
#  print(settings.jsonObjects)
 return jsonify(settings.jsonObjects)

@app.route("/login", methods=['POST'])
def login():
   settings.email = request.form['email'];
   settings.password = request.form['password'];
   # import Login
   DegreeWorksTotalScrape.login()
   return jsonify(settings.email)


if __name__ == '__main__':
    app.run(debug=True)
