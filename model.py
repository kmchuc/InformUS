from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "SECRETKEY"

db = SQLAlchemy()

#################################################################################

#Defining each table through classes 

class PollingCenter(db.Model):
    """Table containing polling center's information"""

    __tablename__ = "pollingcenters"

    polling_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    address = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Integer, nullable=False)
    lng = db.Column(db.Integer, nullable=False)
    hours_of_operation = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Human readable representation of data from PollingCenter table"""

        return f"""<Polling Center polling_id={self.polling_id} 
                                address={self.address} 
                                hours_of_operation={self.hours_of_operation}>"""

class Comment(db.Model):
    """Table containing User's comments for each Polling Center"""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    polling_id = db.Column(db.Integer, db.ForeignKey('pollingcenters.polling_id'), nullable=False)
    comment = db.Column(db.String(140), nullable=False)

    #Defining relationship between Comment and Polling Center tables
    polling_center = db.relationship("PollingCenter",
                                    backref=db.backref("comments", order_by=comment_id))

    #Defining relationship between Comment and User table
    user = db.relationship("User",
                            backref=db.backref("comments", order_by=comment_id))

    def __repr__(self):
        """Human readable representation of data from Comments table"""

        return f"""<Comment comment_id={self.comment_id} 
                            user_id={self.user_id} 
                            polling_id={self.polling_id}>"""

class User(db.Model):
    """Table containing User's profile information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Integer, nullable=False)
    lng = db.Column(db.Integer, nullable=False)

    #Defining relationship between User and Comment table
    comment = db.relationship("Comment",
                            backref=db.backref("users", order_by=user_id))
    
    #Defining relationship between User and Parties table
    parties = db.relationship("Parties",
                            backref=db.backref("users", order_by=user_id))

    def __repr__(self):
        return f"""<User user_id={self.user_id} party_id={self.party_id}>"""

class Parties(db.Model):
    """Table containing each political party"""

    __tablename__ = "parties"

    party_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    
    political_party = db.Column(db.String(100), nullable=False)

    #Defining relationship between Parties and Political Candidates tables
    candidates = db.relationship("PoliticalCandidates",
                                backref=db.backref("parties", order_by=party_id))

    def __repr__(self):
        return f"<Parties party_id={self.party_id} political_party={self.political_party}>"

class PoliticalCandidates(db.Model):
    """Table containing each political candidates information"""

    __tablename__ = "politicalcandidates"

    candidate_id = db.Column(db.Integer,
                            primary_key=True, 
                            autoincrement=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.party_id'), nullable=False)
    candidate_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(400), nullable=False)

    def __repr__(self):
        """Return human-readable representation of Political Candidates Table"""
        return f"<Political Candidates party_id={self.party_id} candidate_name={self.candidate_name}>"   

##############################################################################
#Helper Functions

def connect_to_db(app):
    """Connects the database to our Flask app"""

    #Configures app to use our database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///votings"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # from server import app
    connect_to_db(app)
