#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
from flask_migrate import Migrate
from models import app, db, Venue, Artist, Show

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

moment = Moment(app)
app.config.from_object('config')
db.init_app(app)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = value
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  VENUES
#  ----------------------------------------------------------------

#  repesent the list of the venues filtered by City.
@app.route('/venues')
def venues():
    venueslist = Venue.query.with_entities(Venue.state, Venue.city).distinct().all()
    areas = []
    for state, city in venueslist:
        felteredvenues = Venue.query.filter_by(state=state).filter_by(city=city).all()
        areas.append({
            "city": city,
            "state": state,
            "venues": felteredvenues
        })
    return render_template('pages/venues.html', areas=areas)



# search_venues
# ---------------------------------
@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term=request.form.get('search_term', '')
    venue = Venue.query.filter(Venue.name.like('%'+search_term+'%')).all()
    response = {"count": len(venue), "data": venue}

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


#   display information of a venue depends on venue_id
#   -----------------------------
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    s_time = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).all()
    upcoming_shows = []
    past_shows = []
    current_time = datetime.today()
    for i in s_time:
        artist = Artist.query.get(i.artist_id)
        if i.start_time > current_time:
            upcoming_shows.append({
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": i.start_time
            })
        else:
            past_shows.append({
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": i.start_time
            })

    return render_template('pages/show_venue.html', venue=venue, upcoming_shows=upcoming_shows, past_shows=past_shows, past_shows_count=len(past_shows), upcoming_shows_count=len(upcoming_shows))



#  Create new Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)
    error = False
    if form.validate():
        try:
            name = request.form.get('name')
            city = request.form.get('city')
            state = request.form.get('state')
            address = request.form.get('address')
            phone = request.form.get('phone')
            image_link = request.form.get('image_link')
            facebook_link = request.form.get('facebook_link')

            new_venue = Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link, facebook_link=facebook_link)
            db.session.add(new_venue)
            db.session.commit()

        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
    else:
        flash(form.errors)

    if not error:
        return redirect(url_for('venues'))

# --------------------------------------
# edit_venue

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(request.form)
    error = False
    if form.validate():
        try:
            venue.name = request.form.get('name')
            venue.city = request.form.get('city')
            venue.state = request.form.get('state')
            venue.address = request.form.get('address')
            venue.phone = request.form.get('phone')
            venue.image_link = request.form.get('image_link')
            venue.facebook_link = request.form.get('facebook_link')

            db.session.add(venue)
            db.session.commit()

        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
    else:
         flash(form.errors)

    return redirect(url_for('show_venue', venue_id=venue_id))


#-------------------------------------
#  Artists
#  ----------------------------------------------------------------------
# show the list of the artists
@app.route('/artists')
def artists():
    artistslist = Artist.query.with_entities(Artist.id,Artist.name).distinct().all()
    artists = []
    for id, name in artistslist:
        artists.append({
            "id": id,
            "name": name
        })
    return render_template('pages/artists.html', artists=artists)


# search an artist name
@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term=request.form.get('search_term', '')
    artist = Artist.query.filter(Artist.name.like('%'+search_term+'%')).all()
    response = {"count": len(artist), "data": artist}

    return render_template('pages/search_artists.html', results=response, search_term=search_term)


# display an artist information
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    s_time = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).all()
    upcoming_shows = []
    past_shows = []
    current_time = datetime.today()
    for i in s_time:
        venue = Venue.query.get(i.venue_id)
        if i.start_time > current_time:
            upcoming_shows.append({
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": i.start_time
            })
        else:
            past_shows.append({
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": i.start_time
            })

    return render_template('pages/show_artist.html', artist=artist, upcoming_shows=upcoming_shows, past_shows=past_shows, past_shows_count=len(past_shows), upcoming_shows_count=len(upcoming_shows))



#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artists_submission():
    form = ArtistForm(request.form)
    error = False
    if form.validate():
        try:
            name = request.form.get('name')
            city = request.form.get('city')
            state = request.form.get('state')
            phone = request.form.get('phone')
            genres = request.form.get('genres')
            image_link = request.form.get('image_link')
            facebook_link = request.form.get('facebook_link')

            new_artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, image_link=image_link, facebook_link=facebook_link)
            db.session.add(new_artist)
            db.session.commit()

        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
    else:
        flash(form.errors)

    if not error:
        return redirect(url_for('artists'))

# edit artist information

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(request.form)
    error = False
    if form.validate():
        try:
            artist.name = request.form.get('name')
            artist.city = request.form.get('city')
            artist.state = request.form.get('state')
            artist.phone = request.form.get('phone')
            artist.genres = request.form.get('genres')
            artist.image_link = request.form.get('image_link')
            artist.facebook_link = request.form.get('facebook_link')

            db.session.add(artist)
            db.session.commit()

        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
    else:
        flash(form.errors)

    return redirect(url_for('show_artist', artist_id=artist_id))

#  Shows
#  ----------------------------------------------------------------
# display the list of the shows
@app.route('/shows')
def shows():
    shows = Show.query.all()
    data=[]
    for show in shows:
        venue = Venue.query.get(show.venue_id)
        artist = Artist.query.get(show.artist_id)
        data.append({
            "venue_id": venue.id,
            "venue_name": venue.name,
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time
        })

    return render_template('pages/shows.html', shows=data)



# create new show
@app.route('/shows/create', methods=['GET'])
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():

    error = False
    try:
        venue_id = request.form.get('venue_id')
        artist_id = request.form.get('artist_id')
        start_time = request.form.get('start_time')

        new_show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
        db.session.add(new_show)
        db.session.commit()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()

    if not error:
        return redirect(url_for('shows'))

#           ------------------------------------------------
##         -------------------------------



@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
