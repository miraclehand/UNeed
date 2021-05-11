from datetime import datetime
from pymongo import ASCENDING
from pymongo.operations import IndexModel
from pymodm import MongoModel, EmbeddedMongoModel, fields, connect

#https://pymodm.readthedocs.io/en/latest/index.html
#https://github.com/mongodb/pymodm/tree/master/example/blog

# Establish a connectin to database.
connect('mongodb://localhost:27017/basedb', alias='basedb', connect=False)

class Stock(MongoModel):
    cntry    = fields.CharField(required=True)
    code     = fields.CharField(required=True)
    name     = fields.CharField(required=True)
    dname    = fields.CharField(required=True)  # disassembled name
    label    = fields.CharField(required=True)
    exchange = fields.CharField()
    parent   = fields.CharField()
    sector   = fields.CharField()
    industry = fields.CharField()
    aimed    = fields.CharField()
    capital  = fields.IntegerField()
    avg_v50  = fields.IntegerField()    #average trading value during 50days
    new_adj_close = fields.BooleanField()
    crud     = fields.CharField()   #create, read, update, delete
    lastUpdated = fields.DateTimeField()   # update if insert or delete code
    lastFetched = fields.DateTimeField()   # fetch everyday

    def __init__(self, newone=None, **kwargs):
        super().__init__(**kwargs)

        if newone is None:
            return
        self.cntry     = newone['cntry']    if 'cntry'    in newone else ''
        self.code      = newone['code']     if 'code'     in newone else ''
        self.name      = newone['name']     if 'name'     in newone else ''
        self.dname     = newone['dname']    if 'dname'    in newone else ''
        self.label     = newone['label']    if 'label'    in newone else ''
        self.exchange  = newone['exchange'] if 'exchange' in newone else ''
        self.parent    = newone['parent']   if 'parent'   in newone else ''
        self.sector    = newone['sector']   if 'sector'   in newone else ''
        self.industry  = newone['industry'] if 'industry' in newone else ''
        self.aimed     = newone['aimed']    if 'aimed'    in newone else ''
        self.capital   = newone['capital']  if 'capital'  in newone else ''
        self.avg_v50   = newone['avg_v50']  if 'avg_v50'  in newone else ''
        self.crud      = 'C'
        today = datetime.today()
        today = datetime(today.year, today.month, today.day)
        self.new_adj_close = False
        self.lastUpdated  = today
        self.lastFetched  = today

    @property
    def to_dict(self):
        return {
            'id'  : str(self._id),
            'cntry': self.cntry,
            'code': self.code,
            'name': self.name,
            'dname': self.dname,
            'label': self.label,
            'exchange': self.exchange,
            'parent': self.parent,
            'sector': self.sector,
            'industry': self.industry,
            'aimed': self.aimed,
            'capital': self.capital,
            'avg_v50': self.avg_v50,
            'crud': self.crud,
            'lastUpdated': self.lastUpdated.date(),
            'lastFetched': self.lastFetched.date(),
        }

class Ohlcv(EmbeddedMongoModel):
    date  = fields.DateTimeField(required=True)
    close = fields.FloatField(required=True)
    open  = fields.FloatField()
    high  = fields.FloatField()
    low   = fields.FloatField()
    volume= fields.FloatField()
    diff  = fields.FloatField()
    change= fields.FloatField()
    log   = fields.FloatField()

    def __init__(self, date=None, newone=None, **kwargs):
        super().__init__(**kwargs)

        if newone is None:
            return

        self.date  = date
        self.close = newone['close']
        self.open  = newone['open']
        self.high  = newone['high']
        self.low   = newone['low']
        self.volume= newone['volume']
        self.diff  = newone['diff']
        self.change= newone['change']
        self.log   = newone['log']
        
    @property
    def to_dict(self):
        return {
            'date'  : self.date.date(),
            'close' : self.close,
            'open'  : self.open,
            'high'  : self.high,
            'low'   : self.low,
            'volume': self.volume,
            'diff'  : self.diff,
            'change': self.change,
            'log'   : self.log
        }

class Candle(MongoModel):
    code = fields.CharField(required=True)
    stock = fields.ReferenceField(Stock)
    #ohlcvs = fields.EmbeddedModelListField(Ohlcv, default=[])  FIXME over 0.5v
    ohlcvs = fields.EmbeddedDocumentListField(Ohlcv, default=[])

    def add_or_replace_ohlcv(self, ohlcvs):
        new_adj_close = False
        for i, ohlcv in enumerate(self.ohlcvs):
            if ohlcv.date >= ohlcvs[0]['date']:
                break

        # 권리 때문에, 과거의 수정주가가 바뀌는 경우가 있으면
        # 과거 주가를 다시 받아야한다
        for idx, o in enumerate(self.ohlcvs[i:]):
            #당일 데이터는 무조건 새로운 데이터
            if ohlcvs[idx] == ohlcvs[-1]:
                break
            if o.close != ohlcvs[idx]['close']:
                new_adj_close = True
                break;
        del self.ohlcvs[i:]
        self.ohlcvs.extend([Ohlcv(ohlcv['date'],ohlcv) for ohlcv in ohlcvs])
        return new_adj_close

    def add_or_replace_ohlcv_dict(self, ohlcvs):
        for i, ohlcv in enumerate(self.ohlcvs):
            if ohlcv.date >= ohlcvs.index[-1].to_pydatetime():
                break

        if i > 0:
            del self.ohlcvs[i:]
            self.ohlcvs.extend([Ohlcv(date, ohlcv) for date, ohlcv in ohlcvs.iterrows()])


    def get_close(self, date):
        ohlcv = list(filter(lambda ohlcv: ohlcv.date == date, self.ohlcvs))
        if not ohlcv:
            return 0;
        if ohlcv.__len__() != 1:
            return 0;
        return ohlcv[0].close

    @property
    def to_dict(self):
        return {
            'code'  : self.stock.code,
            'name'  : self.stock.name,
            'ohlcv' : list(self.ohlcvs),
        }

# kr
class StockKr(Stock):
    class Meta:
        connection_alias = 'basedb'
        collection_name = 'stock_kr'
        indexes = [
            IndexModel([('code',ASCENDING)], name='stock_kr_code', unique=True)
        ]

class CandleKr(Candle):
    stock = fields.ReferenceField(StockKr, required=True)

    class Meta:
        connection_alias = 'basedb'
        collection_name = 'candle_kr'
        indexes = [
            IndexModel([('code',ASCENDING)], name='candle_kr_code',unique=True)
        ]

# us
class StockUs(Stock):
    class Meta:
        connection_alias = 'basedb'
        collection_name = 'stock_us'
        indexes = [
            IndexModel([('code',ASCENDING)], name='stock_us_code', unique=True)
        ]

class CandleUs(Candle):
    stock = fields.ReferenceField(StockUs)

    class Meta:
        connection_alias = 'basedb'
        collection_name = 'candle_us'
        indexes = [
            IndexModel([('code',ASCENDING)], name='candle_us_code',unique=True)
        ]

"""
미국증시:
    뉴욕증권거래소 (NYSE)
        나스닥 (NASDAQ)


        다우지수: 뉴욕증권거래소의 주요 우량종목의 주가추이


        나스닥 : 3500 개
        뉴욕   : 3100 개


        https://content1.edgar-online.com/cfeed/ext/charts.dll?81-0-0-0-0-125072016-03NA000000MSFT&SF:1000-FREQ=6-STOK=awW69d9qR8k9HM+pAuvR2Z4d/L8txRsVJTSUZOftveIoRI0+ulxKn9ejsTC2k7mz-1564012983932
"""
