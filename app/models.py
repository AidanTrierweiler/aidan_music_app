from datetime import datetime
from app import db


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(400), index=True)
    age = db.Column(db.String(64))
    artisttoevents = db.relationship('ArtisttoEvent', backref='artist', lazy='dynamic')


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    date = db.Column(db.String(64))
    city = db.Column(db.String(64))
    event_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    artisttoevents = db.relationship('ArtisttoEvent', backref='event', lazy='dynamic')


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    city = db.Column(db.String(64))
    size = db.Column(db.Integer)
    events = db.relationship('Event', backref='event', lazy='dynamic')


class ArtisttoEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)




