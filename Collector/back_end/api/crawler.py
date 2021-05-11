import sys
import numpy as np
import requests
from flask_restful import Resource
from flask import request
from datetime import date, datetime
from app import app
from api.util import to_json
from task.crawler import AbstractCrawlFactory
from commons.celery.tasks import post_stock, put_stock, del_stock
from commons.celery.tasks import post_candle, put_candle, del_candle
from commons.utils.log import write_log
from commons.basedb.models import Ohlcv, StockKr, CandleKr, StockUs, CandleUs
from commons.utils.datetime import str_to_datetime

class StockAPI(Resource):
    def __init__(self):
        super(StockAPI, self).__init__()

    def get(self, cntry=None, id=None):
        write_log(request.remote_addr,'stock get',cntry, id)

        print('StockAPI get')
        if cntry == 'kr': stocks = StockKr.objects.raw({'crud':{'$ne':'D'}})
        if cntry == 'us': stocks = StockUs.objects.raw({'crud':{'$ne':'D'}})

        if id:
            #dt = str_to_datetime(id,  '%Y%m%d')
            #stocks = stocks.raw({'lastUpdated': {'$gt':dt}})
            stocks = stocks.get({'code':id})
        else:
            stocks = list(stocks)

        return {'stocks':to_json(stocks)}

    #update-task
    def put(self, cntry=None):
        write_log(request.remote_addr,'stock put',cntry)

        put_stock.delay(cntry)

        return {'task':'stock put'}, 201

    #add-task
    def post(self, cntry=None):
        write_log(request.remote_addr,'stock post',cntry)

        post_stock.delay(cntry)

        return {'task':'stock post'}, 201

    #delete-task
    def delete(self, cntry=None):
        write_log(request.remote_addr,'stock delete',cntry)

        del_stock.delay(cntry)

        return {'task':'stock delete'}, 201

class CandleAPI(Resource):
    def __init__(self):
        super(CandleAPI, self).__init__()

    def get(self, cntry=None, id=None, date1=None, date2=None):
        write_log(request.remote_addr,'candle get',cntry, id, date1, date2)

        if not id:
            return {'candle': 'None'}

        if cntry == 'kr': candle = CandleKr.objects.get({'code':id})
        if cntry == 'us': candle = CandleUs.objects.get({'code':id})

        return {'candle':to_json(candle.to_dict)}

    #update-task
    def put(self, cntry=None, id=None):
        print('put candle', cntry, id)
        write_log(request.remote_addr,'candle put',cntry, id)

        put_candle.delay(cntry, id)

        return {'task':'candle put'}, 201
    #add-task
    def post(self, cntry=None, id=None):
        write_log(request.remote_addr,'candle post',cntry, id)

        post_candle.delay(cntry, id)

        return {'task':'candle post'}, 201

    #delete-task
    def delete(self, cntry=None, id=None):
        write_log(request.remote_addr,'candle delete',cntry, id)

        del_candle.delay(cntry, id)

        return {'task':'candle delete'}, 201

class CompanyAPI(Resource):
    def __init__(self):
        super(CompanyAPI, self).__init__()

    def get(self, cntry=None, id=None):
        write_log(request.remote_addr,'company get',cntry,id)

        factory = AbstractCrawlFactory.get_factory(cntry)

        crawl_company = factory.create_crawl_company()
        crawl_company.setup(id)
        company = crawl_company.scrapy()

        return {'company':company}, 201

    #update-task
    def put(self, cntry=None, id=None):
        write_log(request.remote_addr,'company put',cntry,id)

    #add-task
    def post(self, cntry=None, id=None):
        write_log(request.remote_addr,'company post',cntry,id)

    #delete-task
    def delete(self, cntry=None):
        write_log(request.remote_addr,'company delete',cntry)

class TickAPI(Resource):
    def __init__(self):
        super(TickAPI, self).__init__()

    def get(self, cntry=None, id=None):
        if cntry == 'kr': Candle = CandleKr
        if cntry == 'us': Candle = CandleUs

        ohlcv = Candle.objects.get({'code':id}).ohlcvs[-1]
            
        if date.today() == ohlcv.date.date():
            tick = ohlcv.close
        else:
            factory = AbstractCrawlFactory.get_factory(cntry)
            crawl_tick = factory.create_crawl_tick()
            ohlcv = crawl_tick.scrapy(id)
            tick = ohlcv['close']

        return {'tick':{id:tick}}, 201

    #update-task
    def put(self, id=None):
        print('TickAPI put', request.remote_addr)

    #add-task
    def post(self):
        print('TickAPI post', request.remote_addr)

    #delete-task
    def delete(self):
        print('TickAPI delete', request.remote_addr)

