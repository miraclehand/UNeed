DEBUG = False
AWS_IP = 'ec2-13-125-8-70.ap-northeast-2.compute.amazonaws.com'
COLLECTOR_INTER_IP = '192.168.0.7'
COLLECTOR_OUTER_IP = '125.183.209.195'
COLLECTOR_PORT = '8000'
COLLECTOR_SERVER_NAME = COLLECTOR_OUTER_IP + ':' + COLLECTOR_PORT

PAIR_INTER_IP = '192.168.0.7'
PAIR_OUTER_IP = '125.183.209.195'
PAIR_PORT = '8100'
PAIR_SERVER_NAME = PAIR_OUTER_IP + ':' + PAIR_PORT

URL_COLLECTOR = 'http://' + COLLECTOR_SERVER_NAME
URL_PAIR      = 'http://' + PAIR_SERVER_NAME

SECRET_KEY = 'Thisissupposedtobesecret!'

#SERVER_NAME = PAIR_IP + ':' + PAIR_PORT
#SESSION_COOKIE_DOMAIN = SERVER_NAME
#MONGODB_DB = 'pair'
#MONGODB_HOST = 'localhost'
#MONGODB_PORT = 27017

