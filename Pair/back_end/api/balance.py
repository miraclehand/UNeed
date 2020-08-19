import math
from flask_restful import Resource
from flask import request
from bson import ObjectId
from datetime import datetime
from db.models import Asset
from task.strategy import AbstractStrategyFactory
from api.util import login_required, serialzed, to_json
from app import app
from constants import *

class AssetAPI(Resource):
    def __init__(self):
        super(AssetAPI, self).__init__()

    @login_required
    def get(self, id=None):
        print('AssetAPI')

        try:
            asset = Asset.objects.get({'username':id})
        except:
            return serialzed({'message':'Not exist [%s]' % username}, 401)

        return {'username':id, 'asset':to_json(asset)}, 201

    #update-task
    @login_required
    def put(self, id=None):
        print('AssetAPI put')

        data = request.get_json()
        username = data["username"]
        budget   = data["budget"]

        try:
            asset = Asset.objects.get({'username':username})
            asset.budget = budget
            asset.save()
        except:
            return serialzed({'message':'Not exist [%s]' % username}, 401)
        return {'username':id, 'asset':to_json(asset)}, 201

    #add-task
    @login_required
    def post(self, id=None):
        print('AssetAPI post')

        data = request.get_json()
        username = data["username"]
        budget   = data["budget"]
        try:
            asset = Asset.objects.get({'username':username})
            return serialzed({'message':'exist user:[%s]' % username}, 401)
        except:
            pass
        asset = Asset(username=username, budget=budget)
        asset.save()

        return {'username':id, 'asset':to_json(asset)}, 201

    #delete-task
    @login_required
    def delete(self, id=None):
        print('AssetAPI DELETE')

        data = request.get_json()
        username = data['username']

        try:
            asset = Asset.objects.get({'username':username})
            Asset.objects.raw({'username':username}).delete()
        except:
            return serialzed({'message':'Not exist [%s]' % username}, 401)
        return serialzed({'message':'delete balance', 'username':username}, 201)


