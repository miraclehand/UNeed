import sys
sys.path.append('../../')

from flask_restful import Api
from flask import render_template, request, abort
from flask import send_from_directory
from flask import current_app
import os
from app import app
from api.chart import NormChartAPI, LogChartAPI, HistChartAPI, VolChartAPI
from api.pair import NodePairAPI, PickedPairAPI
from api.strategy import ProgressAPI, StrainerAPI, SimulaReportAPI, TradingReportAPI
from api.balance import AssetAPI
from api.auth import SignInAPI, SignOnAPI
from job import put_picked_pair_kr, put_node_pair_kr, job_daily_kr
from job import put_picked_pair_us, put_node_pair_us, job_daily_us
from utils.scheduler import shed
from banip.banip import ip_ban_list
import time

api = Api(app)

# resource map
api.add_resource(NormChartAPI,'/api/chart/norm_chart/<cntry>', endpoint='norm_chart')
api.add_resource(LogChartAPI, '/api/chart/log_chart/<cntry>', endpoint='log_chart')
api.add_resource(HistChartAPI,'/api/chart/hist_chart/<cntry>',endpoint='hist_chart')
api.add_resource(VolChartAPI, '/api/chart/vol_chart/<cntry>', endpoint='vol_chart')

api.add_resource(NodePairAPI,  '/api/pair/node_pair/<cntry>', endpoint='node_pair')
api.add_resource(PickedPairAPI,'/api/pair/picked_pair/<cntry>', endpoint='picked_pair')
#api.add_resource(ClassifyAPI,  '/api/pair/classify', endpoint='classify')

api.add_resource(SignInAPI, '/api/auth/signin', endpoint='signin')
api.add_resource(SignOnAPI, '/api/auth/signon', endpoint='signon')

api.add_resource(AssetAPI,  '/api/balance/asset/<id>', endpoint='asset')

api.add_resource(ProgressAPI,     '/api/strategy/progress/<cntry>/<id>', endpoint='progress')
api.add_resource(StrainerAPI,     '/api/strategy/strainer/<cntry>/<id>', endpoint='strainer')
api.add_resource(SimulaReportAPI, '/api/strategy/simula/<cntry>/<id>', endpoint='simula')
api.add_resource(TradingReportAPI,'/api/strategy/trading/<cntry>/<id>',endpoint='trading')

uris = ['/', '/api/chart/','/api/pair/','/api/auth/','/api/balance/','/api/strategy']

@app.before_request
def block_method():
    ip = request.environ.get('REMOTE_ADDR')
    if ip in ip_ban_list:
        abort(403)

    uri = request.environ.get('REQUEST_URI')
    if not any(u in uri for u in uris):
        abort(403)

@app.route('/')
@app.route('/signin')
@app.route('/signon')
@app.route('/chart')
@app.route('/trading')
@app.route('/simula')
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
    if not os.path.isdir(app.static_folder  + '/image'):
        os.mkdir(app.static_folder  + '/image')
    if not os.path.isdir(app.static_folder  + '/xls'):
        os.mkdir(app.static_folder  + '/xls')
    if not os.path.isdir(app.static_folder  + '/xls/kr'):
        os.mkdir(app.static_folder  + '/xls/kr')
    if not os.path.isdir(app.static_folder  + '/xls/us'):
        os.mkdir(app.static_folder  + '/xls/us')
    if not os.path.isdir(app.static_folder  + '/xls/kr/pair'):
        os.mkdir(app.static_folder  + '/xls/kr/pair')
    if not os.path.isdir(app.static_folder  + '/xls/us/pair'):
        os.mkdir(app.static_folder  + '/xls/us/pair')
    if not os.path.isdir(app.static_folder  + '/xls/kr/simula'):
        os.mkdir(app.static_folder  + '/xls/kr/simula')
    if not os.path.isdir(app.static_folder  + '/xls/us/simula'):
        os.mkdir(app.static_folder  + '/xls/us/simula')
    if not os.path.isdir('./log'):
        os.mkdir('./log')

    # run once
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == 'true':
        if app.config['HOSTNAME'] == 'hikey970':
            shed.remove_all()
            shed.add_cron_job(put_picked_pair_kr, 'mon-fri', '16', '0')
            shed.add_cron_job(put_node_pair_kr,  'fri', '20', '0')
            shed.add_cron_job(job_daily_kr,   '*', '23', '50')

    #app.run(host='0.0.0.0', port=5000)
    app.run(host=app.config['PAIR_INTER_IP'], port=app.config['PAIR_PORT'])
    #app.run()
