from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('../../uneed.config.py')
app.config['SERVER_NAME'] = app.config['COLLECTOR_SERVER_NAME']
app.config['SESSION_COOKIE_DOMAIN'] = app.config['SERVER_NAME']

CORS(app)
#CORS(app, resources={r'/_api/*': {'origins': 'https://dartuneed.com:5000'}})
