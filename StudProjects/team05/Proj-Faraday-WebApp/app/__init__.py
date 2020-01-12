import os

from flask import Flask

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))

from app import models, routes
