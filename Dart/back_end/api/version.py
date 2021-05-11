from flask_restful import Resource
from flask import request
from db.models import Version
from app import app
from util import write_log
from api.util import to_json
from constants import *

class VersionAPI(Resource):
    def __init__(self):
        super(VersionAPI, self).__init__()

    def get(self):
        write_log(request.remote_addr,'VersionAPI get')
        print('get VersionAPI')

        soa = Version.objects.raw({}).first()

        return {'version':to_json(soa)}
    
    #update-task
    def put(self):
        pass
        
    #add-task
    def post(self):
        pass

    #delete-task
    def delete(self):
        pass
