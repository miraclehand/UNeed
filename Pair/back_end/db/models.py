from pymongo import ASCENDING
from pymongo.operations import IndexModel
from pymodm import MongoModel, EmbeddedMongoModel, fields, connect

from commons.basedb.models import Stock, StockKr, StockUs
from commons.basedb.models import Candle, CandleKr, CandleUs

#https://pymodm.readthedocs.io/en/latest/index.html
#https://github.com/mongodb/pymodm/tree/master/example/blog

# Establish a connectin to database.
connect('mongodb://localhost:27017/pair', alias='pair', connect=False)

class User(MongoModel):
    username = fields.CharField()
    password = fields.CharField()
    level    = fields.IntegerField()

    class Meta:
        connection_alias = 'pair'
        collection_name = 'user'

class Asset(MongoModel):
    username = fields.CharField()
    budget = fields.IntegerField()

    class Meta:
        connection_alias = 'pair'
        collection_name = 'asset'

    @property
    def to_dict(self):
        return {
            'username' : self.username,
            'budget': self.budget,
        }
    
class StockPair(MongoModel):
    date1  = fields.DateTimeField(required=True)
    date2  = fields.DateTimeField(required=True)

    close1 = fields.IntegerField()
    close2 = fields.IntegerField()

    per1 = fields.CharField()
    per2 = fields.CharField()

    def __init__(self, date1=None, date2=None, **kwargs):
        super().__init__(**kwargs)
        self.date1 = date1
        self.date2 = date2
        self.per1 = 'N/A'
        self.per2 = 'N/A'

class NodePair(MongoModel):
    corr   = fields.FloatField()
    coint_pvalue = fields.FloatField()

class Figure(EmbeddedMongoModel):
    coint_fit    = fields.FloatField()
    coint_calc   = fields.FloatField()
    coint_select = fields.FloatField()
    coint_std    = fields.FloatField()

    ks_pvalue    = fields.FloatField()
    adf_pvalue   = fields.FloatField()
    coint_pvalue = fields.FloatField()

    value     = fields.FloatField()
    density   = fields.FloatField()
    place     = fields.IntegerField()
    place_cnt = fields.IntegerField()

    hit0_cnt = fields.IntegerField()
    """
    cy5_cnt  = fields.IntegerField()
    cy10_cnt = fields.IntegerField()
    cy15_cnt = fields.IntegerField()
    cy20_cnt = fields.IntegerField()
    """

    cy10_cnt = fields.IntegerField()
    cy20_cnt = fields.IntegerField()
    cy30_cnt = fields.IntegerField()
    cy40_cnt = fields.IntegerField()
    cy50_cnt = fields.IntegerField()
    cy60_cnt = fields.IntegerField()
    cy70_cnt = fields.IntegerField()
    cy80_cnt = fields.IntegerField()
    cy90_cnt = fields.IntegerField()

    cy10_20_cnt = fields.IntegerField()
    cy10_30_cnt = fields.IntegerField()
    cy10_40_cnt = fields.IntegerField()
    cy10_50_cnt = fields.IntegerField()
    cy10_60_cnt = fields.IntegerField()
    cy10_70_cnt = fields.IntegerField()
    cy10_80_cnt = fields.IntegerField()
    cy10_90_cnt = fields.IntegerField()

    cy20_30_cnt = fields.IntegerField()
    cy20_40_cnt = fields.IntegerField()
    cy20_50_cnt = fields.IntegerField()
    cy20_60_cnt = fields.IntegerField()
    cy20_70_cnt = fields.IntegerField()
    cy20_80_cnt = fields.IntegerField()
    cy20_90_cnt = fields.IntegerField()

    cy30_40_cnt = fields.IntegerField()
    cy30_50_cnt = fields.IntegerField()
    cy30_60_cnt = fields.IntegerField()
    cy30_70_cnt = fields.IntegerField()
    cy30_80_cnt = fields.IntegerField()
    cy30_90_cnt = fields.IntegerField()

    cy40_50_cnt = fields.IntegerField()
    cy40_60_cnt = fields.IntegerField()
    cy40_70_cnt = fields.IntegerField()
    cy40_80_cnt = fields.IntegerField()
    cy40_90_cnt = fields.IntegerField()

    cy50_60_cnt = fields.IntegerField()
    cy50_70_cnt = fields.IntegerField()
    cy50_80_cnt = fields.IntegerField()
    cy50_90_cnt = fields.IntegerField()

    cy60_70_cnt = fields.IntegerField()
    cy60_80_cnt = fields.IntegerField()
    cy60_90_cnt = fields.IntegerField()

    cy70_80_cnt = fields.IntegerField()
    cy70_90_cnt = fields.IntegerField()

    cy80_90_cnt = fields.IntegerField()

    spread_min = fields.FloatField()
    spread_max = fields.FloatField()

