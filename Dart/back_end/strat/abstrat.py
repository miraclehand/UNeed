import abc
import xlsxwriter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from commons.utils.datetime import str_to_datetime, datetime_to_str
from commons.basedb.models import StockKr
from task.mfg.reproduce import get_ohlcv_pool
from strat.util import get_d_prrt

# Abstract Factory Pattern
#AbstractFactory
class AbstractStratFactory(metaclass=abc.ABCMeta):
    @classmethod
    def get_factory(self, strat):
        if strat == 'Strat2':
            from strat.strat2 import ConcreteStrat2Factory
            return ConcreteStrat2Factory(strat)
        return None

class AbstractProductStrat(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def do_simula(self, begin, end):
        pass

#AbstractProductA
class AbstractProductStratKr(AbstractProductStrat):
    strat = ''
    header1 = [
        '공시일자',
        '공시명',
        '종목명',
        '시가총액',
        '10일평균거래량',
    ]
    header2 = [
        '시가',
        '고가',
        '저가',
        '종가',
        'af1-시가',
        'af1-고가',
        'af1-저가',
        'af1-종가',
        '60일전 종가',
        '30일전 종가',
        '7일전 종가',
        '현재가(공시후 시가)',
        '7일후 종가',
        '30일후 종가',
        '60일후 종가',
        '60일전 등락률',
        '30일전 등락률',
        '7일전 등락률',
        '7일후 등락률',
        '30일후 등락률',
        '60일후 등락률',
        '고가일자',
        '고가',
        '고가대비 등락률',
    ]

    def __init__(self, strat, **kwargs):
        self.strat = strat

    @abc.abstractmethod
    def do_simula(self):
        pass

    def new_workbook(self):
        now  = datetime_to_str(datetime.now(),'%Y%m%d')
        name = f'SimulaDart{self.strat}_{now}.xlsx'
        filename = name
        workbook = xlsxwriter.Workbook(filename, {'constant_memory':True})
        return workbook

    def print_body1(self, sheet, row, column, disc):
        rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()
        bf01 = rcept_date + relativedelta(days = -1)

        stock = StockKr.objects.get({'code':disc.corp.stock_code})
        df = get_ohlcv_pool(stock.code)
        if df.empty:
            avg_vol10 = 0
        else:
            values = df.loc[:bf01].tail(10)['volume'].values
            if values.__len__() > 0:
                avg_vol10 = round(sum(values) / len(values),2)
            else:
                avg_vol10 = 0

        rcept_date = datetime_to_str(rcept_date,'%Y/%m/%d')
        sheet.write(row, column + 0, rcept_date)            #공시일자
        sheet.write(row, column + 1, disc.report_nm)        #공시명
        sheet.write(row, column + 2, disc.corp.corp_name)   #종목명
        sheet.write(row, column + 3, stock.capital)         #시가총액
        sheet.write(row, column + 4, avg_vol10)             #10일평균거래량
        return 5    #입력한 개수

    def print_body2(self, sheet, row, column, disc):
        rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()

        bf60 = rcept_date + relativedelta(months = -2)
        bf30 = rcept_date + relativedelta(months = -1)
        bf07 = rcept_date + relativedelta(days   = -7)
        bf01 = rcept_date + relativedelta(days   = -1)
        af01 = rcept_date + relativedelta(days   = +1)
        af07 = rcept_date + relativedelta(days   = +7)
        af30 = rcept_date + relativedelta(months = +1)
        af60 = rcept_date + relativedelta(months = +2)

        close = disc.tick

        stock = StockKr.objects.get({'code':disc.corp.stock_code})
        df = get_ohlcv_pool(stock.code)

        bf60_close, bf60_rt = get_d_prrt(df.loc[:bf60], close)
        bf30_close, bf30_rt = get_d_prrt(df.loc[:bf30], close)
        bf07_close, bf07_rt = get_d_prrt(df.loc[:bf07], close)
        af07_close, af07_rt = get_d_prrt(df.loc[:af07], close)
        af30_close, af30_rt = get_d_prrt(df.loc[:af30], close)
        af60_close, af60_rt = get_d_prrt(df.loc[:af60], close)

        d_open  = df.loc[rcept_date:].head(1)['open'].values[0]
        d_high  = df.loc[rcept_date:].head(1)['high'].values[0]
        d_low   = df.loc[rcept_date:].head(1)['low'].values[0]
        d_close = df.loc[rcept_date:].head(1)['close'].values[0]
        af01_open  = df.loc[af01:].head(1)['open'].values[0]
        af01_high  = df.loc[af01:].head(1)['high'].values[0]
        af01_low   = df.loc[af01:].head(1)['low'].values[0]
        af01_close = df.loc[af01:].head(1)['close'].values[0]

        df_h = df.loc[af01:af60]['high']
        if df_h.empty:
            high = 0
            high_date = 'N/A'
            high_ratio= 0
        else:
            high = max(df_h.values)
            high_date = datetime_to_str(df_h[df_h == high].keys()[0],'%Y/%m/%d')
            high_ratio= round((high-close) / close * 100,2) if close > 0 else 0

        sheet.write(row, column + 0, d_open)        #시가
        sheet.write(row, column + 1, d_high)        #고가
        sheet.write(row, column + 2, d_low)         #저가
        sheet.write(row, column + 3, d_close)       #종가
        sheet.write(row, column + 4, af01_open)     #익일시가
        sheet.write(row, column + 5, af01_high)     #익일고가
        sheet.write(row, column + 6, af01_low)      #익일저가
        sheet.write(row, column + 7, af01_close)    #익일종가
        sheet.write(row, column + 8, bf60_close)    #60일전종가
        sheet.write(row, column + 9, bf30_close)    #30일전종가
        sheet.write(row, column +10, bf07_close)    #07일전종가
        sheet.write(row, column +11, close)         #현재가(공시후 시가)
        sheet.write(row, column +12, af07_close)    #07일후종가
        sheet.write(row, column +13, af30_close)    #30일후종가
        sheet.write(row, column +14, af60_close)    #60일후종가
        sheet.write(row, column +15, bf60_rt)       #60일등락률
        sheet.write(row, column +16, bf30_rt)       #30일전등락률
        sheet.write(row, column +17, bf07_rt)       #07일전등락률
        sheet.write(row, column +18, af07_rt)       #07일후등락률
        sheet.write(row, column +19, af30_rt)       #30일후등락률
        sheet.write(row, column +20, af60_rt)       #60일후등락률
        sheet.write(row, column +21, high_date)     #고가일자
        sheet.write(row, column +22, high)          #고가가격
        sheet.write(row, column +23, high_ratio)    #고가대비등락률
        return 24    #입력한 개수
