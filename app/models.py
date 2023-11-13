from datetime import datetime
from hashlib import md5
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Model for an artist
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Artist table
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # Artist's name
    description = db.Column(db.String(300))  # Artist's description
    hometown = db.Column(db.String(128))  # Artist's hometown
    a2es = db.relationship('ArtistToEvent', backref='artist', lazy='dynamic')  # Relationship to ArtistToEvent

    def __repr__(self):
        return '<Artist {} - {}>'.format(self.id, self.name)

# Model for an event
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Event table
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # Event's name
    date = db.Column(db.DateTime, nullable=False)  # Date and time of the event
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))  # Foreign key to the Venue table
    a2es = db.relationship('ArtistToEvent', backref='event', lazy='dynamic')  # Relationship to ArtistToEvent

    def __repr__(self):
        return '<Event {} - {}>'.format(self.id, self.name)

# Model for a venue
class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Venue table
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # Venue's name
    location = db.Column(db.String(64), nullable=False)  # Venue's location
    events = db.relationship('Event', backref='venue', lazy='dynamic')  # Relationship to Event

    def __repr__(self):
        return '<Venue {} - {}>'.format(self.id, self.name)

# Association table for many-to-many relationship between Artist and Event
class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the ArtistToEvent table
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)  # Foreign key to the Artist table
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)  # Foreign key to the Event table

# Model for a user
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the User table
    username = db.Column(db.String(64), index=True, unique=True)  # User's username
    email = db.Column(db.String(120), index=True, unique=True)  # User's email
    password_hash = db.Column(db.String(128))  # Hash of the user's password
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)  # Last seen timestamp

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """Sets the password hash for the user"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the given password matches the stored hash"""
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """Generates a Gravatar URL for the user's avatar"""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

# Callback function to reload the user object from the user ID stored in the session
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