class Basket(EmbeddedMongoModel):
    stock      = fields.ReferenceField(Stock, required=True)
    pos        = fields.CharField()
    entry_date = fields.DateTimeField(required=True)
    entry_uv   = fields.FloatField()
    entry_qty  = fields.FloatField()
    entry_amt  = fields.FloatField()
    cost       = fields.FloatField()
    exit_date  = fields.DateTimeField()
    exit_uv    = fields.FloatField()
    label      = fields.CharField()

    def __init__(self, stock=None, pos=None, date=None, uv=None, qty=None, amt=None, cost=None, **kwargs):
        super().__init__(**kwargs)

        self.stock      = stock
        self.pos        = pos
        self.entry_date = date
        self.entry_uv   = uv
        self.entry_qty  = qty
        self.entry_amt  = amt
        self.cost       = cost

class Entry(EmbeddedMongoModel):
    entry_id = fields.IntegerField()
    Long  = fields.EmbeddedDocumentField(Basket, required=True)
    Short = fields.EmbeddedDocumentField(Basket, required=True)
    coint = fields.FloatField()
    label = fields.CharField()
    yld   = fields.FloatField()

    def __init__(self, id=None, Long=None, Short=None, coint=None, label=None, **kwargs):
        super().__init__(**kwargs)

        self.entry_id = id
        self.Long  = Long
        self.Short = Short
        self.coint = coint
        self.label = label

    @property
    def to_dict(self):
        return {
            'entry_id': str(self.entry_id),
            'cntry1' :self.Long.stock.cntry,
            'code1' : self.Long.stock.code,
            'label1': self.Long.label,
            'aimed1': self.Long.stock.aimed,
            'date1' : self.Long.entry_date.date(),
            'pos1'  : '+',
            'uv1'   : self.Long.entry_uv,
            'qty1'  : self.Long.entry_qty,
            'amt1'  : self.Long.entry_amt,
            'cost1' : self.Long.cost,
            'ratio1': self.coint,
            'cntry2' :self.Short.stock.cntry,
            'code2' : self.Short.stock.code,
            'label2': self.Short.label,
            'aimed2': self.Short.stock.aimed,
            'date2' : self.Short.entry_date.date(),
            'pos2'  : '-',
            'uv2'   : self.Short.entry_uv,
            'qty2'  : self.Short.entry_qty,
            'amt2'  : self.Short.entry_amt,
            'cost2' : self.Short.cost,
            'ratio2': self.coint,
        }

