from flask_restful import Resource
from flask import request
from db.models import StdDisc
from app import app
from util import write_log
from api.util import to_json
from constants import *
from task.htmlparser import regex_disc
import requests

class StdDiscAPI(Resource):
    def __init__(self):
        super(StdDiscAPI, self).__init__()

    def get(self, cntry=None, id=None):
        write_log(request.remote_addr,'std disc get',cntry)

        try:
            std_disc = StdDisc.objects.all()
        except:
            return {'list_std_disc':None}

        return {'list_std_disc':to_json(list(std_disc))}
    
    #update-task
    def put(self, cntry=None, id=None):
        pass
        
    #add-task
    def post(self, cntry=None, id=None):
        pass

    #delete-task
    def delete(self, cntry=None, id=None):
        pass
