import datetime
import glob, os
import pymodm.errors as errors
import functools
import jwt
import json
from flask import request, make_response, jsonify
from app import app
from db.models import Disc, User, UserDisc, Watch, UserWatch, Alert, Room, StdDisc, UnitDetail, Unit, UserSimula, Simula, Stats, Corp

def res_error(message, status):
    return '', '%d %s' % (status, message)

def to_json(value):
    return json.loads(json.dumps(value, default=json_default))

def json_default(value):
    if isinstance(value, User):
        return value.to_dict
    if isinstance(value, Corp):
        return value.to_dict
    if isinstance(value, Disc):
        return value.to_dict
    if isinstance(value, UserDisc):
        return value.to_dict
    if isinstance(value, UserWatch):
        return value.to_dict
    if isinstance(value, Watch):
        return value.to_dict
    if isinstance(value, Unit):
        return value.to_dict
    if isinstance(value, UnitDetail):
        return value.to_dict
    if isinstance(value, Alert):
        return value.to_dict
    if isinstance(value, Room):
        return value.to_dict
    if isinstance(value, StdDisc):
        return value.to_dict
    if isinstance(value, UserSimula):
        return value.to_dict
    if isinstance(value, Simula):
        return value.to_dict
    if isinstance(value, Stats):
        return value.to_dict
    if hasattr(value, 'isoformat'):
        return value.isoformat()
    raise TypeError('not JSON serializable', type(value))

def serialzed(message, status_code):
    return make_response(jsonify(message), status_code)


