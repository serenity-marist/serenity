from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
 return render_template('home.html')

@app.route('/webScraperTool')
def webScraperTool():
 import DegreeWorksStudentView
 return render_template('webScraperTool.html')


if __name__ == '__main__':
    app.run(debug=True)
