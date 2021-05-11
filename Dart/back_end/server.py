import sys
sys.path.append('../../')

from flask_restful import Api
from flask import render_template
from flask import send_from_directory
from flask import current_app
import os
from app import app
from init import init
from api.version import VersionAPI
from api.user import UserAPI
from api.tick import TickAPI
from api.corp import CorpAPI
from api.disc import DiscAPI, StdDiscAPI
from api.watch import WatchAPI
#from api.alert import AlertAPI, AlertRoomAPI
#from api.room import RoomAPI
from api.room import ChatRoomAPI
from api.chat import ChatAPI, ChatCatchupAPI
from api.chart import ChartAPI
from api.simula import SimulaAPI
from job import job_weekly, job_daily, job_seconds, job_tick
from task.singleton import shed
import time
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#import ssl

api = Api(app)

# resource map
api.add_resource(VersionAPI,'/api/version', endpoint='version')
api.add_resource(UserAPI,   '/api/user/<usid>', endpoint='user')
api.add_resource(CorpAPI,   '/api/corps/<cntry>',
                            '/api/corp/<cntry>/<id>', endpoint='corp')
api.add_resource(DiscAPI,   '/api/discs/<cntry>', 
                            '/api/disc/<cntry>/<id>', 
                            '/api/disc/<cntry>/<begin>/<end>',
                            endpoint='disc')
api.add_resource(StdDiscAPI,'/api/std_discs/<cntry>', endpoint='std_disc')
api.add_resource(TickAPI,   '/api/tick/<cntry>/<code>/<thistime>', 
                            '/api/ticks/<cntry>', 
                            endpoint='tick')
#api.add_resource(AlertAPI,  '/api/alert/<cntry>/<usid>', endpoint='alert')
#api.add_resource(RoomAPI,   '/api/room/<cntry>/<usid>', endpoint='room')
#api.add_resource(AlertRoomAPI, '/api/alert_room/<cntry>/<usid>/<id>', endpoint='alert_room')
#api.add_resource(ChatRoomAPI,'/api/chat_room/<cntry>/<usid>', endpoint='chat_room')
#api.add_resource(ChatAPI,   '/api/chat/<cntry>/<usid>/<id>', endpoint='chat')

api.add_resource(ChatRoomAPI,'/api/chat_room/<cntry>/<usid>', endpoint='chat_room')
api.add_resource(ChatAPI,   '/api/chat/<cntry>/<usid>/<id>', endpoint='chat')
api.add_resource(ChatCatchupAPI,'/api/chat_catchup/<cntry>/<usid>/<id>', 
                            endpoint='chat_catchup')

api.add_resource(ChartAPI,  '/api/chart/<cntry>', endpoint='chart')
api.add_resource(WatchAPI,  '/api/watchs/<cntry>/<usid>', endpoint='watch')
api.add_resource(SimulaAPI,  '/api/simula/<cntry>/<usid>',
                             '/api/simula/<cntry>/<usid>/<id>',endpoint='simula')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder + '/image', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def create_app(test_config=None):
    if test_config is None:
        #app.config.from_pyfile('config.py', silent=True)
        app.config.from_mapping(
            SECRET_KEY='dev',
            #DATABASE=os.path.join(app.instance_path, 'prototype.sqlite') ,
        )
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app

if __name__ == '__main__':
    if not os.path.isdir('./log'):
        os.mkdir('./log')

    init()

    # run once
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == 'true':
        shed.remove_all()
        shed.add_cron_job(job_weekly,  'fri', '20', '0')
        shed.add_cron_job(job_daily,   '*', '0', '0')
        shed.add_interval_job(job_seconds, 70, 'job_seconds')
        shed.add_cron_job(job_tick,    'mon-fri', '16', '30')

    #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    #ssl_context.load_cert_chain(certfile='../cert/newcert.pem', keyfile='../cert/newkey.pem', password=app.config['SECRET_KEY'])

    #app.run(host='0.0.0.0', port=5000)
    app.run(host='192.168.0.7', port=8200)
    #app.run(host='192.168.0.7', port=8200, ssl_context=ssl_context)
    app.run()

