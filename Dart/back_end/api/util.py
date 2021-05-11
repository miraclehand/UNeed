import datetime
import glob, os
import pymodm.errors as errors
import functools
import jwt
import json
import requests
from bson import ObjectId
from concurrent.futures import ThreadPoolExecutor
from flask import request, make_response, jsonify
from app import app
from constants import *
from db.models import Disc, User, UserDisc, Watch, UserWatch, StdDisc, UnitDetail, Unit, UserSimula, Simula, Stats, Corp, Version, Chat, UserChatRoom, ChatRoom

def res_error(message, status):
    return '', '%d %s' % (status, message)

def to_json(value):
    return json.loads(json.dumps(value, default=json_default))

def json_default(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        return value
    if isinstance(value, Version):
        return value.to_dict
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
    if isinstance(value, UserChatRoom):
        return value.to_dict
    if isinstance(value, Watch):
        return value.to_dict
    if isinstance(value, Unit):
        return value.to_dict
    if isinstance(value, UnitDetail):
        return value.to_dict
    if isinstance(value, Chat):
        return value.to_dict
    if isinstance(value, ChatRoom):
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

def post_url(args):
    if args is None:
        return None
    return requests.post(BCAST_URL, headers=BCAST_HDR, data=args)

def make_payload(chat):
    user  = chat.user
    watch = chat.watch
    if user.email == 'web':
        return None

    print('>>>>>> post_broadcast', user.email, watch.name, chat.disc.corp.corp_name)
    data = {'data_type':1, 'watch_id':watch.id, 'watch_name': watch.name, 'chat':chat.to_dict}

    token_phrase = f'"to":"{user.pushToken}"'
    title_phrase = f'"title":"[공시]{chat.disc.corp.corp_name}"'
    body_phrase  = f'"body":"{chat.disc.report_nm}"'
    data_phrase  = f'"data":{data}'
    sound_phrase = f'"sound":"default"'

    payload = f'{{ {token_phrase}, {title_phrase}, {body_phrase}, {data_phrase}, {sound_phrase} }}'

    #payload = f'{{ "to":"{token}", "title":"{title}", "body":"{body}", "data" : {data} "sound":"default" }}'
    return payload.replace("'",'"').replace('\n','\\n').encode('utf-8')

def post_broadcast_async(payloads):
    with ThreadPoolExecutor(max_workers=10) as pool:
        response_list = list(pool.map(post_url,payloads))

def post_broadcast(payloads):
    return requests.post(BCAST_URL, headers=BCAST_HDR, data=payloads)

def make_user_payload(user, chats):
    token = user.pushToken

    if user.email == 'web':
        return None

    print('>>>>>>>>>>>>>>>>>>>> make_user_payload', user.email, chats.__len__())

    title = '[공시]'
    body  = '[공시]'
    data = {'data_type': '1', 'resend':resend, 'chats' : [{'watch_id':chat.watch.id, 'chat':chat.to_dict} for chat in chats]}

    if resend:
        sound_phrase = f', "sound":"default"'
    else:
        sound_phrase = ''

    payload = f'{{ "to":"{token}", "title":"{title}", "body":"{body}", "data" : {data} {sound_phrase} }}'
    return payload.replace("'",'"').replace('\n','\\n').encode('utf-8')

def post_broadcast(user, chast):
    token = user.pushToken

    if user.email == 'web':
        return None

    print('>>>>>>>>>>>>>>>>>>>> make_user_payload', user.email, chats.__len__())

    title = '[공시]'
    body  = '[공시]'
    data = {'data_type': '1', 'resend':resend, 'chats' : [{'watch_id':chat.watch.id, 'chat':chat.to_dict} for chat in chats]}

    if resend:
        sound_phrase = f', "sound":"default"'
    else:
        sound_phrase = ''

    payload = f'{{ "to":"{token}", "title":"{title}", "body":"{body}", "data" : {data} {sound_phrase} }}'
    payload = payload.replace("'",'"').replace('\n','\\n').encode('utf-8')
    requests.post(BCAST_URL, headers=BCAST_HDR, data=payload)

#https://codethief.io/ko/sending-simultaneous-requests-using-python/
