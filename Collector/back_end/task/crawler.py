import sys
import aiohttp
import asyncio
import requests
import abc
import pandas as pd
import numpy as np
import yfinance as yf
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from task.htmlparser import AbstractParserFactory
from commons.basedb.models import Ohlcv, StockKr, CandleKr, StockUs, CandleUs
from commons.utils.search import getDisassembled
from commons.utils.parser import get_value
from commons.utils.datetime import datetime_to_str

def get_p_close(code, date, Candle):
    candle = Candle.objects.raw({'code':code})
    if candle.count() == 0:
        return 0

    ohlcvs = candle.first().ohlcvs
    if ohlcvs.__len__() <= 0:
        return 0

    idx = 0
    for i, ohlcv in enumerate(ohlcvs):
        if ohlcv.date == date:
            idx = i
            break

    if idx <= 0:
        return 0
    return ohlcvs[idx - 1].close

def cal_diff_ohlcvs(code, Candle, ohlcvs):
    p_close = None
    for i, ohlcv in enumerate(ohlcvs):
        if p_close is None:
            p_close = get_p_close(code, ohlcv['date'], Candle)

        diff   = ohlcv['close'] - p_close
        change = diff / p_close * 100 if p_close != 0 else 0
        ohlcv['diff']   = diff
        ohlcv['change'] = change
        ohlcvs[i] = ohlcv

        p_close = ohlcv['close']
    return ohlcvs

"""
def get_ohlcvs(code, Candle, ohlcvs):
    p_close = None
    for i, ohlcv in enumerate(ohlcvs):
        if p_close is None:
            p_close = get_p_close(code, ohlcv['date'], Candle)

        diff   = ohlcv['close'] - p_close
        change = diff / p_close * 100 if p_close != 0 else 0
        ohlcv['diff']   = diff
        ohlcv['change'] = change
        ohlcvs[i] = ohlcv

        p_close = ohlcv['close']
    return [Ohlcv(ohlcv['date'], ohlcv) for ohlcv in ohlcvs]
"""

# Abstract Factory Pattern
#AbstractFactory
class AbstractCrawlFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_crawl_stock(self):
        pass

    @abc.abstractmethod
    def create_crawl_candle(self):
        pass

    @abc.abstractmethod
    def create_crawl_company(self):
        pass

    @abc.abstractmethod
    def create_crawl_tick(self):
        pass

    @classmethod
    def get_factory(self, cntry):
        if cntry == 'kr':
            return ConcreteCrawlKrFactory()
        if cntry == 'us':
            return ConcreteCrawlUsFactory()
        return None

#ConcreteFactory1
class ConcreteCrawlKrFactory(AbstractCrawlFactory):
    def create_crawl_stock(self):
        return ConcreteProductCrawlStockKr()

    def create_crawl_candle(self):
        return ConcreteProductCrawlCandleKr()

    def create_crawl_company(self):
        return ConcreteProductCrawlCompanyKr()

    def create_crawl_tick(self):
        return ConcreteProductCrawlTickKr()

#ConcreteFactory2
class ConcreteCrawlUsFactory(AbstractCrawlFactory):
    def create_crawl_stock(self):
        return ConcreteProductCrawlStockUs()

    def create_crawl_candle(self):
        return ConcreteProductCrawlCandleUs()

    def create_crawl_company(self):
        return ConcreteProductCrawlCompanyUs()

    def create_crawl_tick(self):
        return ConcreteProductCrawlTickUs()

