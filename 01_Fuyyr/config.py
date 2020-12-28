import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.


basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/fuyyr'
