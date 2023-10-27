from flask import render_template, redirect, url_for, flash, current_app, request
from app.models import Artist, Event, Venue, ArtistToEvent, User
from app import app, db
from app.forms import NewArtistForm, LoginForm, RegistrationForm, EditProfileForm, NewVenueForm, NewEventForm
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse


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


@app.route('/new_venue', methods=['GET', 'POST'])
def new_venue():
    form = NewVenueForm()

    if form.validate_on_submit():
        venue_name = form.venue_name.data
        venue_location = form.venue_location.data

        existing_venue = Venue.query.filter_by(name=venue_name).first()

        if existing_venue:
            flash(f"Venue '{venue_name}' already exists in the database.")
        else:
            new_venue = Venue(name=venue_name, location=venue_location)
            db.session.add(new_venue)
            db.session.commit()
            flash(f"Venue '{venue_name}' has been created.")

        return redirect(url_for('artists'))

    return render_template('new_venue.html', form=form)


# @app.route('/new_event', methods=['GET', 'POST'])
# def new_event():
#     form = NewEventForm()
#
#     form.venue.choices = [(v.id, v.name) for v in Venue.query.all()]
#
#     form.artists.choices = [(a.id, a.name) for a in Artist.query.all()]
#
#     if request.method == 'POST' and form.validate_on_submit():
#
#         event = Event(
#             name=form.name.data,
#             date=form.date.data,
#             venue_id=form.venue.data,
#             a2es=[Artist.query.get(artist_id) for artist_id in form.artists.data])
#         db.session.add(event)
#         db.session.commit()
#         return "Event added successfully!"
#
#     return render_template('new_event.html', form=form)

@app.route('/new_event', methods=['GET', 'POST'])
def new_event():
    form = NewEventForm()

    form.venue.choices = [(v.id, v.name) for v in Venue.query.all()]
    form.artists.choices = [(a.id, a.name) for a in Artist.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        event = Event(
            name=form.name.data,
            date=form.date.data,
            venue_id=form.venue.data,
        )
        db.session.add(event)

        for artist_id in form.artists.data:
            artist = Artist.query.get(artist_id)
            if artist:
                event.a2es.append(ArtistToEvent(artist=artist))
            else:
                flash("Invalid artist selected")

        db.session.commit()
        flash(f"Event '{event.name}' has been created.")
        return redirect(url_for('artists'))

    return render_template('new_event.html', form=form)



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

    e1 = Event(name="Ozzfest", date=datetime(2024, 3, 3, 12, 0, 0), venue=v2)
    e2 = Event(name="Knotfest", date=datetime(2024, 3, 3, 10, 0, 0), venue=v1)
    e3 = Event(name="Rolling loud", date=datetime(2024, 3, 20, 0, 0, 0), venue=v2)
    e4 = Event(name="Coachella", date=datetime(2024, 4, 2, 10, 0, 0), venue=v3)
    e5 = Event(name="Extravaganza", date=datetime(2024, 4, 15, 0, 0, 0), venue=v1)
    e6 = Event(name="Bayfest", date=datetime(2024, 5, 13, 10, 0, 0), venue=v1)
    e7 = Event(name="Warped Tour", date=datetime(2024, 5, 22, 0, 0, 0), venue=v3)
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# @app.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('user.html', user=user)
