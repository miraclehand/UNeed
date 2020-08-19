from flask_restful import Resource
from flask import request
from utils.log import write_log
from api.util import login_required
from task.chart import AbstractChartFactory
#import objgraph

class NormChartAPI(Resource):
    def __init__(self):
        super(NormChartAPI, self).__init__()

    @login_required
    def get(self, cntry=None):
        code1 = request.args.get('code1')
        code2 = request.args.get('code2')
        date1 = request.args.get('date1')
        date2 = request.args.get('date2')

        write_log(request.remote_addr,'norm_chart get',code1,code2,date1,date2)

        if not code1 or not code2 or not date1 or not date2:
            return {'url_img':None, 'corr':None}, 403

        factory = AbstractChartFactory.get_factory(cntry)
        norm_chart = factory.create_norm_chart()
        url = norm_chart.draw_chart(date1, date2, code1, code2)

        return {'img_src':url}, 201

    #update-task
    def put(self):
        pass

    #add-task
    def post(self):
        pass

    #delete-task
    def delete(self):
        pass

class LogChartAPI(Resource):
    def __init__(self):
        super(LogChartAPI, self).__init__()

    @login_required
    def get(self, cntry=None):
        code1 = request.args.get('code1')
        code2 = request.args.get('code2')
        date1 = request.args.get('date1')
        date2 = request.args.get('date2')

        write_log(request.remote_addr,'log_chart get',code1,code2,date1,date2)

        if not code1 or not code2 or not date1 or not date2:
            return {'url_img':None, 'corr':None}, 403

        factory = AbstractChartFactory.get_factory(cntry)
        log_chart = factory.create_log_chart()
        url = log_chart.draw_chart(date1, date2, code1, code2)

        return {'img_src':url}, 201

    #update-task
    def put(self):
        pass

    #add-task
    def post(self):
        pass

    #delete-task
    def delete(self):
        pass

class HistChartAPI(Resource):
    def __init__(self):
        super(HistChartAPI, self).__init__()

    @login_required
    def get(self, cntry=None):
        code1 = request.args.get('code1')
        code2 = request.args.get('code2')
        date1 = request.args.get('date1')
        date2 = request.args.get('date2')

        write_log(request.remote_addr,'hist_chart get',code1,code2,date1,date2)

        if not code1 or not code2 or not date1 or not date2:
            return {'url_img':None, 'histogram':None}, 201

        factory = AbstractChartFactory.get_factory(cntry)
        hist_chart = factory.create_hist_chart()
        url = hist_chart.draw_chart(date1, date2, code1, code2)

        return {'img_src':url}, 201

    #update-task
    def put(self):
        pass

    #add-task
    def post(self):
        pass

    #delete-task
    def delete(self):
        pass

class VolChartAPI(Resource):
    def __init__(self):
        super(VolChartAPI, self).__init__()

    @login_required
    def get(self, cntry=None):
        code1 = request.args.get('code1')
        code2 = request.args.get('code2')
        date1 = request.args.get('date1')
        date2 = request.args.get('date2')

        write_log(request.remote_addr,'vol_chart get',code1,code2,date1,date2)

        if not code1 or not code2 or not date1 or not date2:
            return {'url_img':None, 'corr':None}, 403

        factory = AbstractChartFactory.get_factory(cntry)
        vol_chart = factory.create_vol_chart()
        url = vol_chart.draw_chart(date1, date2, code1, code2)

        return {'img_src':url}, 201

    #update-task
    def put(self):
        pass

    #add-task
    def post(self):
        pass

    #delete-task
    def delete(self):
        pass
