# from datetime import datetime
from app import db


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    description = db.Column(db.String(300))
    hometown = db.Column(db.String(128))
    a2es = db.relationship('ArtistToEvent', backref='artist', lazy='dynamic')

    def __repr__(self):
        return '<Artist {} - {}>'.format(self.id, self.name)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    date = db.Column(db.String(64), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    a2es = db.relationship('ArtistToEvent', backref='event', lazy='dynamic')

    def __repr__(self):
        return '<Event {} - {}>'.format(self.id, self.name)


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    location = db.Column(db.String(64), nullable=False)
    events = db.relationship('Event', backref='venue', lazy='dynamic')

    def __repr__(self):
        return '<venue {} - {}>'.format(self.id, self.name)


class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)



#
# a1 = Artist.query.find(0)
#
# a1.a2es[0].event.venue.name