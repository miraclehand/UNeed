import json
import sys
from flask import request, make_response, jsonify
from app import app
from basedb.models import Ohlcv, Stock, Candle

def to_json(value):
    return json.loads(json.dumps(value, default=json_default))

def json_default(value):
    if isinstance(value, Stock):
        return value.to_dict
    if isinstance(value, Candle):
        return value.to_dict
    if isinstance(value, Ohlcv):
        return value.to_dict
    if hasattr(value, 'isoformat'):
        return value.isoformat()
    raise TypeError('not JSON serializable')

