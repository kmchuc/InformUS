import requests
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, PollingCenter, Comment, User, Parties, PoliticalCandidates
import os

api_key = os.environ['api_key']

############################################################################################################################################################

app = Flask(__name__)
app.secret_key = "SECRETKEY"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Shows the homepage"""

    return render_template("index.html")

@app.route('/map')
def address_form():
    """Show form for user to type in address or get nearby location"""

    return render_template("map.html")

@app.route('/locations.json')
def address_process():
    """Process address submitted"""

    # Get form variables and add to array
    street = request.args["street"]
    city = request.args["city"]
    state = request.args["state"]
    zipcode = request.args["zipcode"]

    # Rendered variables from form into a f format string
    full_address = f"{street} {city}, {state} {zipcode}"

    # The payload will replace parameters within the API request url
    payload = {'key' : api_key,
                'address' : full_address}

    # Assigning the GET API request to voting_json variable 
    voting_json = requests.get('https://www.googleapis.com/civicinfo/v2/voterinfo', params=payload)

    #Jsonifys the get request you make from API using input parameters from form
    voting_json = voting_json.json()

    #Assigns polling_locations to the pollingLocations value in the voting_json dictionary 
    polling_locations = voting_json['pollingLocations']

    # Starting new list to put the addresses of the polling locations from json dictionary
    locationList = []

    # Created a for loop to go through the json dictionary that selects the address line and city to make sure the latitutde and longitude are specific enough
    for line in polling_locations:
        geocode_json = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params={'key' : api_key, 
            'address' : f"{line['address']['line1']}, {line['address']['city']}"})
        locationList.append({'locationName': line['address']['locationName'],
                            'hours': line['pollingHours'],
                            'latlng': geocode_json.json()['results'][0]['geometry']['location']})

    return jsonify(locationList)

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    """Shows form that allows user to login and gain access to comment feature"""

    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)

        flask.flash('Logged in successfully')

        next = flask.request.args.get('next')

        if not is_safe(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return render_template("login.html")

@app.route('/register')
def register_form():
    """Shows form for user to register account info"""

    return render_template("register.html") 

# @app.route('/register', methods=['POST'])
# def register_process():
#     """Process registration form to database"""

#     fname = request.form["fname"]
#     lname = request.form["lname"]
#     email = request.form["email"]
#     street = request.form["street"]
#     city = request.form["city"]
#     state = request.form["state"]
#     zipcode = request.form["zipcode"]
#     party = request.form["party"]

#     full_address = f"{street} {city}, {state} {zipcode}"

#     user_request = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params={'key' : api_key, 
#             'address' : full_address})
    
#     user_request = user_request.json()

#     lat = user_request['results'][0]['geometry']['location']['lat']
#     lng = user_request['results'][0]['geometry']['location']['lng']

#     new_user = User(fname=fname, lname=lname, email=email,                password=password,lat=lat, lng=lng)

#     db.session.add(new_user)
#     db.session.commit()

#     flash(f"User {email} added.")
#     return redirect(f"/map/")
    
if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")