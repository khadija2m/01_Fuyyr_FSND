## Introduction:

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

Your job is to build out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.


## Overview:

This site developed to be able to do the following, if not more, by using a PostgreSQL database:

* creating new venues, artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.

We want Fyyur to be the next new platform that artists and musical venues can use to find each other, and discover new music shows.


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** The forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

## Run Application:

1. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

2. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)

## Use:

This application have 3 sections/pages:
1- Artist: where you see the information about an Artist, add new artist, edit and update the information, or delete the artist.

2- Venues: in the venues page you can see the information about a venue, update one, delete or add new.

3- Shows: it represents the latest show and the upcomming one, and you can perform any update, delete, or add a show to the list.


		** Hope you enjoy it ! **