class AbstractProductCrawl(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def scrapy(self):
        pass

#AbstractProductA
class AbstractProductCrawlStock(AbstractProductCrawl):
    parser = None

    def __init__(self, parser, **kwargs):
        super().__init__(**kwargs)
        self.parser = parser

    @abc.abstractmethod
    def scrapy(self):
        pass

    @abc.abstractmethod
    def save(self, Stock, stock_pages):
        for stocks in stock_pages:
            if not stocks:
                continue
            Stock.objects.bulk_create([Stock(stock) for stock in stocks])

    @abc.abstractmethod
    def upsert(self, Stock, Candle, stock_pages):
        today = datetime.today()
        today = datetime(today.year, today.month, today.day)
        for stocks in stock_pages:
            if not stocks:
                continue
            for stock in stocks:
                Stock.objects.raw({'code': stock['code']}).update({
                    '$set': {'cntry'   : stock['cntry'],
                             'name'    : stock['name'],
                             'dname'   : stock['dname'],
                             'label'   : stock['label'],
                             'exchange': stock['exchange'],
                             'parent'  : stock['parent'],
                             'sector'  : stock['sector'],
                             'industry': stock['industry'],
                             'aimed'   : stock['aimed'],
                             'capital' : stock['capital'],
                             'lastFetched' : today,
                    }
                }, upsert=True)

                candle = Candle.objects.raw({'code':stock['code']})

                if candle.count() > 0:
                    #Update Stock
                    ohlcvs  = candle.first().ohlcvs[-50:]
                    avg_v50 = np.average([o.close * o.volume for o in ohlcvs])

                    Stock.objects.raw({
                        'code':stock['code'],
                        'avg_v50':{'$ne':avg_v50}}
                    ).update({
                        '$set':{'crud'   : 'U',
                                'avg_v50': avg_v50,
                                'lastUpdated': today}})
                else:
                    #Create Stock
                    Stock.objects.raw({'code': stock['code']}).update({
                        '$set': {'crud'   : 'C',
                                 'avg_v50': 0,
                                 'lastUpdated': today,
                        }
                    })

#ConcreteProductA
class ConcreteProductCrawlStockKr(AbstractProductCrawlStock):
    parent_pages = None

    def __init__(self, **kwargs):
        factory = AbstractParserFactory.get_factory('kr')
        parser = factory.create_parser()

        super().__init__(parser, **kwargs)

    async def async_fetch_parents(self, url):
        parents = dict()

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await asyncio.sleep(.1)
                html = await response.read()
                html = html.decode('euc-kr', 'ignore')

                key, value = self.parser.regex_parents(html)
                parents[key] = value
        return parents

    def fetch_parent_pages(self):
        print('fetch_parent_pages')
        if self.parent_pages is not None:
            return

        url = 'https://finance.naver.com/sise/sise_group.nhn?type=group'
        response = requests.get(url)
        group_no = self.parser.regex_group_no(response.text)

        url = 'https://finance.naver.com/sise/sise_group_detail.nhn?type=group&no={no}'
        pg_url = [url.format(no=no) for no in group_no]

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        tasks = [asyncio.ensure_future(self.async_fetch_parents(url)) for url in pg_url]
        self.parent_pages=event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()

    def find_parent(self, code):
        code = '{}0'.format(code[0:5])
        for parents in self.parent_pages:
            parent = [key for key in parents.keys()][0]
            for value in parents.values():
                if code in value.keys():
                    return parent
        return 'N/A'
        
    async def async_fetch_stocks(self, url):
        stocks = list()
        exchange = self.parser.regex_exchange(url)
        u = 'https://finance.naver.com/item/main.nhn?code={}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await asyncio.sleep(.1)
                html = await response.read()
                html = html.decode('euc-kr', 'ignore')

                codes = self.parser.regex_stocks(html)
                for code in codes:
                    if not code: continue
                    print(url, code[0], code[1])
                    async with aiohttp.ClientSession() as session:
                        async with session.get(u.format(code[0])) as response:
                            await asyncio.sleep(.1)
                            html = await response.read()
                            html = html.decode('euc-kr', 'ignore')
                            detail = self.parser.regex_stock_detail(html)
                            stock = {'cntry'   :'kr',
                                     'code'    :code[0],
                                     'name'    :code[1],
                                     'dname'   :getDisassembled(code[1]),
                                     'label'   :code[0] + ' ' + code[1],
                                     'exchange':exchange,
                                     'aimed'   :detail['aimed'],
                                     'sector'  :detail['sector'],
                                     'industry':detail['industry'],
                                     'capital' :detail['capital'],
                                     'parent'  :self.find_parent(code[0]),
                                     'avg_v50' :0,  #candle 데이터로 나중에 저장
                            }
                            stocks.append(stock)
        return stocks

    def scrapy(self):
        self.fetch_parent_pages()

        stock_pages = list()
        url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok={sosok}&page={page}'
        pg_url = [url.format(sosok=sosok,page=page) for sosok in ['0','1'] for page in range(1,40)]

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        tasks =[asyncio.ensure_future(self.async_fetch_stocks(url)) for url in pg_url]
        stock_pages = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()
        return stock_pages

    def save(self, Stock, stock_pages):
        super().save(Stock, stock_pages)

    def upsert(self, Stock, Candle, stock_pages):
        super().upsert(Stock, Candle, stock_pages)

#ConcreteProductB
class ConcreteProductCrawlStockUs(AbstractProductCrawlStock):
    headers = {
        "Accept-Language":"en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
        "Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0"
    }

    def __init__(self, **kwargs):
        factory = AbstractParserFactory.get_factory('us')
        parser = factory.create_parser()

        super().__init__(parser, **kwargs)

    async def async_fetch_stocks(self, url):
        stocks = list()
        for i in range(1, 5):
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url) as response:
                    await asyncio.sleep(.1)
                    html = await response.read()
                    html = html.decode('euc-kr', 'ignore')

                    self.parser.regex_exchange(url)
                    stocks = self.parser.regex_stocks(html)

                    print(url, stocks.__len__())

                    if stocks.__len__() == 0:
                          # finviz에서 데이터를 넘겨주지 않았음. 1초후 재요청
                        await asyncio.sleep(1)
                    elif stocks.__len__() == 1:
                          # finviz에서는 1건이 나온다는건 마지막이라는 뜻
                        break
                    else:
                        break
        return stocks

    def scrapy(self):
        stock_pages = list()

        url = 'https://finviz.com/screener.ashx?v=111&f={exchange}&o=-marketcap&r={page}'
        step = 20
        for i in range(1, 4000, step):
            pg_url = [url.format(exchange=exchange,page=page) for exchange in ['exch_nasd','exch_nyse'] for page in range(i, i+step, step)]

            event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop)
            tasks = [asyncio.ensure_future(self.async_fetch_stocks(url)) for url in pg_url]
            stocks = event_loop.run_until_complete(asyncio.gather(*tasks))
            event_loop.close()

            stock_pages.extend(stocks)
        return stock_pages

    def _scrapy(self):
        stock_pages = list()

        url = 'https://finviz.com/screener.ashx?v=111&f={exchange}&o=-marketcap&r={page}'

        pg_url = [url.format(exchange=exchange,page=page) for exchange in ['exch_nasd','exch_nyse'] for page in range(1, 4500, 20)]

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        tasks = [asyncio.ensure_future(self.async_fetch_stocks(url)) for url in pg_url]
        stock_pages = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()

        return stock_pages

    def save(self, Stock, stock_pages):
        super().save(Stock, stock_pages)

    def upsert(self, Stock, Candle, stock_pages):
        super().upsert(Stock, Candle, stock_pages)

