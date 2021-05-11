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

class ChatRoomAPI(Resource):
    def __init__(self):
        super(ChatRoomAPI, self).__init__()

    def get(self, cntry=None, usid=None):
        write_log(request.remote_addr,'chat room get',cntry, usid)

        user = User.objects.get({'email':usid})
        try:
            ucr = UserChatRoom.objects.get({'user':user._id})
        except:
            return {'rooms':None}

        return {'rooms': ucr.to_dict['rooms']}

    #update-task
    def put(self, cntry=None, usid=None):
        write_log(request.remote_addr,'chat put',cntry)

    #add-task
    def post(self, cntry=None, usid=None):
        write_log(request.remote_addr,'chat post',cntry)

    #delete-task
    def delete(self, cntry=None, usid=None):
        write_log(request.remote_addr,'chat delete',cntry)

        user = User.objects.get({'email':usid})
        try:
            ucr = UserChatRoom.objects.get({'user':user._id})
        except:
            return {'rooms':None}

        data = request.get_json()
        watch_id = data['watch_id']
        print('del', watch_id)


