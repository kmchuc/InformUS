from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from model import User

class RegistrationForm(FlaskForm):
    fname = StringField('First Name: ', validators=[DataRequired()])
    lname = StringField('Last Name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Length(min=6), Email(message='Enter a valid email.')])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        'Repeat Password: ', validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    street = StringField('Street: ', validators=[DataRequired()])
    city = StringField('City: ', validators=[DataRequired()])
    state = SelectField('State: ', choices=[("alabama", "AL"), ("alaska", "AK"), ("arizona", "AZ"), ("arkansas", "AR"), ("california", "CA"), ("colorado", "CO"), ("connecticut", "CT"), ("delaware", "DE"), ("florida", "FL"), ("georgia", "GA"), ("hawaii", "HI"), ("idaho", "ID"), ("illinois", "IL"), ("indiana", "IN"), ("iowa", "IA"), ("kansas", "KS"), ("kentucky", "KY"), ("louisiana", "LA"), ("maine", "ME"), ("maryland", "MD"), ("massachusetts", "MA"), ("michigan", "MI"), ("minnesota", "MN"), ("mississippi", "MS"), ("missouri", "MO"), ("montana", "MT"), ("nebraska", "NE"), ("nevada", "NV"), ("newhampshire", "NH"), ("newjersey", "NJ"), ("newmexico", "NM"), ("newyork", "NY"), ("northcarolina", "NC"), ("northdakota", "ND"), ("ohio", "OH"), ("oklahoma", "OK"), ("oregon", "OR"), ("pennsylvania", "PA"), ("rhodeisland", "RI"), ("southcarolina", "SC"), ("southdakota", "SD"), ("tennessee", "TN"), ("texas", "TX"), ("utah", "UT"), ("vermont", "VT"), ("virginia", "VA"), ("washington", "WA"), ("westvirginia", "WV"), ("wisconsin", "WI"), ("wyoming", "WY")])
    zipcode = StringField('Zipcode: ', validators=[DataRequired()])
    politicalparty = StringField('Political Party: ', validators=[DataRequired()], id='inputPoliticalParty')
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is not None:
            raise ValidationError('Email already in use. Please use different email.')

class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email(message='Enter a valid email.')])
    password = PasswordField('Password: ', validators=[DataRequired()])
    # submit = SubmitField('Log In')
