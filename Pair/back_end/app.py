from flask import Flask
from flask_cors import CORS
import os

cur_folder = os.path.dirname(__file__)
static_folder   = cur_folder + '/../front_end/static/dist'
template_folder = cur_folder + '/../front_end/templates'

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
app.config.from_pyfile('config.py')
app.config['SERVER_NAME'] = app.config['PAIR_SERVER_NAME']
app.config['SESSION_COOKIE_DOMAIN'] = app.config['SERVER_NAME']

CORS(app)
