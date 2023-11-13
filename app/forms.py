from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, SubmitField, \
    TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User

# Form for creating a new artist
class NewArtistForm(FlaskForm):
    artist_name = StringField('Artist Name', validators=[DataRequired()])  # Artist's name, required field
    hometown = StringField('Hometown')  # Artist's hometown
    Description = StringField('Description')  # Artist's description
    submit = SubmitField('Create New Artist')  # Submit button

# Form for creating a new venue
class NewVenueForm(FlaskForm):
    venue_name = StringField('Venue name', validators=[DataRequired()])  # Venue's name, required field
    venue_location = StringField('Venue location', validators=[DataRequired()])  # Venue's location, required field
    submit = SubmitField('Create New Venue')  # Submit button

# Form for creating a new event
class NewEventForm(FlaskForm):
    name = StringField('Event Name')  # Event's name
    date = DateField('Date', format='%Y-%m-%d')  # Event's date, with specified format
    venue = SelectField('Venue', coerce=int)  # Dropdown for selecting venue
    artists = SelectMultipleField('Artists', coerce=int, choices=[])  # Multi-select for choosing artists
    submit = SubmitField('Create New Event')  # Submit button

# Form for user login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Username, required field
    password = PasswordField('Password', validators=[DataRequired()])  # Password, required field
    remember_me = BooleanField('Remember Me')  # Checkbox to remember the user
    submit = SubmitField('Sign In')  # Submit button

# Form for user registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Username, required field
    email = StringField('Email', validators=[DataRequired(), Email()])  # Email, required field and must be a valid email
    password = PasswordField('Password', validators=[DataRequired()])  # Password, required field
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])  # Password confirmation, must match the password
    submit = SubmitField('Register')  # Submit button

    # Custom validator for username to ensure uniqueness
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # Custom validator for email to ensure uniqueness
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# Form for editing user profile
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Username, required field
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])  # About me section, with length restriction
    submit = SubmitField('Submit')  # Submit button
