import requests
from jinja2 import StrictUndefined
from flask import Flask, g, render_template, redirect, request, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, PollingCenter, Comment, User, Parties, PoliticalCandidates
import os

api_key = os.environ['api_key']

############################################################################################################################################################

app = Flask(__name__)
app.secret_key = "SECRETKEY"
app.jinja_env.undefined = StrictUndefined

# @app.before_request
# def before_request():
#     g.user = None

#     if 'user_id' in session:
#         user = User.query.get(session['user_id'])
#         g.user = user

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Process registration form to database"""
    
    if request.method == 'POST':
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        password = request.form["password"]
        street = request.form["street"]
        city = request.form["city"]
        state = request.form["state"]
        zipcode = request.form["zipcode"]
        party = request.form["politicalparty"]

        address = f"{street} {city}, {state} {zipcode}"

        user_request = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params={'key' : api_key, 
                'address' : address})
        
        user_request = user_request.json()

        lat = user_request['results'][0]['geometry']['location']['lat']
        lng = user_request['results'][0]['geometry']['location']['lng']

        user_party = Parties.query.filter_by(political_party=party).first()

        party_id = user_party.party_id

        new_user = User(address=address, fname=fname, lname=lname, email=email, password=password,lat=lat, lng=lng, party_id=party_id)

        db.session.add(new_user)
        db.session.commit()

        flash(f"User {email} added.")
        return redirect(url_for("home"))

    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    """Process login"""

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")
    
    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")
    
    session['user_id'] = user.user_id

    return redirect('/home')

@app.route('/home')
def home():

    # if not g.user:
    #     return redirect(url_for('login'))

    return render_template('home.html')

@app.route('/homesetup.json')
def setup():

    # for user's session
    if session.get(['user_id']):
        user = User.query.get(session['user_id'])
        print(user)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        address = user.address
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(address)
        # query for user's address and run it through google civic api

        payload = {'key' : api_key,
                    'address' : address}

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
    # get that sent through google geolocation 
    # have markers show on map
    

# @app.route('/logout')
# def logout():
#     del session["user_id"]
#     flash("You have logged out successfully!")
#     return redirect('/')

##############################################################
if __name__ == "__main__":
    app.debug = True

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")