class Strainer(MongoModel):
    username = fields.CharField()
    name   = fields.CharField()
    label  = fields.CharField()
    
    #just reference
    date1 = fields.CharField()
    date2 = fields.CharField()

    #buy
    #stock filter
    close         = fields.FloatField()
    avg_v50       = fields.FloatField()
    stock_type    = fields.IntegerField()
    stock_ind     = fields.IntegerField()
    stock_exc_ind = fields.CharField()

    #pair spread
    density       = fields.FloatField()
    place         = fields.FloatField()
    coint         = fields.FloatField()
    coint_std     = fields.FloatField()
    dist_yield    = fields.FloatField()

    hit0_cnt      = fields.IntegerField()
    cy5_cnt       = fields.IntegerField()
    cy10_cnt      = fields.IntegerField()
    cy15_cnt      = fields.IntegerField()
    cy20_cnt      = fields.IntegerField()

    #pair null hypothese test
    ks_pvalue     = fields.FloatField()
    adf_pvalue    = fields.FloatField()
    coint_pvalue  = fields.FloatField()

    #sell
    clear_yield = fields.FloatField()
    loss_yield  = fields.FloatField()
    days        = fields.IntegerField()

    def __init__(self, id=None, newone=None, report_id=None, **kwargs):
        super().__init__(**kwargs)

        if newone is None:
            return
        self.username = id
        self.name = report_id if report_id else newone['name']
        self.label= self.name

        #just reference
        self.date1 = newone['date1']
        self.date2 = newone['date2']

        #stock filter
        self.close         = float(newone['close'])
        self.avg_v50       = float(newone['avg_v50'])
        self.stock_type    = int(newone['stock_type'])
        self.stock_ind     = int(newone['stock_ind'])
        self.stock_exc_ind = str(newone['stock_exc_ind'])

        #pair spread
        self.density       = float(newone['density'])
        self.place         = float(newone['place'])
        self.coint         = float(newone['coint'])
        self.coint_std     = float(newone['coint_std'])
        self.dist_yield    = float(newone['dist_yield'])

        self.hit0_cnt      = int(newone['hit0_cnt'])
        self.cy5_cnt       = int(newone['cy5_cnt'])
        self.cy10_cnt      = int(newone['cy10_cnt'])
        self.cy15_cnt      = int(newone['cy15_cnt'])
        self.cy20_cnt      = int(newone['cy20_cnt'])

        #pair null hypothese test
        self.ks_pvalue    = float(newone['ks_pvalue'])
        self.adf_pvalue   = float(newone['adf_pvalue'])
        self.coint_pvalue = float(newone['coint_pvalue'])

        #sell
        self.clear_yield = float(newone['clear_yield'])
        self.loss_yield  = float(newone['loss_yield'])
        self.days        = int(newone['days'])

    @property
    def to_dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'label': self.label,
            'date1': self.date1,
            'date2': self.date2,

            'close': self.close,
            'avg_v50': self.avg_v50,
            'stock_type': self.stock_type,
            'stock_ind': self.stock_ind,
            'stock_exc_ind': self.stock_exc_ind,

            'density': self.density,
            'place': self.place,
            'coint': self.coint,
            'coint_std': self.coint_std,
            'dist_yield': self.dist_yield,
            'hit0_cnt': self.hit0_cnt,
            'cy5_cnt': self.cy5_cnt,
            'cy10_cnt': self.cy10_cnt,
            'cy15_cnt': self.cy15_cnt,
            'cy20_cnt': self.cy20_cnt,

            'ks_pvalue': self.ks_pvalue,
            'adf_pvalue': self.adf_pvalue,
            'coint_pvalue': self.coint_pvalue,

            'clear_yield': self.clear_yield,
            'loss_yield': self.loss_yield,
            'days': self.days,
        }

class Report(MongoModel):
    username    = fields.CharField(required=True)
    create_date = fields.DateTimeField()
    seq         = fields.IntegerField()

    entries     = fields.EmbeddedDocumentListField(Entry, default=[])

    strainer    = fields.EmbeddedDocumentField(Strainer)

    long_cnt    = fields.IntegerField()
    short_cnt   = fields.IntegerField()
    hold_cnt    = fields.IntegerField()
    yld         = fields.FloatField()

    def __init__(self, username=None, create_date=None, seq=None, **kwargs):
        super().__init__(**kwargs)
        
        self.username = username
        self.create_date = create_date
        self.seq = seq
        self.yld = 0

class SimulaReport(Report):
    date1       = fields.DateTimeField(required=True)
    date2       = fields.DateTimeField(required=True)

    progress    = fields.FloatField()
    seconds     = fields.IntegerField()
    valid       = fields.BooleanField()

    def __init__(self, username=None, create_date=None, seq=None, **kwargs):
        super().__init__(username, create_date, seq, **kwargs)
        
        self.progress = 0
        self.seconds = 0
        self.valid = True

class PickedPair(MongoModel):
    corr = fields.FloatField()
    corr_std  = fields.FloatField()
    coint_std = fields.FloatField()
    fig_str = fields.EmbeddedDocumentField(Figure) # straight
    fig_rev = fields.EmbeddedDocumentField(Figure) # reverse

# kr
class StockPairKr(StockPair):
    stock1 = fields.ReferenceField(StockKr, required=True)
    stock2 = fields.ReferenceField(StockKr, required=True)

    def __init__(self, date1=None,date2=None,stock1=None,stock2=None,**kwargs):
        super().__init__(date1, date2, **kwargs)
        self.stock1 = stock1
        self.stock2 = stock2

class NodePairKr(NodePair, StockPairKr):
    class Meta:
        connection_alias = 'pair'
        collection_name = 'node_pair_kr'
        indexes = [
            IndexModel([('date2',ASCENDING)], name='node_pair_kr_date2')
        ]

class PickedPairKr(PickedPair, StockPairKr):
    class Meta:
        connection_alias = 'pair'
        collection_name = 'picked_pair_kr'
        indexes = [
            IndexModel([('date2',ASCENDING)], name='picked_pair_kr_date2')
        ]

