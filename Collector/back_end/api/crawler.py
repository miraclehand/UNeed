import sys
import numpy as np
import requests
from flask_restful import Resource
from flask import request
from datetime import date, datetime
from app import app
from utils.log import write_log
from api.util import to_json
from task.crawler import AbstractCrawlFactory
from basedb.models import Ohlcv, StockKr, CandleKr, StockUs, CandleUs

class StockAPI(Resource):
    def __init__(self):
        super(StockAPI, self).__init__()

    def get(self, cntry=None, id=None):
        if cntry == 'kr': stocks = StockKr.objects.all()
        if cntry == 'us': stocks = StockUs.objects.all()

        if id:
            stocks = stocks.get({'code':id})
        else:
            stocks = list(stocks)

        return {'stocks':to_json(stocks)}

    #update-task
    def put(self, cntry=None):
        if cntry == 'kr': Stock, Candle = StockKr, CandleKr
        if cntry == 'us': Stock, Candle = StockUs, CandleUs
        today = datetime.today()
        today = datetime(today.year, today.month, today.day)

        factory = AbstractCrawlFactory.get_factory(cntry)
        crawl_stock = factory.create_crawl_stock()
        stock_pages = crawl_stock.scrapy()
        crawl_stock.upsert(Stock, Candle, stock_pages)
        Stock.objects.raw({'lastModified':{'$ne':today}}).delete()

        return {'task':'stock put'}, 201

    #add-task
    def post(self, cntry=None):
        if cntry == 'kr': Stock = StockKr
        if cntry == 'us': Stock = StockUs

        Stock.objects.delete()

        factory = AbstractCrawlFactory.get_factory(cntry)
        crawl_stock = factory.create_crawl_stock()
        stock_pages = crawl_stock.scrapy()
        crawl_stock.save(Stock, stock_pages)

        return {'task':'stock post'}, 201

    #delete-task
    def delete(self, cntry=None):
        if cntry == 'kr': Stock = StockKr
        if cntry == 'us': Stock = StockUs

        Stock.objects.delete()

class CandleAPI(Resource):
    def __init__(self):
        super(CandleAPI, self).__init__()

    def get(self, cntry=None, id=None, date1=None, date2=None):
        if not id:
            return {'candle': 'None'}

        if cntry == 'kr': candle = CandleKr.objects.get({'code':id})
        if cntry == 'us': candle = CandleUs.objects.get({'code':id})
        return {'candle':to_json(candle.to_dict)}

    #update-task
    def put(self, cntry=None, id=None):
        if cntry == 'kr': Stock, Candle = StockKr, CandleKr
        if cntry == 'us': Stock, Candle = StockUs, CandleUs

        factory = AbstractCrawlFactory.get_factory(cntry)
        crawl_candle = factory.create_crawl_candle()

        codes=[stock.code for stock in Stock.objects.order_by([('capital',-1)])]

        #국내주식3000개, 미국주식7000개,
        #미국주식은 데이터 받다가 거부 당함. 그래서 시총기준 5000개만 받음
        codes = codes[:5000]

        n = 100
        days = 10 # 2weeks
        for i in range(0, codes.__len__(), n):
            print('page', i)
            crawl_candle.setup(codes[i:i+n], days)
            ohlcv_pages = crawl_candle.scrapy()
            crawl_candle.upsert(Stock, Candle, ohlcv_pages)

        # 권리 때문에, 과거의 수정주가가 바뀌는 경우가 있으면
        # 과거 주가를 다시 받아야한다
        codes = [stock.code for stock in Stock.objects.raw({'new_adj_close':True})]
        url = app.config['URL_COLLECTOR'] + '/api/crawler/candle/{}/{}'
        for code in codes:
            requests.post(url.format(cntry, code))

        url = app.config['URL_PAIR'] + '/api/pair/picked_pair/{}'
        requests.put(url.format(cntry))
        return None

    #add-task
    def post(self, cntry=None, id=None):
        if cntry == 'kr': Stock, Candle = StockKr, CandleKr
        if cntry == 'us': Stock, Candle = StockUs, CandleUs

        if id:
            Candle.objects.raw({'code':id}).delete()
            codes = [stock.code for stock in Stock.objects.raw({'code':id})]
        else:
            Candle.objects.delete()
            codes = [stock.code for stock in Stock.objects.order_by([('capital',-1)])]

        #국내주식3000개, 미국주식7000개,
        #미국주식은 데이터 받다가 거부 당함. 그래서 시총기준 5000개만 받음
        codes = codes[:5000]

        factory = AbstractCrawlFactory.get_factory(cntry)
        crawl_candle = factory.create_crawl_candle()

        n = 100
        days = 2500 # 10years
        for i in range(0, codes.__len__(), n):
            print('page', i)
            crawl_candle.setup(codes[i:i+n], days)
            ohlcv_pages = crawl_candle.scrapy()
            crawl_candle.save(Stock, Candle, ohlcv_pages)

        return {'task':'candle post'}, 201

    #delete-task
    def delete(self, cntry=None, id=None):
        if cntry == 'kr': Stock, Candle = StockKr, CandleKr
        if cntry == 'us': Stock, Candle = StockUs, CandleUs

        Candle.objects.delete()

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
            crawl_tick.setup(id)
            ohlcv = crawl_tick.scrapy()
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

