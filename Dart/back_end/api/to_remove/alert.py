from flask_restful import Resource
from flask import request
from bson import ObjectId
from db.models import User, Watch, Alert, Room
from app import app
from util import write_log
from api.util import to_json
from constants import *
from task.htmlparser import regex_disc
import requests

class AlertAPI(Resource):
    def __init__(self):
        super(AlertAPI, self).__init__()

    def get(self, cntry=None, usid=None):
        write_log(request.remote_addr,'alert get',cntry)

        user = User.objects.get({'email':usid})

        try:
            alert = Alert.objects.get({'user':user._id})
        except:
            return {'rooms':None}

        return {'rooms':to_json(list(alert.rooms))}
    
    #update-task
    def put(self, cntry=None, usid=None):
        write_log(request.remote_addr,'alert put',cntry)

        user = User.objects.get({'email':usid})
        alert = Alert.objects.get({'user':user._id})

        return {'rooms':to_json(list(alert.rooms))}
        
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
            alert = Alert.objects.get({'user':user._id})
        except:
            alert = Alert(user)

        watch = Watch.objects.get({'_id':ObjectId(watch_id)})

        message = None
        #message = Message(title, content)
        message.save()

        room = Room()
        room.watch = watch
        room.last_message = message

        alert.add_or_replace_room(room)
        alert.save()

        #watch_list.add_watch(Watch('stock_code', 'stock_name', keyword))
        #watch_list.save()

        return {'rooms':to_json(list(alert.rooms))}

    #delete-task
    def delete(self, cntry=None):
        write_log(request.remote_addr,'alert delete',cntry)

        user = User.objects.get({'email':id})
        Alert.objects.raw({'user':{'$eq':user}}).delete()

class AlertRoomAPI(Resource):
    def __init__(self):
        super(AlertRoomAPI, self).__init__()

    def get(self, cntry=None, usid=None, id=None):
        write_log(request.remote_addr,'alert get',cntry)

        print('get AlertRoomAPI', cntry, usid, id)
        user = User.objects.get({'email':usid})
        try:
            alert = Alert.objects.get({'user':user._id})
        except:
            return {'discs':None}

        for room in alert.rooms:
            if str(room.watch.id) == str(id):
                print('id', id, 'watch_id', room.watch.id, room.discs.__len__())
                return {'discs':to_json(list(room.discs))}

        return {'discs':None}
    
    #update-task
    def put(self, cntry=None, id=None):
        write_log(request.remote_addr,'alert room put',cntry)

    #add-task
    def post(self, cntry=None, id=None):
        write_log(request.remote_addr,'alert room post',cntry)

    #delete-task
    def delete(self, cntry=None):
        write_log(request.remote_addr,'alert room delete',cntry)

        user = User.objects.get({'email':id})