class BasketKr(Basket):
    stock = fields.ReferenceField(StockKr, required=True)

class EntryKr(Entry):
    Long  = fields.EmbeddedDocumentField(BasketKr, required=True)
    Short = fields.EmbeddedDocumentField(BasketKr, required=True)

class StrainerKr(Strainer):
    class Meta:
        connection_alias = 'pair'
        collection_name = 'strainer_kr'

class TradingReportKr(Report):
    entries  = fields.EmbeddedDocumentListField(EntryKr, default=[])
    strainer = fields.EmbeddedDocumentField(StrainerKr)

    class Meta:
        connection_alias = 'pair'
        collection_name = 'trading_report_kr'

class SimulaReportKr(SimulaReport):
    entries  = fields.EmbeddedDocumentListField(EntryKr, default=[])
    strainer = fields.EmbeddedDocumentField(StrainerKr)

    class Meta:
        connection_alias = 'pair'
        collection_name = 'simula_report_kr'

# us
class StockPairUs(StockPair):
    stock1 = fields.ReferenceField(StockUs, required=True)
    stock2 = fields.ReferenceField(StockUs, required=True)

    def __init__(self, date1=None,date2=None,stock1=None,stock2=None,**kwargs):
        super().__init__(date1, date2, **kwargs)
        self.stock1 = stock1
        self.stock2 = stock2

class NodePairUs(NodePair, StockPairUs):
    class Meta:
        connection_alias = 'pair'
        collection_name = 'node_pair_us'
        indexes = [
            IndexModel([('date2',ASCENDING)], name='node_pair_us_date2')
        ]

class PickedPairUs(PickedPair, StockPairUs):
    corr = fields.FloatField()
    corr_std  = fields.FloatField()
    coint_std = fields.FloatField()
    fig_str = fields.EmbeddedDocumentField(Figure) # straight
    fig_rev = fields.EmbeddedDocumentField(Figure) # reverse

    class Meta:
        connection_alias = 'pair'
        collection_name = 'picked_pair_us'
        indexes = [
            IndexModel([('date2',ASCENDING)], name='picked_pair_us_date2')
        ]

class BasketUs(Basket):
    stock = fields.ReferenceField(StockUs, required=True)

class EntryUs(Entry):
    Long  = fields.EmbeddedDocumentField(BasketUs, required=True)
    Short = fields.EmbeddedDocumentField(BasketUs, required=True)

class StrainerUs(Strainer):
    class Meta:
        connection_alias = 'pair'
        collection_name = 'strainer_us'

class TradingReportUs(Report):
    entries  = fields.EmbeddedDocumentListField(EntryUs, default=[])
    strainer = fields.EmbeddedDocumentField(StrainerUs)

    class Meta:
        connection_alias = 'pair'
        collection_name = 'trading_report_us'

class SimulaReportUs(SimulaReport):
    entries  = fields.EmbeddedDocumentListField(EntryUs, default=[])
    strainer = fields.EmbeddedDocumentField(StrainerUs)

    class Meta:
        connection_alias = 'pair'
        collection_name = 'simula_report_us'

# kind => 9:all, 1:parent, 2:industry, 3:aimed, 4:makret
class Classify(MongoModel):
    kind  = fields.IntegerField(required=True)
    code  = fields.CharField(required=True)
    label = fields.CharField(required=True)
    cnt   = fields.IntegerField()
    #nodes = fields.EmbeddedDocumentListField(PickedPair, default=[])

    class Meta:
        connection_alias = 'pair'
        collection_name = 'classify'

    def __init__(self, kind=None, label=None, nodes=None, **kwargs):
        super().__init__(**kwargs)

        self.kind = kind
        self.label = label
        self.nodes= nodes

"""
미국증시:
    뉴욕증권거래소 (NYSE)
        나스닥 (NASDAQ)

        다우지수: 뉴욕증권거래소의 주요 우량종목의 주가추이

        나스닥 : 3500 개
        뉴욕   : 3100 개


        https://content1.edgar-online.com/cfeed/ext/charts.dll?81-0-0-0-0-125072016-03NA000000MSFT&SF:1000-FREQ=6-STOK=awW69d9qR8k9HM+pAuvR2Z4d/L8txRsVJTSUZOftveIoRI0+ulxKn9ejsTC2k7mz-1564012983932
"""
