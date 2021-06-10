import os
import sys
sys.path.append('../../')
sys.path.append(os.path.dirname(__file__))

from commons.basedb.models import Ohlcv, StockKr, CandleKr, StockUs, CandleUs
from datetime import datetime
from dateutil.relativedelta import relativedelta
from task.crawler import AbstractCrawlFactory

def upsert_stock(cntry):
    if cntry == 'kr': Stock, Candle = StockKr, CandleKr
    if cntry == 'us': Stock, Candle = StockUs, CandleUs

    today = datetime.today()
    today = datetime(today.year, today.month, today.day)
    bf_month = today-relativedelta(months=2)

    factory = AbstractCrawlFactory.get_factory(cntry)
    crawl_stock = factory.create_crawl_stock()
    stock_pages = crawl_stock.scrapy()
    crawl_stock.upsert(Stock, Candle, stock_pages)
    Stock.objects.raw({'lastFetched':{'$lt':bf_month}}).update({'$set':{'crud':'D'}})

def insert_stock(cntry):
    if cntry == 'kr': Stock = StockKr
    if cntry == 'us': Stock = StockUs

    Stock.objects.delete()

    factory = AbstractCrawlFactory.get_factory(cntry)
    crawl_stock = factory.create_crawl_stock()
    stock_pages = crawl_stock.scrapy()
    crawl_stock.save(Stock, stock_pages)

def delete_stock(cntry):
    if cntry == 'kr': Stock = StockKr
    if cntry == 'us': Stock = StockUs

    Stock.objects.delete()

def upsert_candle(cntry, code=None):
    if cntry == 'kr': Stock, Candle = StockKr, CandleKr
    if cntry == 'us': Stock, Candle = StockUs, CandleUs

    factory = AbstractCrawlFactory.get_factory(cntry)
    crawl_candle = factory.create_crawl_candle()

    if code:
        codes=[stock.code for stock in Stock.objects.raw({'code':code})]
    else:
        codes=[stock.code for stock in Stock.objects.order_by([('capital',-1)])]

    #국내주식3000개, 미국주식7000개,
    #미국주식은 데이터 받다가 거부 당함. 그래서 시총기준 5000개만 받음
    codes = codes[:5000]

    n = 100
    days = 14 # 2weeks
    for i in range(0, codes.__len__(), n):
        print('page', i, n, codes.__len__())
        crawl_candle.setup(codes[i:i+n], days)
        ohlcv_pages = crawl_candle.scrapy()
        crawl_candle.upsert(Stock, Candle, ohlcv_pages)
    # 권리 때문에, 과거의 수정주가가 바뀌는 경우가 있으면
    # 과거 주가를 다시 받아야한다
    codes = [stock.code for stock in Stock.objects.raw({'new_adj_close':True})]
    for i, code in enumerate(codes):
        print(i, codes.__len__(), code)
        insert_candle(cntry, code)
        Stock.objects.raw({'code':code}).update({'$set':{'new_adj_close':False}})

    return None
    url = app.config['URL_PAIR'] + '/api/pair/picked_pair/{}'
    requests.put(url.format(cntry))

def insert_candle(cntry, code=None):
    if cntry == 'kr': Stock, Candle = StockKr, CandleKr
    if cntry == 'us': Stock, Candle = StockUs, CandleUs

    if code:
        Candle.objects.raw({'code':code}).delete()
        codes=[stock.code for stock in Stock.objects.raw({'code':code})]
    else:
        Candle.objects.delete()
        codes=[stock.code for stock in Stock.objects.order_by([('capital',-1)])]

    #국내주식3000개, 미국주식7000개,
    #미국주식은 데이터 받다가 거부 당함. 그래서 시총기준 5000개만 받음
    codes = codes[:5000]

    factory = AbstractCrawlFactory.get_factory(cntry)
    crawl_candle = factory.create_crawl_candle()

    n = 100
    days = 3650 # 10years
    for i in range(0, codes.__len__(), n):
        print('page', i)
        crawl_candle.setup(codes[i:i+n], days)
        ohlcv_pages = crawl_candle.scrapy()
        crawl_candle.save(Stock, Candle, ohlcv_pages)

def delete_candle(cntry):
    if cntry == 'kr': Stock, Candle = StockKr, CandleKr
    if cntry == 'us': Stock, Candle = StockUs, CandleUs

    Candle.objects.delete()

def reqest_company(cntry, code):
    factory = AbstractCrawlFactory.get_factory(cntry)
    crawl_company = factory.create_crawl_company()
    crawl_company.setup(code)
    company = crawl_company.scrapy()
    print(company)

if __name__ == '__main__':
    #upsert_stock('us')
    #insert_stock('us')
    #upsert_candle('kr')
    #insert_candle('kr')
    #upsert_candle('us')
    insert_candle('us')
    #reqest_company('kr', '152330')

