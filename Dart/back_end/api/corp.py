from flask_restful import Resource
from flask import request
from db.models import Corp
from app import app
from util import write_log
from api.util import to_json
from constants import *
import requests, zipfile, io
import xml.etree.ElementTree as elemTree

def fetch_corps():
    print('fetch_corps')
    r = requests.get(DART_URL.format('corpCode.xml'))
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        z.extractall('data/')
    r.close()

    tree = elemTree.parse('data/CORPCODE.xml')

    corps = tree.findall('list')
    return corps

class CorpAPI(Resource):
    def __init__(self):
        super(CorpAPI, self).__init__()

    def get(self, cntry=None, id=None):
        write_log(request.remote_addr,'corp get',cntry)

    #update-task
    def put(self, cntry=None):
        write_log(request.remote_addr,'corp put',cntry)

        corps = fetch_corps()

        for corp in corps:
            try:
                corp=Corp.objects.get({'corp_code':corp.find('corp_code').text})
            except:
                Corp(corp).save()

    #add-task
    def post(self, cntry=None):
        write_log(request.remote_addr,'corp post',cntry)

        Corp.objects.delete()

        corps = fetch_corps()
        Corp.objects.bulk_create([Corp(corp) for corp in corps])

    #delete-task
    def delete(self, cntry=None):
        write_log(request.remote_addr,'corp delete',cntry)

        Corp.objects.delete()

