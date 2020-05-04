from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.fields.html5 import TelField
from model import User

class RegistrationForm(FlaskForm):
    fname = StringField('First Name: ', validators=[DataRequired()])
    lname = StringField('Last Name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Length(min=6), Email(message='Enter a valid email.')])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=6, message='Enter a password at least 8 characters long.')])
    password2 = PasswordField(
        'Repeat Password: ', validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    street = StringField('Street: ', validators=[DataRequired()])
    city = StringField('City: ', validators=[DataRequired()])
    state = SelectField('State: ', choices=[("Alabama", "AL"), ("Alaska", "AK"), ("Arizona", "AZ"), ("Arkansas", "AR"), ("California", "CA"), ("Colorado", "CO"), ("Connecticut", "CT"), ("Delware", "DE"), ("Florida", "FL"), ("Georgia", "GA"), ("Hawaii", "HI"), ("Idao", "ID"), ("Illinois", "IL"), ("Indiana", "IN"), ("Iowa", "IA"), ("Kansas", "KS"), ("Kentucky", "KY"), ("Louisiana", "LA"), ("Maine", "ME"), ("Maryland", "MD"), ("Massachusetts", "MA"), ("Michigan", "MI"), ("Minnesota", "MN"), ("Mississippi", "MS"), ("Missouri", "MO"), ("mMntana", "MT"), ("Nebraska", "NE"), ("Nevada", "NV"), ("New Hampshire", "NH"), ("New Jersey", "NJ"), ("New Mexico", "NM"), ("New York", "NY"), ("North Carolina", "NC"), ("North Dakota", "ND"), ("Ohio", "OH"), ("Oklahoma", "OK"), ("Oregon", "OR"), ("Pennsylvania", "PA"), ("Rhode Island", "RI"), ("South Carolina", "SC"), ("South Dakota", "SD"), ("Tennessee", "TN"), ("Texas", "TX"), ("Utah", "UT"), ("Vermont", "VT"), ("Virginia", "VA"), ("Washington", "WA"), ("West Virginia", "WV"), ("Wisconsin", "WI"), ("Wyoming", "WY")])
    zipcode = StringField('Zipcode: ', validators=[DataRequired()])
    phonenum = TelField('Phone Number: ', validators=[DataRequired(), Length(min=10, message='Enter valid phone number')])
    politicalparty = StringField('Political Party: ', validators=[DataRequired()], id='inputPoliticalParty')
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is not None:
            raise ValidationError('Email already in use. Please use different email.')

class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email(message='Enter a valid email.')])
    password = PasswordField('Password: ', validators=[DataRequired()])
