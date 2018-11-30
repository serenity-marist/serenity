from flask import Flask, render_template, session
from flask import request
from flask import render_template, redirect, url_for, request, jsonify
import os
import settings
import json
import DegreeWorksTotalScrape


app = Flask(__name__)
app.secret_key = 'any random string'
@app.route('/')
def home():
  # DegreeWorksTotalScrape.init()
  # isLogged = False
  # if 'email' in session:
  isLogged = False
  if 'email' in session:
    isLogged = True
  return render_template('landing.html', isLogged = isLogged)

@app.route('/dashboard')
def dashboard():
 return render_template('dashboard.html')

@app.route('/webScraperTool', methods =['POST'])
def webScraperTool():
 jsonObjects = DegreeWorksTotalScrape.runScrape()
 return jsonify(jsonObjects)

@app.route('/logout' ,methods=['GET'])
def logout():
  isLogged = False
  session.pop('email', None)
  session.pop('password', None)
  DegreeWorksTotalScrape.logout()
  return redirect("/")


@app.route('/destroy', methods=['GET'])
def destroy():
  DegreeWorksTotalScrape.destroy()
  return jsonify("ok")

@app.route("/login", methods=['POST'])
def login():
  # When a user initially logs in, we get the user data from request form.
  # The data then gets saved.
   if not request.form['email'] == "":
     session['email'] = request.form['email']
     session['password'] = request.form['password']
   result = DegreeWorksTotalScrape.login(session['email'],session['password'])
   # As soon as we can login with their info, delete the password
   # session.pop('password', None)
   return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0', threaded=True)
