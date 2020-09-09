# Setup for Flask App
import os
from flask import Flask

app = Flask(__name__)
# app.secret_key = os.environ['SECRET_KEY']

# Setup for Database
from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///local.db'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import c_and_c.views
