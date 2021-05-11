from flask_restful import Resource
from flask import request
from bson import ObjectId
from db.models import User, Watch, UserRoom, Room
from app import app
from util import write_log
from api.util import to_json
from constants import *
from task.htmlparser import regex_disc
import requests

class RoomAPI(Resource):
    def __init__(self):
        super(RoomAPI, self).__init__()

    def get(self, cntry=None, usid=None):
        write_log(request.remote_addr,'room get',cntry)

        user = User.objects.get({'email':usid})

        try:
            user_room = UserRoom.objects.get({'user':user._id})
        except:
            return {'rooms':None}

        return {'rooms':to_json(list(user_room.rooms))}
    
    #update-task
    def put(self, cntry=None, usid=None):
        write_log(request.remote_addr,'alert put',cntry)

        user = User.objects.get({'email':usid})
        user_room = UserRoom.objects.get({'user':user._id})

        return {'rooms':to_json(list(user_room.rooms))}
        
    #add-task
    def post(self, cntry=None, usid=None):
        write_log(request.remote_addr,'alert post',cntry)

        data = request.get_json()

        #stock_code = data['stock_code']
        #stock_name = data['stock_name']
        title     = data['title']
        content   = data['content']
        watch_id  = data['watch_id']

        user = User.objects.get({'email':usid})

        alert = None
        try:
            user_room = UserRoom.objects.get({'user':user._id})
        except:
            user_room = UserRoom(user)

        watch = Watch.objects.get({'_id':ObjectId(watch_id)})

        message = None
        #message = Message(title, content)
        message.save()

        room = Room()
        room.watch = watch
        room.last_message = message

        user_room.add_or_replace_room(room)
        user_room.save()

        #watch_list.add_watch(Watch('stock_code', 'stock_name', keyword))
        #watch_list.save()

        return {'rooms':to_json(list(user_room.rooms))}

    #delete-task
    def delete(self, cntry=None):
        write_log(request.remote_addr,'alert delete',cntry)

        user = User.objects.get({'email':id})
        UserRoom.objects.raw({'user':{'$eq':user}}).delete()

