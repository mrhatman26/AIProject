from flask import Flask, render_template, url_for, request, redirect
import sys

app = Flask(__name__)

#Home
@app.route('/')
def home():
    return render_template('home.html', page_name="About Me")

#Launch Website
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=5000)