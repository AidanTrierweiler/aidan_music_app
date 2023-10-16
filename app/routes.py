from flask import render_template, redirect, url_for, flash, current_app, request
from app.models import Artist, Event, Venue, ArtistToEvent
from app import app, db
from app.forms import NewArtistForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/artists')
def artists():
    artist_list = Artist.query.all()
    return render_template("artist_list.html", artist_list=artist_list)


@app.route('/artist/<name>')
def artist_name(name):
    artist = Artist.query.filter_by(name=name).first()

    if artist:
        return render_template("artist.html", artist=artist)
    else:
        flash("Artist '{name}' not found.", 'warning')
        return redirect(url_for('index'))


@app.route('/new_artist', methods=['GET', 'POST'])
def new_artist():
    form = NewArtistForm()

    if form.validate_on_submit():
        artist_name = form.artist_name.data
        artist_description = form.Description.data
        artist_hometown = form.hometown.data

        existing_artist = Artist.query.filter_by(name=artist_name).first()

        if existing_artist:
            flash(f"Artist '{artist_name}' already exists in the database.")
        else:
            new_artist = Artist(name=artist_name, description=artist_description, hometown=artist_hometown)
            db.session.add(new_artist)
            db.session.commit()
            flash(f"Artist '{artist_name}' has been created.")

        return redirect(url_for('artists'))

    return render_template('new_artist.html', form=form)


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    a1 = Artist(name="Caamp", hometown="Columbus Ohio", description="He loves playing folk music")
    a2 = Artist(name="Lil Uzi", hometown="Philly", description="Rapper that makes good music")
    a3 = Artist(name="Noah Kahan", hometown="Stafford Vermont", description="Makes good folk music")
    a4 = Artist(name="Jack Johnson", hometown="Hawaii", description="Makes the best music of all time. Curious George!")
    a5 = Artist(name="Mt. Joy", hometown="Philly", description="Makes soothing music")
    db.session.add_all([a1, a2, a3, a4, a5])
    db.session.commit()

    v1 = Venue(name="partyplace", location="New York")
    v2 = Venue(name="jazzy Joy", location="Memphis")
    v3 = Venue(name="Cool Venue", location="Boston")
    db.session.add_all([v1, v2, v3])
    db.session.commit()

    e1 = Event(name="Ozzfest", date="12/4/2023", venue=v2)
    e2 = Event(name="Knotfest", date="12/10/2023", venue=v1)
    e3 = Event(name="Rolling loud", date="12/25/2023", venue=v2)
    e4 = Event(name="Coachella", date="1/4/2024", venue=v3)
    e5 = Event(name="Extravaganza", date="1/10/2024", venue=v1)
    e6 = Event(name="Bayfest", date="2/4/2024", venue=v1)
    e7 = Event(name="Warped Tour", date="4/5/2024", venue=v3)
    db.session.add_all([e1, e2, e3, e4, e5, e6, e7])
    db.session.commit()

    a2es_list = [
        ArtistToEvent(artist=a1, event=e1),
        ArtistToEvent(artist=a3, event=e1),
        ArtistToEvent(artist=a5, event=e1),

        ArtistToEvent(artist=a2, event=e2),
        ArtistToEvent(artist=a5, event=e2),
        ArtistToEvent(artist=a4, event=e2),

        ArtistToEvent(artist=a3, event=e3),
        ArtistToEvent(artist=a5, event=e3),
        ArtistToEvent(artist=a1, event=e3),

        ArtistToEvent(artist=a2, event=e4),
        ArtistToEvent(artist=a4, event=e4),

        ArtistToEvent(artist=a2, event=e5),
        ArtistToEvent(artist=a5, event=e5),
        ArtistToEvent(artist=a4, event=e5),

        ArtistToEvent(artist=a1, event=e6),
        ArtistToEvent(artist=a2, event=e6),
        ArtistToEvent(artist=a3, event=e6),

        ArtistToEvent(artist=a2, event=e7)]

    db.session.add_all(a2es_list)
    db.session.commit()

    return render_template('index.html', title='Home')
