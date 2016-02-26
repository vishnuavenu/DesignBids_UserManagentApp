import os

from flask import Flask
from flask_bootstrap import Bootstrap
APP_GID = 1111
APP_GRP = "calmusers/"

# Users directory
# USER_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), APP_GRP)
USER_DIR = os.path.join(os.path.dirname(__file__), "..", APP_GRP)

app = Flask(__name__)
app.debug = True
# adding bootstrap
Bootstrap(app)

# Precautions in order to avoid cyclic - redundancy
from app import controllers

