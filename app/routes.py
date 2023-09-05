from flask import render_template
from app import app


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
    return render_template("caamp.html", title="Caamp",)


@app.route('/new_artist')
def new_artist():
    return render_template("new_artist.html", title="New Artist")


