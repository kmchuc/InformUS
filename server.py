import requests
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, PollingCenter, Comment, User, Parties, PoliticalCandidates
import os
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from forms import LoginForm, RegistrationForm

api_key = os.environ['api_key']

############################################################################################################################################################

app = Flask(__name__)
app.secret_key = "SECRETKEY"
login = LoginManager(app)
login.login_view = 'login'
app.jinja_env.undefined = StrictUndefined

@login.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

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


    #Rendered variables from form into a f format string
    full_address = f"{street} {city}, {state} {zipcode}"

    electionId = "2000"

    # The payload will replace parameters within the API request url
    payload = {'key': api_key,
                'electionId': electionId, 
                'address': full_address}

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

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        password = form.password.data
        street = form.street.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        politicalparty = form.politicalparty.data

        address = f"{street} {city}, {state} {zipcode}"

        user_request = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params={'key': api_key, 
                                'address': address})
        
        user_request = user_request.json()

        lat = user_request['results'][0]['geometry']['location']['lat']
        lng = user_request['results'][0]['geometry']['location']['lng']

        party = Parties.query.filter_by(political_party=politicalparty).first()

        print(party)

        party = party.party_id

        user = User(fname=fname, lname=lname, email=email, password=password, address=address, lat=lat, lng=lng, party_id=party)

        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Process login"""

    if current_user.is_authenticated:
        return redirect('/home')
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()

            if user is None or not form.password.data:
                flash('Invalid username or password')
                return redirect('/login')
            
            login_user(user)
            return redirect('/home')

        flash('Invalid username/password combination. Please try again.')
    return render_template('login.html', form=form)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():

    if request.method == 'POST':
        comment = request.form['comment']
        user = User.query.get(session['id'])
        lat = request.form['lat']
        lng = request.form['lng']
        hours = request.form['hours']

        pollingcenter = PollingCenter.query.filter_by(lat=lat, lng=lng).first()
        if not pollingcenter:
            pollingcenter = PollingCenter(lat=lat, lng=lng, hours_of_operation=hours)
            db.session.add(pollingcenter)
            db.session.commit()

        new_comment = Comment(comment=comment, polling_id=pollingcenter.polling_id, user_id=user.id)
        db.session.add(new_comment)
        db.session.commit()

        flash("Comment submitted")
    return render_template('home.html')

@app.route('/homesetup.json')
def setup():

    user = User.query.get(current_user.get_id())
    # user = User.query.get(session['id'])

    address = user.address
    electionId = "2000"

    # The payload will replace parameters within the API request url
    payload = {'key' : api_key,
                'electionId' : electionId, 
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
            'address': f"{line['address']['line1']}, {line['address']['city']}"})
        locationList.append({'locationName': line['address']['locationName'],
                            'hours': line['pollingHours'],
                            'latlng': geocode_json.json()['results'][0]['geometry']['location']})

    return jsonify(locationList)

@app.route('/comments.json')
def comments():
    """route for getting comments for polling locations"""

    lat = request.args['lat']
    lng = request.args['lng']

    pollingcenter = PollingCenter.query.filter_by(lat=lat, lng=lng).first()

    comments = []

    if pollingcenter:
        for comment in pollingcenter.comments:
            comments.append({
                'comment_id': comment.comment_id,
                'user_id': comment.user_id,
                'polling_id': comment.polling_id,
                'comment': comment.comment
            })
        return jsonify(comments)
        
    else:
        comments.append({
                'comment_id': None,
                'user_id': None,
                'polling_id': None,
                'comment': "Location has no comments"
            })
    return jsonify(comments)



@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect('/')

##############################################################

if __name__ == "__main__":
    app.debug = True

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")