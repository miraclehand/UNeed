from flask_restful import Resource
from flask import request
from bson import ObjectId
from datetime import datetime
from db.models import User, Watch, UserChatRoom, Chat
from app import app
from util import write_log
from api.util import to_json, make_payload, post_broadcast_async
from api.util import post_broadcast
from constants import *

class ChatAPI(Resource):
    def __init__(self):
        super(ChatAPI, self).__init__()

    def get(self, cntry=None, usid=None, id=None):
        write_log(request.remote_addr,'chat get',cntry, usid, id)

        user = User.objects.get({'email':usid})
        try:
            ucr = UserChatRoom.objects.get({'user':user._id})
        except:
            return {'chats':None}

        for room in ucr.rooms:
            if str(room.watch.id) != str(id):
                continue
            return {'chats':to_json(room)}

        return {'chats':None}
    
    #update-task
    def put(self, cntry=None, id=None):
        write_log(request.remote_addr,'chat put',cntry)

    #add-task
    def post(self, cntry=None, id=None):
        write_log(request.remote_addr,'chat post',cntry)

    #delete-task
    def delete(self, cntry=None):
        write_log(request.remote_addr,'chat delete',cntry)

        user = User.objects.get({'email':id})

class ChatCatchupAPI(Resource):
    def __init__(self):
        super(ChatCatchupAPI, self).__init__()

    def get(self, cntry=None, usid=None, id=None):
        print('chatcatchup get', usid, id)
        write_log(request.remote_addr,'chatcatchup get',cntry, usid, id)

        user = User.objects.get({'email':usid})
        try:
            ucr = UserChatRoom.objects.get({'user':user._id})
            sql = ''
        except:
            sql = 'drop table std_disc;drop table watch; drop table watch_stock; drop table disc; drop table chat_room; drop table chat;'
            return {'exec_query':sql }

        chats = Chat.objects.raw({
            '_id': {'$gt' : ObjectId(id)},
            'user':user._id,
            'recv_date': {'$exists': False}
        }).order_by([('_id',1)])

        rooms = chats.aggregate(
            {'$group' : { '_id' : '$watch',
                          'chat_id': { '$max': '$_id'},
                          'last_label': { '$last' : '$label'},
                          'badge': {'$sum':1},
            }},
            {'$sort': {'chat_id': 1}},
        )
        rooms = [{'watch_id':room['_id'], 'last_label':room['last_label'], 'badge':room['badge']} for room in rooms]

        for room in rooms:
            watch = Watch.objects.get({'_id': room['watch_id']})
            room['watch_id']   = watch.id
            room['watch_name'] = watch.name

        l_chats = list(chats)
        last_chat_id = str(l_chats[-1]._id) if l_chats.__len__() > 0 else '0'


        return {'last_chat_id':last_chat_id,
                'exec_query':sql,
                'chats':to_json(l_chats),
                'rooms':to_json(rooms)
        }

class ChatCheckAPI_to_remomve(Resource):
    def __init__(self):
        super(ChatCheckAPI_to_remomve, self).__init__()

    def get(self, cntry=None, usid=None, id=None):
        print('chatcheck get', usid, id)
        write_log(request.remote_addr,'chatcheck get',cntry, usid, id)

        user = User.objects.get({'email':usid})
        try:
            ucr = UserChatRoom.objects.get({'user':user._id})
        except:
            return {'rooms':None}

        if not id:
            return {'rooms':None}

        chats = Chat.objects.raw({
            '_id': {'$gt' : ObjectId(id)},
            'user':user._id,
            'recv_date': {'$exists': False}
        })
        """
        chats = Chat.objects.raw({
            'user':user._id,
            'watch': ObjectId('6059e1e7c3cbba450c022205')
        })
        """

        if chats.count() == 0:
            return {'rooms':None}

        payloads = [make_payload(chat, '1') for chat in chats]
        post_broadcast_async(payloads)
        #payloads = make_user_payload(user, chats)
        #post_broadcast(user, chats)

        cursor = list(chats.aggregate(
            {'$group' : { '_id' : '$watch',
                          'chat_id': { '$max': '$_id'},
                          'last_label': { '$last' : '$label'},
                          'badge': {'$sum':1},
            }},
            {'$sort': {'chat_id': 1}},
        ))

        rooms = [{'watch_id':c['_id'], 'last_label':c['last_label'], 'badge':c['badge']} for c in cursor]

        for room in rooms:
            watch = Watch.objects.get({'_id': room['watch_id']})
            room['watch_id']   = watch.id
            room['watch_name'] = watch.name

        return {'rooms':to_json(rooms)}

        """
        chat_id = None
        for room in ucr.rooms:
            for chat in room.chats:
                if chat.recv_date is not None:
                    continue
                if str(chat._id) > str(id):
                    post_broadcast(user, room.watch, chat)
                    chat_id = chat._id
            return {'chatid':str(chat_id)}
        """

        return {'chatid':None}
    
    #update-task
    def put(self, cntry=None, usid=None, id=None):
        print('chatcheck put', usid, id)
        write_log(request.remote_addr,'chatcheck put',cntry)

        now = datetime.now()
        Chat.objects.raw({'_id':ObjectId(id)}).update({'$set':{'recv_date':now}})

    #add-task
    def post(self, cntry=None, id=None):
        write_log(request.remote_addr,'chat post',cntry)

    #delete-task
    def delete(self, cntry=None):
        write_log(request.remote_addr,'chat delete',cntry)

        user = User.objects.get({'email':id})
