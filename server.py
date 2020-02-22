import requests
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, PollingCenter, Comment, User, Parties, PoliticalCandidates
import os

api_key = os.environ['api_key']
print(api_key)

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

    #Rendered variables from form into a f format string
    full_address = f"{street} {city}, {state} {zipcode}"

    payload = {'key' : api_key,
                'address' : full_address}

    voting_json = requests.get('https://www.googleapis.com/civicinfo/v2/voterinfo', params=payload)

    #Jsonifys the get request you make from API using input parameters from form
    voting_json = voting_json.json()

    #Assigns polling_locations to the pollingLocations value in the voting_json dictionary 
    polling_locations = voting_json['pollingLocations']
    
    address_list = []

    for line in address_list:
        address_list.append(line['address']['line1'])
    
    

    return render_template("map.html", full_address=full_address, address_list=address_list)

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")