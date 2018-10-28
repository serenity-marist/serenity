
from flask import Flask, render_template, session
from flask import request
from flask import render_template, redirect, url_for, request, jsonify
import settings
import json
import DegreeWorksTotalScrape


app = Flask(__name__)
app.secret_key = 'any random string'
@app.route('/')
def home():
  isLogged = False
  if 'sessionId' in session:
    isLogged = True
    settings.email = session['sessionId']
    settings.password = session['password']
  return render_template('landing.html', isLogged = isLogged)

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

@app.route('/logout' ,methods=['GET'])
def logout():
  session.pop('sessionId', None)
  DegreeWorksTotalScrape.logout()
  return "OK"


@app.route("/login", methods=['POST'])
def login():
   settings.email = request.form['email']
   settings.password = request.form['password']
   if settings.email == "" or settings.password == "":
     settings.email =  session['sessionId']
     settings.password = session['password']
   session['sessionId'] = settings.email
   session['password'] = settings.password
   # import Login
   DegreeWorksTotalScrape.login()
   return jsonify(settings.email)


if __name__ == '__main__':
    app.run(debug=True)