#AbstractProductA
class AbstractProductCrawlCandle(AbstractProductCrawl):
    codes = None
    days  = None
    parser = None

    def __init__(self, parser, **kwargs):
        super().__init__(**kwargs)
        self.parser = parser

    @abc.abstractmethod
    def setup(self, codes, days):
        self.codes = codes
        self.days  = days
        pass

    @abc.abstractmethod
    def scrapy(self):
        pass

    @abc.abstractmethod
    def upsert(self, Stock, Candle, ohlcv_pages):
        for ohlcvs in ohlcv_pages:
            if not ohlcvs:
                continue
            code = ohlcvs[0]['code']
            stock = Stock.objects.get({'code':code})
            new_ohlcvs = cal_diff_ohlcvs(code, Candle, ohlcvs)
            try:
                candle = Candle.objects.get({'code':code})
                stock.new_adj_close = candle.add_or_replace_ohlcv(new_ohlcvs)
                candle.save()
            except Exception as e:
                print('exception', code, e)
                candle = Candle(code=code,
                    stock=stock,
                    ohlcvs=[Ohlcv(ohlcv['date'], ohlcv) for ohlcv in new_ohlcvs]
                ).save()
            ohlcvs = candle.ohlcvs[-50:]
            stock.avg_v50 = np.average([o.close * o.volume for o in ohlcvs])
            stock.save()

    @abc.abstractmethod
    def save(self, Stock, Candle, ohlcv_pages):
        for ohlcvs in ohlcv_pages:
            if not ohlcvs:
                continue
            code = ohlcvs[0]['code']
            stock = Stock.objects.raw({'code':code}).first()
            new_ohlcvs = cal_diff_ohlcvs(code, Candle, ohlcvs)
            candle = Candle(code=code,
                   stock=stock,
                   #ohlcvs=[Ohlcv(ohlcv['date'], ohlcv) for ohlcv in ohlcvs]
                   ohlcvs=[Ohlcv(ohlcv['date'], ohlcv) for ohlcv in new_ohlcvs]
            ).save()

            ohlcvs = candle.ohlcvs[-50:]
            stock.new_adj_close = False
            stock.avg_v50 = np.average([o.close * o.volume for o in ohlcvs])
            stock.save()


