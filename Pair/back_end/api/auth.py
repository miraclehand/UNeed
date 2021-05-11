import jwt
from datetime import datetime, timedelta
import time
from flask_restful import Resource
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
import pymodm.errors as errors
from db.models import User
from api.util import login_required, serialzed

class SignInAPI(Resource):
    def __init__(self):
        super(SignInAPI, self).__init__()

    def get(self):
        print('SignInAPI GET')

    #update-task
    def put(self):
        print('SignInAPI PUT')

    #add-task
    def post(self):
        print('SignInAPI POST')
        data = request.get_json()

        username = data["username"]
        password = data["password"]
        print(username, password)

        try:
            user = User.objects.get({'username':username})
            if check_password_hash(user.password, password):
                days = 0
                minutes = 59
                if username == 'admin': days = 365
                if username == 'sar':   days = 30
                exp_date = datetime.now() + timedelta(days=days,minutes=minutes)
                unixtime = time.mktime(exp_date.timetuple())
                #token = jwt.encode({'public_id' : user.username, 'exp' : unixtime}, app.config['SECRET_KEY']).decode('UTF-8')
                token = jwt.encode({'public_id' : user.username, 'exp' : unixtime}, app.config['SECRET_KEY'])
                level = user.level

                return serialzed({'username':username,'token':token,'level':level}, 201)
        except Exception as e:
            print('error')
            print(e)

        return serialzed({'token':''}, 401)

    #delete-task
    def delete(self):
        print('SignInAPI DELETE')

class SignOnAPI(Resource):
    def __init__(self):
        super(SignOnAPI, self).__init__()

    @login_required
    def get(self):
        print('SignOnAPI GET')
        return serialzed({'message':'get profile', 'username':username}, 201)

    #update-task
    def put(self):
        print('SignOnAPI PUT')
        data = request.get_json()

        username = data["username"]
        password = data["password"]
        new_password = data["new_password"]

        user = User.objects.get({'username':username})

        if user:
            return serialzed({'task':'Not exist [{}]'.format(username)}, 401)
        if check_password_hash(user.password, password):
            user.password = generate_password_hash(new_password,method='sha256')
            user.save()
        else:
            return serialzed({'message':'Not matched password'}, 401)

        return serialzed({'message':'modify auth', 'username':username}, 201)

    #add-task
    def post(self):
        print('SignOnAPI POST')
        data = request.get_json(force = True)

        username = data["username"]
        password = data["password"]
        level    = data["level"]

        try:
            user = User.objects.get({'username':username})
            return serialzed({'message':'exist user:[%s]' % username}, 401)
        except:
            pass
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username,password=hashed_password,level=level)
        new_user.save()

        return serialzed({'message':'create user', 'username':username}, 201)

    #delete-task
    def delete(self):
        print('SignOnAPI DELETE')
        data = request.get_json()

        username = data["username"]
        password = data["password"]

        try:
            user = User.objects.get({'username':username})
        except:
            return serialzed({'message':'Not exist [%s]' % username}, 401)

        if check_password_hash(user.password, password):
            User.objects.raw({'username':{'$eq':username}}).delete()
        else:
            return serialzed({'message':'Not matched password'}, 401)
        return serialzed({'message':'delete user', 'username':username}, 201)
