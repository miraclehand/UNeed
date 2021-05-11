from flask_restful import Resource
from flask import request
from db.models import User, Watch, UserWatch, StdDisc
from app import app
from util import write_log
from api.util import to_json
from constants import *

class WatchAPI(Resource):
    def __init__(self):
        super(WatchAPI, self).__init__()

    def get(self, cntry=None, usid=None):
        write_log(request.remote_addr,'user watch get',cntry)

        user = User.objects.get({'email':usid})

        try:
            watchs = UserWatch.objects.get({'user':user._id}).watchs
        except:
            return {'watchs':[]}

        return {'watchs':to_json(list(watchs))}
    
    #update-task
    def put(self, cntry=None, usid=None):
        print('put', cntry, usid)
        write_log(request.remote_addr,'user watch put',cntry)

        data = request.get_json()
        unit = data['unit']

        user = User.objects.get({'email':usid})
        watchs = list(UserWatch.objects.raw({'user':{'$eq':user._id}}).watchs)

        return {'watchs':to_json(watchs)}
        
    #add-task
    def post(self, cntry=None, usid=None):
        write_log(request.remote_addr,'user watch post',cntry)
        print('post', cntry, usid)

        data = request.get_json()

        unit = data['unit']
        print('post', unit)

        user = User.objects.get({'email':usid})

        std_disc = StdDisc.objects.get({'id':unit['std_disc']['std_disc_id']})
        unit['std_disc'] = std_disc

        user_watch = None
        try:
            user_watch = UserWatch.objects.get({'user':user._id})
        except:
            user_watch = UserWatch(user)

        new_watch = Watch(unit)
        new_watch.save()
        user_watch.add_watch(new_watch)
        user_watch.save()

        return {'watchs':to_json(list(user_watch.watchs))}

    #delete-task
    def delete(self, cntry=None, usid=None):
        print('delete', cntry, usid)
        write_log(request.remote_addr,'user watch delete',cntry)

        data = request.get_json()

        unit = data['unit']

        user = User.objects.get({'email':usid})
        user_watch = UserWatch.objects.get({'user':user._id})
        user_watch.del_watch(unit)
        if user_watch.watchs.__len__() == 0:
            user_watch.delete()
        else:
            user_watch.save()