#ConcreteProductA
class ConcreteProductCrawlCandleKr(AbstractProductCrawlCandle):
    def __init__(self, **kwargs):
        factory = AbstractParserFactory.get_factory('kr')
        parser = factory.create_parser()

        super().__init__(parser, **kwargs)

    def setup(self, codes, days):
        super().setup(codes, days)
        
    async def async_fetch_ohlcv(self, url):
        ohlcv = list()

        code = get_value(url, 'symbol=', '&')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await asyncio.sleep(.1)
                html = await response.read()
                html = html.decode('euc-kr', 'ignore').replace('\t','').replace('"','').replace('/>','')

                ohlcv = self.parser.regex_ohlcv(code, html)
        return ohlcv

    # yfinance는 국내주식 정보를 제대로 넘겨주지 않는다. 수정주가가 이상함
    def scrapy(self):
        ohlcvs = list()
        url = 'https://fchart.stock.naver.com/sise.nhn?symbol={code}&timeframe=day&count=%d&requestType=0' % self.days

        urls = [url.format(code=code) for code in self.codes]

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        tasks = [asyncio.ensure_future(self.async_fetch_ohlcv(url)) for url in urls]
        ohlcvs = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()
        return ohlcvs

    def upsert(self, Stock, Candle, ohlcv_pages):
        super().upsert(Stock, Candle, ohlcv_pages)

    def save(self, Stock, Candle, ohlcv_pages):
        super().save(Stock, Candle, ohlcv_pages)

#ConcreteProductB
class ConcreteProductCrawlCandleUs(AbstractProductCrawlCandle):
    def __init__(self, **kwargs):
        factory = AbstractParserFactory.get_factory('us')
        parser = factory.create_parser()

        super().__init__(parser, **kwargs)

    def setup(self, codes, days):
        super().setup(codes, days)

    async def async_fetch_ohlcv(self, url):
        ohlcv = list()

        code = get_value(url, 'chart/', '?')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await asyncio.sleep(.1)
                html = await response.read()
                html = html.decode().replace(':','').replace('"','')

                ohlcv = self.parser.regex_ohlcv(code, html)
        return ohlcv

    def scrapy(self):
        ohlcvs = list()

        today = datetime.today()
        date2 = datetime(today.year, today.month, today.day)
        date1 = date2 - relativedelta(days = self.days)
        period1 = int(time.mktime(date1.timetuple()))
        period2 = int(time.mktime(date2.timetuple()))

        url = 'https://query1.finance.yahoo.com/v8/finance/chart/{code}?lang=en-US&region=US&includeAdjustedClose=true&interval=1d&period1=%s&period2=%s&corsDomain=finance.yahoo.com' % (period1, period2)

        urls = [url.format(code=code) for code in self.codes]

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        tasks = [asyncio.ensure_future(self.async_fetch_ohlcv(url)) for url in urls]
        ohlcvs = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()
        return ohlcvs

    def upsert(self, Stock, Candle, ohlcv_pages):
        super().upsert(Stock, Candle, ohlcv_pages)

    def save(self, Stock, Candle, ohlcv_pages):
        super().save(Stock, Candle, ohlcv_pages)

    """
    def scrapy_yf(self):
        ohlcvs = list()
        
        today = datetime.today()
        edate = datetime_to_str(today,'%Y-%m-%d')
        sdate = datetime_to_str(today-relativedelta(days=self.days),'%Y-%m-%d')

        df = yf.download(self.codes, start=sdate, end=edate)
        df.rename(columns = {'Date':'date', 'Open':'open', 'Adj Close': 'close', 'High':'high', 'Low':'low', 'Volume':'volume'}, inplace = True)

        ohlcvs = {idx: gp.xs(idx, level=1, axis=1) for idx, gp in df.groupby(level=1, axis=1)}
        return ohlcvs

    def save_yf(self, Stock, Candle, ohlcv_pages):
        for code, ohlcvs in ohlcv_pages.items():
            #ITRN 는 수정주가가 음수이다 (2013-10-01)
            ohlcvs_log = np.log(ohlcvs.loc[ohlcvs['close'] > 0, 'close'])
            ohlcvs['log'] = ohlcvs_log
            ohlcvs = ohlcvs.dropna()

            if ohlcvs.empty:
                continue

            stock = Stock.objects.raw({'code':code}).first()

            candle = Candle.objects.raw({'code':code})
            if candle.count() > 0:
                candle = candle.first()
                candle.add_or_replace_ohlcv22(ohlcvs)
                candle.save()
                continue

            Candle(code=code,
                   stock=stock,
                   ohlcvs=[
                       Ohlcv(date, ohlcv) for date, ohlcv in ohlcvs.iterrows()
                   ]
            ).save()
    """

