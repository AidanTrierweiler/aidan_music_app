from flask import render_template, redirect, url_for, flash
from app import app
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
