from flask_restful import Resource
from flask import request, Response
from bson import ObjectId
from datetime import datetime
from utils.log import write_log
from api.util import login_required, to_json, res_error
from api.util import get_xls
from db.models import StockKr, StrainerKr, TradingReportKr, SimulaReportKr
from db.models import StockUs, StrainerUs, TradingReportUs, SimulaReportUs
from task.xls import save_xls_simula_lastest
from task.strategy import AbstractStrategyFactory
from task.singleton import pool_variant

#import objgraph

class StrainerAPI(Resource):
    def __init__(self):
        super(StrainerAPI, self).__init__()

    @login_required
    def get(self, cntry=None, id=None):
        if cntry == 'kr': Strainer = StrainerKr
        if cntry == 'us': Strainer = StrainerUs

        strainers = Strainer.objects.raw({'username':{'$eq':id}})

        return {'username':id, 'strainers':[to_json(list(strainers)),]}, 201

    @login_required
    def post(self, cntry=None, id=None):
        if cntry == 'kr': Strainer = StrainerKr
        if cntry == 'us': Strainer = StrainerUs

        strainer = request.get_json()['strainer']

        write_log(request.remote_addr,'strainer post', cntry, data)

        if not data['name']:
            return res_error('[name] is requried', 403)

        strainer = Strainer(id, strainer).save()

        strainers = Strainer.objects.raw({'username':{'$eq':id}})

        return {'username':id, 'strainers':[to_json(list(strainers)),]}, 201

    @login_required
    def delete(self, cntry=None, id=None):
        data = request.get_json()
        strainer = data['strainer']

        write_log(request.remote_addr,'strainer delete', cntry, strainer)

        if not strainer['name']:
            return res_error('[name] is requried', 403)

        if cntry == 'kr': Strainer = StrainerKr
        if cntry == 'us': Strainer = StrainerUs

        Strainer.objects.raw({'_id':ObjectId(strainer['_id'])}).delete()

        strainers = Strainer.objects.raw({'username':{'$eq':id}})

        return {'username':id, 'strainers':[to_json(list(strainers)),]}, 201

class TradingReportAPI(Resource):
    def __init__(self):
        super(TradingReportAPI, self).__init__()

    @login_required
    def get(self, cntry=None, id=None):
        factory = AbstractStrategyFactory.get_factory(cntry)
        report = factory.create_trading_report()
        report.setup(id)
        #report = report.get_last_report()

        if not report:
            return {}, 404
        entries = report.get_open_entries()

        return {'username':id, 'entries':to_json(list(entries))}, 201

    #add-task
    @login_required
    def post(self, cntry=None, id=None):
        data = request.get_json()

        code1 = data['code1']
        date1 = data['date1']
        pos1  = data['pos1']
        uv1   = data['uv1']
        qty1  = data['qty1']

        code2 = data['code2']
        date2 = data['date2']
        pos2  = data['pos2']
        uv2   = data['uv2']
        qty2  = data['qty2']

        write_log(request.remote_addr,'trading post', code1, code2)

        factory = AbstractStrategyFactory.get_factory(cntry)
        report = factory.create_trading_report()
        report.setup(id)

        basket1 = report.new_basket(code1, pos1, date1, uv1, qty1)
        basket2 = report.new_basket(code2, pos2, date2, uv2, qty2)
        report.open_entry(basket1, basket2)

        entries = report.get_open_entries()

        return {'username':id, 'entries':to_json(list(entries))}, 201

    #delete-task
    @login_required
    def delete(self, cntry=None, id=None):
        data = request.get_json()
        entry_id = data['entry_id']

        write_log(request.remote_addr,'trading delete', entry_id)

        factory = AbstractStrategyFactory.get_factory(cntry)
        report = factory.create_trading_report()
        report.setup(id)
        report.close_entry(entry_id, 0, 0)

        entries = report.get_open_entries()

        return {'username':id, 'entries':to_json(list(entries))}, 201

class ProgressAPI(Resource):
    def __init__(self):
        super(ProgressAPI, self).__init__()

    @login_required
    def get(self, cntry=None, id=None):
        today = datetime.today().date()
        date = datetime(year=today.year, month=today.month, day=today.day)

        factory = AbstractStrategyFactory.get_factory(cntry)
        simula_report = factory.create_simula_report()
        simula_report.setup(id)

        report = simula_report.get_last_report()

        seconds = 0
        progress = 100

        if report and report.valid and report.create_date == date:
            seconds  = report.seconds
            progress = report.progress

        return {'username':id, 'seconds':seconds, 'progress':progress}, 201

    @login_required
    def delete(self, cntry=None, id=None):
        factory = AbstractStrategyFactory.get_factory(cntry)
        simula_report = factory.create_simula_report()
        simula_report.setup(id)
        report = simula_report.get_last_report()

        seconds = 0
        progress = 100

        if report:
            seconds = report.seconds
        pool_variant.set('simula_valid', False)
        return {'username':id, 'seconds':seconds, 'progress':progress}, 201

class SimulaReportAPI(Resource):
    def __init__(self):
        super(SimulaReportAPI, self).__init__()

    @login_required
    def get(self, cntry=None, id=None):
        simulas = get_xls('simula')
        return {'username':id, 'simulas':[simulas,]}, 201

    #add-task
    @login_required
    def post(self, cntry=None, id=None):
        if cntry == 'kr': Strainer = StrainerKr
        if cntry == 'us': Strainer = StrainerUs

        data = request.get_json()

        date1 = data['date1']
        date2 = data['date2']

        today = datetime.today().date()
        date  = datetime(year=today.year, month=today.month, day=today.day)

        write_log(request.remote_addr,'simula post', data)

        if not date1 or not date2:
            return res_error('[date1], [date2] are requried', 403)

        strainer = Strainer(id, data['strainer'])
        factory = AbstractStrategyFactory.get_factory(cntry)
        simula_report = factory.create_simula_report()
        simula_report.setup(id)
        simula_report.set_strainer(strainer)

        report = simula_report.get_last_report()
        if report and report.valid:
            if report.create_date == date and report.progress < 100:
                return res_error('Simulation already running...', 403)

        simula_report.play(date1, date2)

        today = datetime.today().date()
        date = datetime(year=today.year, month=today.month, day=today.day)
        save_xls_simula_lastest(date)

        simulas = get_xls('simula')
        return {'username':id, 'simulas':[simulas,]}, 201