#AbstractProductA
class AbstractProductCrawlCompany(AbstractProductCrawl):
    code = None
    parser = None

    def __init__(self, parser, **kwargs):
        super().__init__(**kwargs)
        self.parser = parser

    @abc.abstractmethod
    def setup(self, code):
        self.code = code

    @abc.abstractmethod
    def scrapy(self):
        pass

#ConcreteProductA
class ConcreteProductCrawlCompanyKr(AbstractProductCrawlCompany):
    def __init__(self, **kwargs):
        factory = AbstractParserFactory.get_factory('kr')
        parser = factory.create_parser()

        super().__init__(parser, **kwargs)

    def setup(self, code):
        super().setup(code)

    def scrapy(self):
        url ='https://finance.naver.com/item/main.nhn?code={}'.format(self.code)

        response = requests.get(url)
        company = self.parser.regex_company(response.text)

        if not company:
            return None

        factory = AbstractCrawlFactory.get_factory('kr')
        crawl_tick = factory.create_crawl_tick()
        ohlcv = crawl_tick.scrapy(self.code)
        close = ohlcv['close']

        cns_eps = company['cns_eps']    #추정EPS
        cns_eps = cns_eps.replace(',','').replace('원','')

        if cns_eps == 'N/A':
            cns_per = 'N/A'
        else:
            cns_per = format(int(close) / int(cns_eps),'.2f') + '배'

        company['close'] = format(int(close), ',') + '원'
        company['cns_per'] = cns_per #추정PER

        return company

#ConcreteProductB
class ConcreteProductCrawlCompanyUs(AbstractProductCrawlCompany):
    def __init__(self, **kwargs):
        factory = AbstractParserFactory.get_factory('us')
        parser = factory.create_parser()

        super().__init__(parser, **kwargs)

    def setup(self, code):
        super().setup(code)

    def scrapy(self):
        url = 'https://finviz.com/quote.ashx?t={}'.format(self.code)
        response = requests.get(url)
        company = self.parser.regex_company(response.text)

        return company

#AbstractProductA
class AbstractProductCrawlTick(AbstractProductCrawl):
    code = None
    parser = None

    def __init__(self, parser, **kwargs):
        super().__init__(**kwargs)
        self.parser = parser

    @abc.abstractmethod
    def scrapy(self, code):
        pass

#ConcreteProductA
class ConcreteProductCrawlTickKr(AbstractProductCrawlTick):
    def __init__(self, **kwargs):
        factory = AbstractParserFactory.get_factory('kr')
        parser = factory.create_parser()

        super().__init__(parser, **kwargs)

    def scrapy(self, code):
        url = 'https://fchart.stock.naver.com/sise.nhn?symbol={code}&timeframe=day&count=1&requestType=0'.format(code=code)

        response = requests.get(url)
        ohlcv = self.parser.regex_ohlcv(code, response.text)
        return ohlcv[0]

#ConcreteProductB
class ConcreteProductCrawlTickUs(AbstractProductCrawlTick):
    def __init__(self, **kwargs):
        factory = AbstractParserFactory.get_factory('us')
        parser = factory.create_parser()

        super().__init__(parser, **kwargs)

    def scrapy(self, code):
        url = f'https://l1-query.finance.yahoo.com/v8/finance/chart/{code}?&range=%s&interval=1d' % '1d'
        response = requests.get(url)
        html = response.text.replace(':','').replace('"','')
        ohlcv = self.parser.regex_ohlcv(code, html)
        return ohlcv[0]

if __name__ == '__main__':
    #request_companies('005930', '000030')
    #print(request_companies('005930', '000030'))
    #stock_pages = request_stock_pages();
    #request_stock_pages_us()
    pass

