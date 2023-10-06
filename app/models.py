# from datetime import datetime
from app import db


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    a2es = db.relationship('ArtistToEvent', backref='artist', lazy='dynamic')


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    date = db.Column(db.String(64), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    artists = db.relationship('Artist', backref='events', lazy='dynamic')
    a2es = db.relationship('ArtistToEvent', backref='event', lazy='dynamic')


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    location = db.Column(db.String(64), nullable=False)
    events = db.relationship('Event', backref='venue', lazy='dynamic')


class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)



#
# a1 = Artist.query.find(0)
#
# a1.a2es[0].event.venue.name