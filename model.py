from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "SECRETKEY"

DB_URI = "postgresql:///voting"

db = SQLAlchemy()

#################################################################################

#Defining each table through classes 

class PollingCenter(db.Model):
    """Table containing polling center's information"""

    __tablename__ = "polling-centers"

    polling_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    address = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Integer, nullable=False)
    lng = db.Column(db.Integer, nullable=False)
    hours_of_operation = db.Column(db.String(50), nullable=False)
    

    def __repr__(self):
        """Human readable representation of data from PollingCenter table"""

        return f"<Polling Center polling_id={self.polling_id} address={self.address} hours_of_operation={self.hours_of_operation}"

class Comment(db.Model):
    """Table containing User's comments for each Polling Center"""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    polling_id = db.Column(db.Integer, db.ForeignKey('polling-centers.polling_id'), index=True)
    comment = db.Column(db.String(140), nullable=False)

    def __repr__(self):
        """Human readable representation of data from Comments table"""

        return f"<Comment comment_id={self.comment_id} user_id={self.user_id} polling_id={self.polling_id}"

class User(db.Model):
    """Table containing User's profile information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), index=True)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(3), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Integer, nullable=False)
    lng = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<User user_id={self.user_id} party_id={self.party_id}"

class Parties(db.Model):
    """Table containing each political party"""

    __tablename__ = "parties"

    party_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    
    political_party = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Parties party_id={self.party_id} political_party={self.political_party}"

class PoliticalCandidates(db.Model):
    """Table containing each political candidates information"""

    __tablename__ = "politicalcandidates"

    candidate_id = db.Column(db.Integer,
                            primary_key=True 
                            autoincrement=True)
    party_id = db.Column(db.Integer, nullable=False)





    


app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
db.app = app
db.init_app(app)

db.create_all()
