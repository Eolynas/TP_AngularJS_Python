import logging
import os

from flask import Flask

from app.tools import logger


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
from app import routes
