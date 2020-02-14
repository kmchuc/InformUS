import requests
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, PollingCenter, Comment, User, Parties, PoliticalCandidates

# r = requests.get('https://www.googleapis.com/civicinfo/v2/voterinfo?address=990%20Jackson%20Street%20San%20Francisco%2C%20CA%2094133&key=AIzaSyCALOx3a43D4qa6l_2R9YJPAPF43A4NnjA')

# voting_info = r.json()

# polling_locations = voting_info['pollingLocations']

# first_result = polling_locations[0]

#####################################################################################################################################################################################
app = Flask(__name__)
app.secret_key = "SECRETKEY"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Shows the homepage"""
    return render_template("index.html")

# @app.route('/nearme', methods=['GET'])
# def address_form():
#     """Show form for user to type in address or get nearby location"""

#     return render_template("address_form.html")

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")