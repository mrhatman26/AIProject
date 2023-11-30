from flask import Flask, render_template, url_for, request, redirect
from misc_functions import multi_replace
import sys

app = Flask(__name__)

#Home
@app.route('/')
def home():
    return render_template('home.html', page_name="About")

@app.route('/job_search')
def job_search():
    skills_file = open("./static/skills_file.txt", "r")
    skills_list = []
    for item in skills_file:
        item = multi_replace(item, "", "'", "\n")
        item = item.title().replace("-", " ")
        skills_list.append(item)
    skills_file.close()
    return render_template('skills.html', page="Job Search", skills=skills_list)

#Launch Website
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=5000)