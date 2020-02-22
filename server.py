import requests
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, PollingCenter, Comment, User, Parties, PoliticalCandidates
import os

api_key = os.environ['api_key']
print(api_key)

#####################################################################################################################################################################################

app = Flask(__name__)
app.secret_key = "SECRETKEY"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Shows the homepage"""

    return render_template("index.html")

@app.route('/map', methods=['GET'])
def address_form():
    """Show form for user to type in address or get nearby location"""

    return render_template("map.html")

@app.route('/map', methods=['POST'])
def address_process():
    """Process address submitted"""

    return render_template("map.html")

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")