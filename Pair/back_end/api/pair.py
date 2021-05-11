from flask_restful import Resource
from flask import request
from datetime import datetime, timedelta
from db.models import NodePairKr, PickedPairKr, Classify
from task.xls import save_xls_picked_pair, reorganize_xls_picked_pair
from commons.celery.tasks import put_node_pair, put_picked_pair
from commons.utils.datetime import to_yyyymmdd, add_year
from commons.utils.log import write_log
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
        write_log(request.remote_addr,'node put',cntry)
        print('NodePairAPI put', request.remote_addr)

        put_node_pair.delay(cntry)
        """
        start = datetime.now()
        date = to_yyyymmdd(datetime.now().today())

        factory = AbstractPairFactory.get_factory(cntry)
        node_pair = factory.create_node_pair()

        node_pair.make_model(date)

        print('END NodePairAPI put', datetime.now() - start)
        """
        return None

    #add-task
    def post(self, cntry=None):
        write_log(request.remote_addr,'node post',cntry)
        print('NodePairAPI post', request.remote_addr)
        return None

    #delete-task
    def delete(self, cntry=None):
        write_log(request.remote_addr,'node delete',cntry)

        if cntry == 'kr': NodePair = NodePairKr
        if cntry == 'us': NodePair = NodePairUs
        NodePair.objects().delete()

class PickedPairAPI(Resource):
    def __init__(self):
        super(PickedPairAPI, self).__init__()

    def get(self, cntry=None):
        if app.config['HOSTNAME'] == 'hikey970':
            picked_pairs = get_xls(cntry, 'pair')
        return {'picked_pairs':picked_pairs}, 201

    #update-task
    def put(self, cntry=None):
        write_log(request.remote_addr,'pair put',cntry)
        print('PickedPairAPI put', request.remote_addr)

        put_picked_pair.delay(cntry)
        """
        start = datetime.now()

        factory = AbstractPairFactory.get_factory(cntry)
        picked_pair = factory.create_picked_pair()
        date, cnt = picked_pair.make_model()
        save_xls_picked_pair(cntry, date, date)
        reorganize_xls_picked_pair(cntry, date)

        print('END PickedPairAPI put', datetime.now() - start)
        """

        return None

    #add-task
    def post(self, cntry=None):
        write_log(request.remote_addr,'pair post',cntry)
        print('PickedPairAPI post', request.remote_addr)

        date = to_yyyymmdd(datetime.now().today())

        #make_picked_pair_kr_model(date)
        return None

    #delete-task
    def delete(self, cntry=None):
        write_log(request.remote_addr,'pair delete',cntry)

        if cntry == 'kr': PickedPair = PickedPairKr
        if cntry == 'us': PickedPair = PickedPairUs
        PickedPair.objects().delete()
