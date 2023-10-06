from flask import render_template, redirect, url_for, flash
from app.models import Artist, Event, Venue
from app import app, db
from app.forms import NewArtistForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/artist')
def artist():
    artist_list = ["Jack Johnson", "Caamp", "Mt. Joy", "Dayglow"]
    return render_template("artist.html", title="Artist", artist_list=artist_list)


@app.route('/caamp')
def artist_page():
    return render_template("caamp.html", title="Caamp", )


@app.route('/new_artist', methods=['GET', 'POST'])
def new_artist():
    form = NewArtistForm()
    if form.validate_on_submit():
        flash('New artist has been created'.format(
            form.artist_name.data, form.hometown.data, form.Description.data))
        return render_template('new_artist.html', title='New Artist', form=form, name=form.artist_name.data,
                               description=form.Description.data, hometown=form.hometown.data)
    return render_template('new_artist.html', title='New Artist', form=form, name=form.artist_name.data,
                           description=form.Description.data, hometown=form.hometown.data)


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    a1 = Artist(name="Caamp")
    a2 = Artist(name="Lil Uzi")
    a3 = Artist(name="Noah Kahan")
    a4 = Artist(name="Jack Johnson")
    a5 = Artist(name="Mt. Joy")
    db.session.add_all([a1, a2, a3, a4, a5])
    db.session.commit()

    e1 = Event(name="Ozzfest", date="12/4/2023")
    e2 = Event(name="Knotfest", date="12/10/2023")
    e3 = Event(name="Rolling loud", date="12/25/2023")
    e4 = Event(name="Coachella", date="1/4/2024")
    e5 = Event(name="Extravaganza", date="1/10/2024")
    e6 = Event(name="Bayfest", date="2/4/2024")
    e7 = Event(name="Warped Tour", date="4/5/2024")
    db.session.add_all([e1, e2, e3, e4, e5, e6, e7])
    db.session.commit()

    v1 = Venue(name="partyplace", location="New York")
    v2 = Venue(name="jazzy Joy", location="Memphis")
    v3 = Venue(name="Cool Venue", location="Boston")
    db.session.add_all([v1, v2, v3])
    db.session.commit()

    return render_template('base.html', title='Home')
