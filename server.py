import requests
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, PollingCenter, Comment, User, Parties, PoliticalCandidates
import os
from civic_to_maps import civic_to_maps

api_key = os.environ['api_key']
print(api_key)

############################################################################################################################################################

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

    # Get form variables and add to array
    street = request.form["street"]
    city = request.form["city"]
    state = request.form["state"]
    zipcode = request.form["zipcode"]

    # Rendered variables from form into a f format string
    full_address = f"{street} {city}, {state} {zipcode}"

    # Apply full address to the civic_to_maps function
    coordinates = civic_to_maps(full_address)

    return render_template("map.html")

@app.route('/register')
def register_form():
    """Shows form for user to register account info"""

    return render_template("register.html") 

@app.route('/register', methods=['POST'])
def register_process():
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    street = request.form["street"]
    city = request.form["city"]
    state = request.form["state"]
    zipcode = request.form["zipcode"]
    party = request.form["party"]

    full_address = f"{street} {city}, {state} {zipcode}"
    
    return render_template("register.html")
    
if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")