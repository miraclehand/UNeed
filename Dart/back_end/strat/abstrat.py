import abc

import xlsxwriter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from commons.utils.datetime import str_to_datetime, datetime_to_str
from commons.basedb.models import StockKr
from db.models import Fnltt
from task.mfg.reproduce import get_ohlcv_pool
from strat.util import get_content_value, get_prrt, get_d_prrt, get_losscut_date, get_bigo_adj, get_max_value, get_reprt_name
from strat.buy_sell_strat import buy_sell_strat1, buy_sell_strat2, buy_sell_strat3, buy_sell_strat4, buy_sell_strat5

from commons.utils.parser import remove_not_digit, to_number

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
    format_percent = None
    format_num = None
    format_num_color = None
    header_posted = [
        '공시일자',
        '공시시점',
        '공시명',
    ]
    header_stock = [
        '종목명',
        '시가총액',
        '10일평균거래대금(백만)',
        '당기일1',
        '순이익1(억원)',
        '당기일2',
        '순이익2(억원)',
        '당기일3',
        '순이익3(억원)',
        '당기일4',
        '순이익4(억원)',
    ]
    header_rechg = [
        'T-3등락률',
        'T-2등락률',
        'T-1등락률',
        'T등락률',
        'T+1등락률',
        'T+2등락률',
        '52주신고일자',
        '52주신고가대비 등락률',
    ]
    header_after = [
        '시가등락률',
        '고가등락률',
        '저가등락률',
        '종가등락률',
        'af1-시가등락률',
        'af1-고가등락률',
        'af1-저가등락률',
        'af1-종가등락률',
        '현재가(공시후 시가)',
        '현재등락률',
        '60일전 등락률',
        '30일전 등락률',
        '7일전 등락률',
        '당일 등락률',
        '1주일후 등락률',
        '2주일후 등락률',
        '3주일후 등락률',
        '4주일후 등락률',
        '5주일후 등락률',
        '6주일후 등락률',
        '7주일후 등락률',
        '8주일후 등락률',
        '고가일자',
        '고가대비 등락률',
        '5%로스컷일자',
        '10%로스컷일자',
        '15%로스컷일자',
        '20%로스컷일자',
        '30%로스컷일자',
        '비고',
    ]
    header_trade = [
        '이익실현',
        '로스컷',
        '고가일자',
        '고가대비등락률',
        '당일등락률',
        '1주후 매도',
        '2주후 매도',
        '3주후 매도',
        '4주후 매도',
        '5주후 매도',
        '6주후 매도',
        '매도일자1',
        '수익률1',
        '매도일자2',
        '수익률2',
        '매도일자3',
        '수익률3',
        '매도일자4',
        '수익률4',
        '매도일자5',
        '수익률5',
        '비고',
    ]

    def __init__(self, strat, header_strat, **kwargs):
        self.strat = strat
        self.header_raw    = self.header_posted + self.header_stock + self.header_rechg + header_strat + self.header_after
        self.header_filter = self.header_raw
        self.header_trade  = self.header_posted + self.header_stock + self.header_rechg + header_strat + self.header_trade

    @abc.abstractmethod
    def do_simula(self):
        pass

    def new_workbook(self):
        now  = datetime_to_str(datetime.now(),'%Y%m%d')
        name = f'strat/xls/SimulaDart{self.strat}_{now}.xlsx'
        filename = name
        workbook = xlsxwriter.Workbook(filename, {'constant_memory':True})
        self.format_percent   = workbook.add_format()
        self.format_num       = workbook.add_format()
        self.format_num_color = workbook.add_format()

        self.format_percent.set_num_format('#,##0%')
        self.format_num.set_num_format('#,##0')
        self.format_num_color.set_num_format('[Red]+General;[Blue]-General;General')
        return workbook

    def print_posted(self, sheet, row, column, disc):
        rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()

        rcept_date = datetime_to_str(rcept_date,'%Y/%m/%d')+' ' + disc.reg_time
        if disc.reg_time < '09:00':
            rcept_uploaded = '장전'
        elif disc.reg_time > '15:30':
            rcept_uploaded = '장후'
        else:
            rcept_uploaded = '장중'

        datas = [(rcept_date,     None)        #공시일자
                ,(rcept_uploaded, None)        #공시시점
                ,(disc.report_nm, None)        #공시명
        ]

        for index, data in enumerate(datas):
            sheet.write(row, column + index, data[0], data[1])
        return column + datas.__len__()    #입력한 개수

    def print_stock(self, sheet, row, column, disc):
        rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()
        bf01 = rcept_date + relativedelta(days = -1)

        stock = StockKr.objects.get({'code':disc.corp.stock_code})

        df = get_ohlcv_pool(stock.code)
        if df.empty:
            avg_vol10 = 0
        else:
            values = df.loc[:bf01].tail(10)['volume'] * df.loc[:bf01].tail(10)['close']
            if values.__len__() > 0:
                avg_vol10 = round(sum(values) / len(values) / 1000000,2)
            else:
                avg_vol10 = 0

        bsns_year   = disc.rcept_dt[0:4]
        bsns_year_p = str(int(bsns_year) - 1)
        mmdd = disc.rcept_dt[4:]
        if mmdd <= '0331':
            reprt_codes = [ ]
        elif mmdd <= '0630': 
            reprt_codes = [ '11013' ]
        elif mmdd <= '0930': 
            reprt_codes = [ '11013' ,'11012' ]
        elif mmdd <= '1231': 
            reprt_codes = [ '11013' ,'11012' ,'11014' ]

        #'fs_div':'CFS' # 연결재무제표
        #'sj_div':'IS'  # 손익계산서
        #'ord':'27'     # 법인세차감전 순이익
        fnltt = Fnltt.objects \
                    .raw({'corp_code':disc.corp.corp_code}) \
                    .raw({'fs_div':'CFS'}) \
                    .raw({'sj_div':'IS'})  \
                    .raw({'ord':'27'})     \
                    .raw({'$or':[{'bsns_year':{'$lte':bsns_year_p}}, \
                                 {'bsns_year':{'$eq':bsns_year}, \
                                  'reprt_code':{'$in':reprt_codes} \
                                 }]}) \
                    .order_by([('bsns_year',-1),('rcept_no', -1)])

        net_profit1, net_profit2, net_profit3, net_profit4 = 0, 0, 0, 0
        thstrm_dt1,  thstrm_dt2,  thstrm_dt3,  thstrm_dt4  ='','','',''

        if fnltt.count() > 3: 
            reprt_name = get_reprt_name(fnltt[3].reprt_code)
            thstrm_dt1 = f'{fnltt[3].bsns_year} {reprt_name}'
            net_profit1 = to_number(fnltt[3].thstrm_amount)
        if fnltt.count() > 2:
            reprt_name = get_reprt_name(fnltt[2].reprt_code)
            thstrm_dt2 = f'{fnltt[2].bsns_year} {reprt_name}'
            net_profit2 = to_number(fnltt[2].thstrm_amount)
        if fnltt.count() > 1:
            reprt_name = get_reprt_name(fnltt[1].reprt_code)
            thstrm_dt3 = f'{fnltt[1].bsns_year} {reprt_name}'
            net_profit3 = to_number(fnltt[1].thstrm_amount)
        if fnltt.count() > 0:
            reprt_name = get_reprt_name(fnltt[0].reprt_code)
            thstrm_dt4 = f'{fnltt[0].bsns_year} {reprt_name}'
            net_profit4 = to_number(fnltt[0].thstrm_amount)

        net_profit1 = net_profit1 / 100000000
        net_profit2 = net_profit2 / 100000000
        net_profit3 = net_profit3 / 100000000
        net_profit4 = net_profit4 / 100000000
        datas = [(stock.name,    None)            #종목명
                ,(stock.capital, self.format_num) #시가총액
                ,(avg_vol10,     self.format_num) #10일평균거래대금(백만)
                ,(thstrm_dt1,    None)            #당기일1
                ,(net_profit1,   self.format_num) #법인세차감전 순이익1
                ,(thstrm_dt2,    None)            #당기일1
                ,(net_profit2,   self.format_num) #법인세차감전 순이익2
                ,(thstrm_dt3,    None)            #당기일1
                ,(net_profit3,   self.format_num) #법인세차감전 순이익3
                ,(thstrm_dt4,    None)            #당기일1
                ,(net_profit4,   self.format_num) #법인세차감전 순이익3
        ]

        for index, data in enumerate(datas):
            sheet.write(row, column + index, data[0], data[1])
        return column + datas.__len__()    #입력한 개수

    def print_rechg(self, sheet, row, column, disc):
        rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()

        df = get_ohlcv_pool(disc.corp.stock_code)

        changes = df.loc[rcept_date:].head(3)['change']
        changeT  = round(changes[0],2) if changes.__len__() > 0 else '-'
        changeT1 = round(changes[1],2) if changes.__len__() > 1 else '-'
        changeT2 = round(changes[2],2) if changes.__len__() > 2 else '-'

        changes = df.loc[:rcept_date].tail(4)['change']
        changeP3 = round(changes[0],2) if changes.__len__() > 0 else '-'
        changeP2 = round(changes[1],2) if changes.__len__() > 0 else '-'
        changeP1 = round(changes[2],2) if changes.__len__() > 0 else '-'

        s_close = df.loc[rcept_date:].head(1)['close']
        if not s_close.empty:
            d_close = s_close.values[0]
        else:
            d_close = 0

        bf52w = rcept_date + relativedelta(weeks = -52)
        bf01  = rcept_date + relativedelta(days = -1)
        df_h = df.loc[bf52w:bf01]['high']
        if not df_h.empty:
            new_high_date, high = get_max_value(df_h)
            new_high_rt = get_prrt(high, d_close)
        else:
            new_high_date = ''
            new_high_rt = 0

        datas = [(changeP3,      self.format_num_color) #T-3등락률
                ,(changeP2,      self.format_num_color) #T-2등락률
                ,(changeP1,      self.format_num_color) #T-1등락률
                ,(changeT,       self.format_num_color) #T등락률
                ,(changeT1,      self.format_num_color) #T+1등락률
                ,(changeT2,      self.format_num_color) #T+2등락률
                ,(new_high_date, None)                  #신고가일자
                ,(new_high_rt,   self.format_num_color) #신고가등락률
        ]

        for index, data in enumerate(datas):
            sheet.write(row, column + index, data[0], data[1])
        return column + datas.__len__()    #입력한 개수

    """
    def print_body_raw(self, sheet, row, disc):
        column = 0
        column = self.print_posted(sheet, row, column, disc)
        column = self.print_stock( sheet, row, column, disc)
        column = self.print_rechg( sheet, row, column, disc)
        return column

    def print_body1(self, sheet, row, column, disc):
        return self.print_body_raw(sheet, row, disc)
    """

    def print_after(self, sheet, row, column, disc):
        rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()

        bf60 = rcept_date + relativedelta(months = -2)
        bf30 = rcept_date + relativedelta(months = -1)
        bf07 = rcept_date + relativedelta(days   = -7)
        bf01 = rcept_date + relativedelta(days   = -1)
        af01 = rcept_date + relativedelta(days   = +1)
        af1w = rcept_date + relativedelta(weeks  = +1)
        af2w = rcept_date + relativedelta(weeks  = +2)
        af3w = rcept_date + relativedelta(weeks  = +3)
        af4w = rcept_date + relativedelta(weeks  = +4)
        af5w = rcept_date + relativedelta(weeks  = +5)
        af6w = rcept_date + relativedelta(weeks  = +6)
        af7w = rcept_date + relativedelta(weeks  = +7)
        af8w = rcept_date + relativedelta(weeks  = +8)

        close  = disc.tick
        change = disc.change

        stock = StockKr.objects.get({'code':disc.corp.stock_code})
        df = get_ohlcv_pool(stock.code)

        if df.loc[rcept_date:].__len__() > 0:
            d_open   = df.loc[rcept_date:].head(1)['open'].values[0]
            d_high   = df.loc[rcept_date:].head(1)['high'].values[0]
            d_low    = df.loc[rcept_date:].head(1)['low'].values[0]
            d_close  = df.loc[rcept_date:].head(1)['close'].values[0]
            d_change = df.loc[rcept_date:].head(1)['change'].values[0]
            d_change = round(d_change,2)
        else:
            return 0

        if df.loc[af01:].__len__() > 0:
            af01_open   = df.loc[af01:].head(1)['open'].values[0]
            af01_high   = df.loc[af01:].head(1)['high'].values[0]
            af01_low    = df.loc[af01:].head(1)['low'].values[0]
            af01_close  = df.loc[af01:].head(1)['close'].values[0]
            af01_change = df.loc[af01:].head(1)['change'].values[0]
        else:
            af01_open   = '-'
            af01_high   = '-'
            af01_low    = '-'
            af01_close  = '-'
            af01_change = '-'

        bf60_close, bf60_rt = get_d_prrt(df.loc[:bf60], d_close)
        bf30_close, bf30_rt = get_d_prrt(df.loc[:bf30], d_close)
        bf07_close, bf07_rt = get_d_prrt(df.loc[:bf07], d_close)

        af1w_close, af1w_rt = get_d_prrt(df.loc[:af1w], d_close)
        af2w_close, af2w_rt = get_d_prrt(df.loc[:af2w], d_close)
        af3w_close, af3w_rt = get_d_prrt(df.loc[:af3w], d_close)
        af4w_close, af4w_rt = get_d_prrt(df.loc[:af4w], d_close)
        af5w_close, af5w_rt = get_d_prrt(df.loc[:af5w], d_close)
        af6w_close, af6w_rt = get_d_prrt(df.loc[:af6w], d_close)
        af7w_close, af7w_rt = get_d_prrt(df.loc[:af7w], d_close)
        af8w_close, af8w_rt = get_d_prrt(df.loc[:af8w], d_close)

        df_8w= df.loc[af01:af8w]
        df_h = df_8w['high']
        if df_h.empty:
            high = 0
            high_date = 'N/A'
            high_ratio= 0
        else:
            high_date, high = get_max_value(df_h)
            high_ratio = get_prrt(d_close, high)

        df_l = df_8w['low']
        loss05date = get_losscut_date(df_l, d_close,  5)
        loss10date = get_losscut_date(df_l, d_close, 10)
        loss15date = get_losscut_date(df_l, d_close, 15)
        loss20date = get_losscut_date(df_l, d_close, 20)
        loss30date = get_losscut_date(df_l, d_close, 30)

        d_base_close = d_close * 100 / (100 + d_change)

        d_open_rt = get_prrt(d_base_close, d_open)
        d_high_rt = get_prrt(d_base_close, d_high)
        d_low_rt  = get_prrt(d_base_close, d_low)
        d_close_rt= get_prrt(d_base_close, d_close)

        if af01_change == '-':
            af01_open_rt = '-'
            af01_high_rt = '-'
            af01_low_rt  = '-'
            af01_close_rt= '-'
        else:
            af01_base_close = af01_close * 100 / (100 + af01_change)
            af01_open_rt = get_prrt(af01_base_close, af01_open)
            af01_high_rt = get_prrt(af01_base_close, af01_high)
            af01_low_rt  = get_prrt(af01_base_close, af01_low)
            af01_close_rt= get_prrt(af01_base_close, af01_close)

        bigo = get_bigo_adj(df.loc[bf60:af8w]['change'])

        datas = [
            (d_open_rt,    self.format_num_color)    #시가등락률
           ,(d_high_rt,    self.format_num_color)    #고가등락률
           ,(d_low_rt,     self.format_num_color)    #저가등락률
           ,(d_close_rt,   self.format_num_color)    #종가등락률
           ,(af01_open_rt, self.format_num_color)    #익일시가등락률
           ,(af01_high_rt, self.format_num_color)    #익일고가등락률
           ,(af01_low_rt,  self.format_num_color)    #익일저가등락률
           ,(af01_close_rt,self.format_num_color)    #익일종가등락률
           ,(close,        self.format_num)          #현재가(공시후 시가)
           ,(change,       self.format_num)          #현재등락률
           ,(bf60_rt,      self.format_num_color)    #60일등락률
           ,(bf30_rt,      self.format_num_color)    #30일전등락률
           ,(bf07_rt,      self.format_num_color)    #07일전등락률
           ,(d_change,     self.format_num_color)    #당일등락률
           ,(af1w_rt,      self.format_num_color)    #1주일후등락률
           ,(af2w_rt,      self.format_num_color)    #2주일후등락률
           ,(af3w_rt,      self.format_num_color)    #3주일후등락률
           ,(af4w_rt,      self.format_num_color)    #3주일후등락률
           ,(af5w_rt,      self.format_num_color)    #3주일후등락률
           ,(af6w_rt,      self.format_num_color)    #3주일후등락률
           ,(af7w_rt,      self.format_num_color)    #3주일후등락률
           ,(af8w_rt,      self.format_num_color)    #3주일후등락률
           ,(high_date,    None)                     #고가일자
           ,(high_ratio,   self.format_num_color)    #고가대비등락률
           ,(loss05date,   None)                     #5%로스컷일자
           ,(loss10date,   None)                     #10%로스컷일자
           ,(loss15date,   None)                     #15%로스컷일자
           ,(loss20date,   None)                     #20%로스컷일자
           ,(loss30date,   None)                     #30%로스컷일자
           ,(bigo,         None)                     #비고
        ]
        for index, data in enumerate(datas):
            sheet.write(row, column + index, data[0], data[1])
        return column + datas.__len__()    #입력한 개수

    def print_trade_sum(self, sheet, profit, losscut):
        """
        sheet.write(0, 15, 'WIN')
        sheet.write_formula('Q1', '=COUNTA(A8:A99999)-COUNTIF(M8:M99999, "-")')
        sheet.write_formula('R1', f'=Q1 * {profit}')
        sheet.write(1, 15, 'LOSS')
        sheet.write_formula('Q2', '=COUNTA(A8:A99999)-COUNTIF(N8:N99999, "-")')
        sheet.write_formula('R2', f'=Q2 *-{losscut}')
        sheet.write(2, 15, 'TIE')
        sheet.write_formula('Q3', '=COUNTA(A8:A99999) - Q1 - Q2')
        sheet.write_formula('R4', '=R1 + R2')
        """

        sheet.write_formula('Y6',  '=SUM(Y8:Y99999)')   #권리락전일
        sheet.write_formula('AA6', '=SUM(AA8:AA99999)') #신주상장일

        sheet.write_formula('AH6', '=SUM(AH8:AH99999)') #1주
        sheet.write_formula('AI6', '=SUM(AI8:AI99999)') #2주
        sheet.write_formula('AJ6', '=SUM(AJ8:AJ99999)') #3주
        sheet.write_formula('AK6', '=SUM(AK8:AK99999)') #4주
        sheet.write_formula('AL6', '=SUM(AL8:AL99999)') #5주
        sheet.write_formula('AM6', '=SUM(AM8:AM99999)') #6주
        sheet.write_formula('AO6', '=SUM(AO8:AO99999)') #수익률1
        sheet.write_formula('AQ6', '=SUM(AQ8:AQ99999)') #수익률2
        sheet.write_formula('AS6', '=SUM(AS8:AS99999)') #수익률3
        sheet.write_formula('AU6', '=SUM(AU8:AU99999)') #수익률4
        sheet.write_formula('AW6', '=SUM(AW8:AW99999)') #수익률5

    def print_trade(self, sheet, row, column, disc, profit, losscut):
        profit_date = ''
        losscut_date = ''
        high_date = ''
        high_ratio = ''

        rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()
        af01 = rcept_date + relativedelta(days = +1)

        df = get_ohlcv_pool(disc.corp.stock_code)
        d_close  = df.loc[rcept_date:].head(1)['close'].values[0]
        d_change = df.loc[rcept_date:].head(1)['change'].values[0]

        df_h = df.loc[af01:]['high']
        high_date, high = get_max_value(df_h)
        high_ratio = get_prrt(d_close, high)

        bigo = get_bigo_adj(df.loc[af01:]['change'])

        af1w = rcept_date + relativedelta(weeks  = +1)
        af2w = rcept_date + relativedelta(weeks  = +2)
        af3w = rcept_date + relativedelta(weeks  = +3)
        af4w = rcept_date + relativedelta(weeks  = +4)
        af5w = rcept_date + relativedelta(weeks  = +5)
        af6w = rcept_date + relativedelta(weeks  = +6)
        af7w = rcept_date + relativedelta(weeks  = +7)
        af8w = rcept_date + relativedelta(weeks  = +8)

        af1w_close, af1w_rt = get_d_prrt(df.loc[:af1w], d_close)
        af2w_close, af2w_rt = get_d_prrt(df.loc[:af2w], d_close)
        af3w_close, af3w_rt = get_d_prrt(df.loc[:af3w], d_close)
        af4w_close, af4w_rt = get_d_prrt(df.loc[:af4w], d_close)
        af5w_close, af5w_rt = get_d_prrt(df.loc[:af5w], d_close)
        af6w_close, af6w_rt = get_d_prrt(df.loc[:af6w], d_close)
        af7w_close, af7w_rt = get_d_prrt(df.loc[:af7w], d_close)
        af8w_close, af8w_rt = get_d_prrt(df.loc[:af8w], d_close)

        base_date  = get_content_value(disc.content,'신주배정기준일:')
        _base_date = None
        if base_date and base_date != '-':
            _base_date = remove_not_digit(base_date)
            _base_date = str_to_datetime(_base_date, '%Y%m%d').date()

            if df.loc[:_base_date].__len__() > 0:
                _base_date = df.loc[:_base_date].tail(3).index[0]

        sell_date1, sell_rt1 = buy_sell_strat1(disc, df, profit, losscut)
        sell_date2, sell_rt2 = buy_sell_strat2(disc, df, profit, losscut)
        sell_date3, sell_rt3 = buy_sell_strat3(disc, df, profit, losscut)
        sell_date4, sell_rt4 = buy_sell_strat4(disc, df, profit, losscut)
        sell_date5, sell_rt5 = buy_sell_strat5(disc, df, profit, losscut)
        profit_date, losscut_date = '-', '-'

        if not sell_rt1:
            pass
        elif sell_rt1 >= profit:
            profit_date = datetime_to_str(sell_date1,'%Y/%m/%d')
        elif sell_rt1 <= -losscut:
            losscut_date = datetime_to_str(sell_date1,'%Y/%m/%d')

        d_change = df.loc[rcept_date:].head(1)['change'].values[0]
        d_change = round(d_change,2)
        d_base_close = d_close * 100 / (100 + d_change)
        d_close_rt = get_prrt(d_base_close, d_close)

        sell_date1 = datetime_to_str(sell_date1,'%Y/%m/%d')
        sell_date2 = datetime_to_str(sell_date2,'%Y/%m/%d')
        sell_date3 = datetime_to_str(sell_date3,'%Y/%m/%d')
        sell_date4 = datetime_to_str(sell_date4,'%Y/%m/%d')
        sell_date5 = datetime_to_str(sell_date5,'%Y/%m/%d')

        datas = [
            (profit_date,  None),    #이익실현일자
            (losscut_date, None),    #로스컷일자
            (high_date,    None),    #고가일자
            (high_ratio,   self.format_num_color),    #고가대비등락률
            (d_close_rt,   self.format_num_color),    #종가등락률
            (af1w_rt,      self.format_num_color),    #1주일후 매도
            (af2w_rt,      self.format_num_color),    #2주일후 매도
            (af3w_rt,      self.format_num_color),    #3주일후 매도
            (af4w_rt,      self.format_num_color),    #4주일후 매도
            (af5w_rt,      self.format_num_color),    #5주일후 매도
            (af6w_rt,      self.format_num_color),    #6주일후 매도
            #(af7w_rt,      self.format_num_color),    #7주일후 매도
            #(af8w_rt,      self.format_num_color),    #8주일후 매도
            (sell_date1,   None),    #매도일자
            (sell_rt1,     self.format_num_color),    #수익률
            (sell_date2,   None),    #매도일자
            (sell_rt2,     self.format_num_color),    #수익률
            (sell_date3,   None),    #매도일자
            (sell_rt3,     self.format_num_color),    #수익률
            (sell_date4,   None),    #매도일자
            (sell_rt4,     self.format_num_color),    #수익률
            (sell_date5,   None),    #매도일자
            (sell_rt5,     self.format_num_color),    #수익률
            (bigo,         None),    #비고
        ]
        for index, data in enumerate(datas):
            sheet.write(row, column + index, data[0], data[1])
        return datas.__len__()    #입력한 개수
