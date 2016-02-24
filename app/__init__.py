from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.debug = True
# adding bootstrap
Bootstrap(app)

# Precautions in order to avoid cyclic - redundancy
from app import views
