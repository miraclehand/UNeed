from flask_restful import Resource
from flask import request
from datetime import datetime, timedelta
from db.models import NodePairKr, PickedPairKr, Classify
from task.xls import save_xls_picked_pair, reorganize_xls_picked_pair
from utils.datetime import to_yyyymmdd, add_year
from app import app
from api.util import get_xls
from task.singleton import pool_ohlcv
from task.pair import AbstractPairFactory
import requests

class NodePairAPI(Resource):
    def __init__(self):
        super(NodePairAPI, self).__init__()

    def get(self, cntry=None):
        #print('NodePairAPI', request.remote_addr)
        return {'items':[]}

    #update-task
    def put(self, cntry=None):
        print('NodePairAPI put', request.remote_addr)

        start = datetime.now()
        date2 = to_yyyymmdd(datetime.now().today())
        date1 = add_year(date2, -2)

        factory = AbstractPairFactory.get_factory(cntry)
        node_pair = factory.create_node_pair()

        node_pair.make_model(date1, date2)

        print('END NodePairAPI put', datetime.now() - start)

        return None

    #add-task
    def post(self, cntry=None):
        print('NodePairAPI post', request.remote_addr)
        return None

    #delete-task
    def delete(self, cntry=None):
        if cntry == 'kr': NodePair = NodePairKr
        if cntry == 'us': NodePair = NodePairUs
        NodePair.objects().delete()

class PickedPairAPI(Resource):
    def __init__(self):
        super(PickedPairAPI, self).__init__()

    def get(self, cntry=None):
        if app.config['HOSTNAME'] == 'hikey970':
            picked_pairs = get_xls(cntry, 'pair')
        else:
            url = app.config['URL_PAIR_HIKEY'] + '/api/pair/picked_pair/{}'
            picked_pairs=requests.get(url.format(cntry)).json()['picked_pairs']
        return {'picked_pairs':picked_pairs}, 201

    #update-task
    def put(self, cntry=None):
        print('PickedPairAPI put', request.remote_addr)

        start = datetime.now()

        date2 = to_yyyymmdd(datetime.now().today())
        date1 = add_year(date2, -2)

        factory = AbstractPairFactory.get_factory(cntry)
        picked_pair = factory.create_picked_pair()
        picked_pair.make_model(date1, date2)
        save_xls_picked_pair(cntry, date2, date2)
        reorganize_xls_picked_pair(cntry, date2)

        print('END PickedPairAPI put', datetime.now() - start)

        return None

    #add-task
    def post(self, cntry=None):
        print('PickedPairAPI post', request.remote_addr)

        date = to_yyyymmdd(datetime.now().today())

        #make_picked_pair_kr_model(date)
        return None

    #delete-task
    def delete(self, cntry=None):
        if cntry == 'kr': PickedPair = PickedPairKr
        if cntry == 'us': PickedPair = PickedPairUs
        PickedPair.objects().delete()
