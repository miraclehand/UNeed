import json

HOSTNAME = ''
INTER_IP = ''
OUTER_IP = ''
COLLECTOR_PORT = ''
PAIR_PORT = ''
SECRET_KEY = ''

with open('../../uneed.config.json') as json_file:
    json_data = json.load(json_file)
    HOSTNAME = json_data['HOSTNAME']
    AWS_IP   = json_data['AWS_IP']
    HIKEY_INTER_IP = json_data['HIKEY_INTER_IP']
    HIKEY_OUTER_IP = json_data['HIKEY_OUTER_IP']
    COLLECTOR_PORT = json_data['COLLECTOR_PORT']
    PAIR_PORT  = json_data['PAIR_PORT']
    SECRET_KEY = json_data['SECRET_KEY']

DEBUG = False
INTER_IP = HIKEY_INTER_IP if HOSTNAME == 'hikey970' else AWS_IP
OUTER_IP = HIKEY_OUTER_IP if HOSTNAME == 'hikey970' else AWS_IP

COLLECTOR_INTER_IP = INTER_IP
COLLECTOR_OUTER_IP = OUTER_IP
COLLECTOR_SERVER_NAME = COLLECTOR_OUTER_IP + ':' + COLLECTOR_PORT

PAIR_INTER_IP = INTER_IP
PAIR_OUTER_IP = OUTER_IP
PAIR_SERVER_NAME = PAIR_OUTER_IP + ':' + PAIR_PORT

URL_COLLECTOR = 'http://' + COLLECTOR_SERVER_NAME
URL_PAIR      = 'http://' + PAIR_SERVER_NAME

