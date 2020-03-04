import requests
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, PollingCenter, Comment, User, Parties, PoliticalCandidates
from flask_login import login_user, login_required, logout_user
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

@app.route('/register', methods=['GET'])
def register_form():
    """Shows form for user to register account info"""

    return render_template("register.html") 

@app.route('/register', methods=['GET', 'POST'])
def register_process():
    """Process registration form to database"""

    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]
    street = request.form["street"]
    city = request.form["city"]
    state = request.form["state"]
    zipcode = request.form["zipcode"]
    party = request.form["party"]

    address = f"{street} {city}, {state} {zipcode}"

    user_request = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params={'key' : api_key, 
            'address' : address})
    
    user_request = user_request.json()

    lat = user_request['results'][0]['geometry']['location']['lat']
    lng = user_request['results'][0]['geometry']['location']['lng']

    new_user = User(address=address, fname=fname, lname=lname, email=email,  password=password, lat=lat, lng=lng)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {email} added.")
    return redirect(f"/home")

@app.route('/login')
def login_form():
    """Shows login form. """

    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_process():
    """Process login"""

    # Get form variables 
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Couldn't find existing email and password combination, please type email/password again")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password. Please try again.")
        return redirect('/login')
    
    session["user_id"] = user.user_id

    flash("Login successfully!")
    return redirect('/home')

@app.route('/home')
@login_required
def home():

    return('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    del session["user_id"]
    flash("You have logged out successfully!")
    return redirect('/')

if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")