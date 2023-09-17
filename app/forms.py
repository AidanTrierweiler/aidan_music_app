from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewArtistForm(FlaskForm):
    artist_name = StringField('Artist Name', validators=[DataRequired()])
    hometown = StringField('Hometown')
    Description = StringField('Description')
    submit = SubmitField('Create New Artist')
