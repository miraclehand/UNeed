from flask_restful import Resource
from flask import request
from db.models import User
from app import app
from util import write_log
from api.util import to_json
from constants import *

class UserAPI(Resource):
    def __init__(self):
        super(UserAPI, self).__init__()

    def get(self, usid=None):
        write_log(request.remote_addr,'user get',usid)

        user = User.objects.get({'token':usid})

        return {'user':to_json(user)}
    #update-task
    def put(self, id=None):
        print('111111111111111111111111111111111111111111')
        write_log(request.remote_addr,'user put',usid)

        data = request.get_json()
        print('put')
        print(data)

    #add-task
    def post(self, usid=None):
        write_log(request.remote_addr,'user post',usid)

        data = request.get_json()
        print('POST', data)

        name      = data["name"]
        email     = data["email"]
        pushToken = data["pushToken"]
        level     = data["level"]

        try:
            user = User.objects.get({'email':email})
            user.name      = name
            user.pushToken = pushToken
            user.level     = level
            user.save()
        except:
            user = User(name, email, pushToken, level)
            user.save()
        return {'user':to_json(user)}

    #delete-task
    def delete(self, usid=None):
        write_log(request.remote_addr,'user delete',usid)

