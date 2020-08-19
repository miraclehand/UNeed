from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('config.py')

CORS(app)
#CORS(app, resources={r'/_api/*': {'origins': 'https://dartuneed.com:5000'}})

