from flask_restful import Resource
from flask import request
from app import app
from api.util import to_json
from constants import *
from commons.utils.log import write_log
from commons.basedb.models import StockKr, CandleKr, Ohlcv
from commons.basedb.models import StockUs, CandleUs

class ChartAPI(Resource):
    def __init__(self):
        super(ChartAPI, self).__init__()

    def get(self, cntry=None):
        write_log(request.remote_addr,'chart get',cntry)

        code = request.args.get('code')
        print('get', code)

        #df = get_ohlcv_db(CandleKr, code)
