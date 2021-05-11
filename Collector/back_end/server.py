import sys
sys.path.append('../../')

from flask_restful import Api
from flask import render_template, request, abort
from flask import send_from_directory
from app import app
from api.crawler import StockAPI, CandleAPI, CompanyAPI, TickAPI
from job import put_stock_kr, put_candle_kr
from job import put_stock_us, put_candle_us
from commons.utils.scheduler import shed
from commons.banip.banip import ip_ban_list
import os
import time

api = Api(app)

# resource map
api.add_resource(StockAPI,  '/api/crawler/stocks/<cntry>',
                            '/api/crawler/stock/<cntry>/<id>',
                            endpoint='stock')
api.add_resource(CandleAPI, '/api/crawler/candles/<cntry>',
                            '/api/crawler/candle/<cntry>/<id>',
                            endpoint='candle')
api.add_resource(CompanyAPI,'/api/crawler/company/<cntry>/<id>',
                            endpoint='company')
api.add_resource(TickAPI,   '/api/crawler/tick/<cntry>/<id>',
                            endpoint='tick')


@app.before_request
def block_method():
    ip = request.environ.get('REMOTE_ADDR')
    if ip in ip_ban_list:
        abort(403)

    #uri = request.environ.get('REQUEST_URI')
    #if not '/api/crawler/' in uri:
    #    abort(403)

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

# run once
# gunicorn을 사용해서 app server를 실행시키면, workers 개수만 큼 sche가 생성됨.
if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == 'true':
    print('shed start')
    if app.config['HOSTNAME'] == 'hikey970':
        shed.remove_all()
        shed.add_cron_job(put_candle_kr, 'mon-fri', '15', '40')
        shed.add_cron_job(put_candle_us, 'tue-sat', '6',  '35')
        shed.add_cron_job(put_stock_kr,  'mon-fri', '20', '0')
        shed.add_cron_job(put_stock_us,  'tue-sat', '11', '0')
"""
import logging
from logging.handlers import RotationgFileHandler
handler = RotationgFileHandler('aaa.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
app.logger.debug('ttttttttttttttttt1')
"""

if __name__ == '__main__':

    #app.run(host='0.0.0.0', port=5000)
    app.run(host=app.config['COLLECTOR_INTER_IP'], port=app.config['COLLECTOR_PORT'])
    #app.run()
