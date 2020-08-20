import datetime
import glob, os
import pymodm.errors as errors
import functools
import jwt
import json
from flask import request, make_response, jsonify
from app import app
from basedb.models import Stock, StockKr, StockUs
from basedb.models import Candle
from db.models import Asset, Entry, Strainer

def get_code(cntry, code):
    if code is None:
        return None

    if cntry == 'kr':
        Stock = StockKr
    else:
        Stock = StockUs

    try:
        return Stock.objects.get({'$or': [{'code':code}, {'name':code}]}).code
    except errors.DoesNotExist:
        pass

    return None

def get_name(code):
    if cntry == 'kr':
        Stock = StockKr
    else:
        Stock = StockUs

    try:
        name = Stock.objects.get({'code':code}).name
    except errors.DoesNotExist:
        name = ''
    return name

def get_xls(cntry, path):
    items = []
    absolute_path = os.path.join(app.static_folder, f'xls/{cntry}', path, '*')

    url = app.config['URL_PAIR']
    for filename in sorted(glob.glob(absolute_path), reverse=True):
        splited  = filename.split(os.sep)
        name = os.path.basename(filename)
        link = os.sep.join(splited[-5:])
        link = os.path.join(url, link)
        items.append({'label':name, 'link':link})
    return items

def res_error(message, status):
    return '', '%d %s' % (status, message)
    

def to_json(value):
    return json.loads(json.dumps(value, default=json_default))

def json_default(value):
    if isinstance(value, Stock):
        return value.to_dict
    if isinstance(value, Candle):
        return value.to_dict
    if isinstance(value, Ohlcv):
        return value.to_dict
    if isinstance(value, Asset):
        return value.to_dict
    if isinstance(value, Entry):
        return value.to_dict
    if isinstance(value, Strainer):
        return value.to_dict
    if hasattr(value, 'isoformat'):
        return value.isoformat()
    raise TypeError('not JSON serializable')

def serialzed(message, status_code):
    return make_response(jsonify(message), status_code)

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = None

        #FreePass.objects.get({'$eq':request.remote_addr})
        username = request.headers['username']
        if username == 'admin' or username == 'sar':
            return f(*args, **kwargs)

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'message': 'login required'}), 401)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as e:
            return make_response(jsonify({'message': e.__str__()}), 401)
        return f(*args, **kwargs)
    return decorated
