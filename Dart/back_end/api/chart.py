from flask_restful import Resource
from flask import request
from app import app
from util import write_log
from api.util import to_json
from constants import *
import requests

import sys
sys.path.append('/home/yepark/Production/UNeed')
from data.db.models import Ohlcv, StockKr, CandleKr, StockUs, CandleUs

#import sys, os

#sys.path.append('/home/yepark/Production/stock_analyzer/back_end')
#from analyzer.db.models import CandleKr

class ChartAPI(Resource):
    def __init__(self):
        super(ChartAPI, self).__init__()

    def get(self, cntry=None):
        write_log(request.remote_addr,'chart get',cntry)

        code = request.args.get('code')
        print('get', code)

        #df = get_ohlcv_db(CandleKr, code)
