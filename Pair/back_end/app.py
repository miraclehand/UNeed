from flask import Flask

app = Flask(__name__, static_folder="../front_end/static/dist", template_folder="../front_end/templates")
app.config.from_pyfile('config.py')
app.config['SERVER_NAME'] = app.config['PAIR_SERVER_NAME']
app.config['SESSION_COOKIE_DOMAIN'] = app.config['SERVER_NAME']

