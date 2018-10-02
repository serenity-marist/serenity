from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
 return render_template('home.html')

@app.route('/webScraperTool')
def webScraperTool():
 import DegreeWorksTotalScrape
 return render_template('webScraperTool.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/test', methods =['GET','POST'])
def test():
    return "data"
    # return _test(request.form["test"])



if __name__ == '__main__':
    app.run(debug=True)
