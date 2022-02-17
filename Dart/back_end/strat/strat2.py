from strat.abstrat import AbstractStratFactory, AbstractProductStratKr
from strat.util import get_content_value, extract_key_value
from db.models import StdDisc, Disc
from dateutil.relativedelta import relativedelta
from commons.utils.datetime import str_to_datetime
from task.mfg.reproduce import get_ohlcv_pool
from commons.utils.parser import remove_not_digit

#ConcreteFactory1
class ConcreteStrat2Factory(AbstractStratFactory):
    strat = ''
    def __init__(self, strat, **kwargs):
        super().__init__()
        self.strat = strat

    def create_strat(self):
        return ConcreteProductStrat2(self.strat)

#ConcreteProductA
class ConcreteProductStrat2(AbstractProductStratKr):
    def __init__(self, strat, **kwargs):
        header_strat = [
            '배정비율',
            #'증자 전 수량',
            #'배정 수량',
            #'증자 후 수량',
            '신주배정기준일',
            '권리락전일 등락률',
            '신주의 상장 예정일',
            '신주의 상장 예정일 등락률',
            '이사회결의일(결정일)',
        ]
        super().__init__(strat, header_strat, **kwargs)

    # 1. 배정비율 50%이상
    def filter1(self, disc):
        if disc.report_nm.find('정정') >= 0:
            return False

        # 배정비율 50%이상만
        asgn_ratio = get_content_value(disc.content,'배정비율:')
        asgn_ratio = extract_key_value(asgn_ratio, '보통주식')
        asgn_ratio = asgn_ratio.replace('%','').replace('-','0')
        if int(asgn_ratio) < 50:
            return False

        return True

    # 1. filter2
    # 2. 장전,장후 제거 => 남들과 똑같은 시점에서 정보를 알고 주식을 사면 승률이 낮아짐
    # 3. 주요사항보고서(무상증자결정)
    def filter2(self, disc):
        if not self.filter1(disc):
            return False

        # 장전, 장후 제거
        #if disc.reg_time < '09:00' or disc.reg_time > '15:30':
        if disc.reg_time > '15:30':
            return False

        if disc.report_nm != '주요사항보고서(무상증자결정)':
            return False

        rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()
        bf01 = rcept_date + relativedelta(days = -1)

        df = get_ohlcv_pool(disc.corp.stock_code)
        if df.empty:
            avg_vol10 = 0
        else:
            values = df.loc[:bf01].tail(10)['volume'] * df.loc[:bf01].tail(10)['close']
        if values.__len__() > 0:
            avg_vol10 = round(sum(values) / len(values),2)
        else:
            avg_vol10 = 0

        # 최근10일 평균거래대금 1억이하 제거 (수정주가라서 정확한 금액이 안나옴)
        if avg_vol10 < 100000000:
            return False

        return True

    def print_header(self, sheet, headers, row = 0):
        for column, header in enumerate(headers):
            sheet.write(row, column, header)

    def print_filter(self, sheet, filtered):
        if   filtered == 'filtered1':
            matters = [
                '1. 배정비율 50% 이하제거',
            ]
        elif filtered == 'filtered2':
            matters = [
                '1. 배정비율 50% 이하제거',
                #'2. 장전, 장후 공시 제거',
                '2. 장후 공시 제거',
                '3. 주요사항보고서(무상증자결정)',
                '4. 거래대금1억이하 제거'
            ]
        else:
            matters = []

        for row, matter in enumerate(matters):
            sheet.write(row, 0, matter)

        return 6

    def print_strat(self, sheet, row, column, disc, figure):
        asgn_ratio = get_content_value(disc.content,'배정비율:')
        before_qty = get_content_value(disc.content,'증자 전 수량:')
        asgn_qty   = get_content_value(disc.content,'배정 수량:')
        after_qty  = get_content_value(disc.content,'증자 후 수량:')
        base_date  = get_content_value(disc.content,'신주배정기준일:')
        list_date  = get_content_value(disc.content,'신주의 상장 예정일:')
        decn_date  = get_content_value(disc.content,'이사회결의일(결정일):')

        if figure:
            asgn_ratio = extract_key_value(asgn_ratio, '보통주식')
            before_qty = extract_key_value(before_qty, '보통주식')
            asgn_qty   = extract_key_value(asgn_qty,   '보통주식')
            after_qty  = extract_key_value(after_qty,  '보통주식')
            try:
                asgn_ratio = float(asgn_ratio.replace('%','').replace('-','0')) /100
            except:
                print('except', asgn_ratio)

        rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()
        df = get_ohlcv_pool(disc.corp.stock_code)

        ex_right_rt = 0
        list_rt     = 0
        if df.loc[rcept_date:].__len__() > 0:
            d_close  = df.loc[rcept_date:].head(1)['close'].values[0]
            if base_date and base_date != '-':
                _base_date = remove_not_digit(base_date)
                _base_date  = str_to_datetime(_base_date, '%Y%m%d').date()
                if df.loc[:_base_date].__len__() > 0:
                    ex_right_close = df.loc[:_base_date].tail(3)['close'][0]
                    ex_right_rt = round((ex_right_close - d_close) / d_close * 100,2)
            if list_date and list_date != '-':
                #2021.01.03 -> 2021.02.05   로 표현하는 경우도 있음 
                idx = list_date.find('->')
                if idx < 0:
                    _list_date = list_date
                else:
                    _list_date = list_date[idx+2:]
                _list_date = remove_not_digit(_list_date)
                _list_date  = str_to_datetime(_list_date, '%Y%m%d').date()

                if df.loc[_list_date:].__len__() > 0:
                    list_close = df.loc[_list_date:].head(1)['close'].values[0]
                    list_rt    = round((list_close - d_close) / d_close * 100,2)

        datas = [(asgn_ratio, self.format_percent)    #배정비율
                #,(before_qty, None)  #증자 전 수량
                #,(asgn_qty,   None)  #배정 수량
                #,(after_qty,  None)  #증자 후 수량
                ,(base_date,   None)  #신주배정기준일
                ,(ex_right_rt, self.format_num_color)  #권리락전일 등락률
                ,(list_date,   None)  #신주의 상장 예정일
                ,(list_rt,     self.format_num_color)  #신주의 상장 예정일 등락률
                ,(decn_date,   None)  #이사회결의일(결정일)
        ]
        for index, data in enumerate(datas):
            sheet.write(row, column + index, data[0], data[1])

        return column + datas.__len__()    #입력한 개수

    def print_body_raw(self, sheet, row, disc):
        column = 0
        column = self.print_posted(sheet, row, column, disc)    #공시시점
        column = self.print_stock (sheet, row, column, disc)    #주식정보
        column = self.print_rechg (sheet, row, column, disc)    #최근등락률
        column = self.print_strat (sheet, row, column, disc, False)
        column = self.print_after (sheet, row, column, disc)    #주가변동추이

    def print_body_filter(self, sheet, row, disc):
        column = 0
        column = self.print_posted(sheet, row, column, disc)    #공시시점
        column = self.print_stock (sheet, row, column, disc)    #주식정보
        column = self.print_rechg (sheet, row, column, disc)    #최근등락률
        column = self.print_strat (sheet, row, column, disc, True)
        column = self.print_after (sheet, row, column, disc)    #주가변동추이

    def print_body_trade(self, sheet, row, disc, profit, losscut):
        column = 0
        column = self.print_posted(sheet, row, column, disc)    #공시시점
        column = self.print_stock (sheet, row, column, disc)    #주식정보
        column = self.print_rechg (sheet, row, column, disc)    #최근등락률
        column = self.print_strat (sheet, row, column, disc, True)
        column = self.print_trade (sheet, row, column, disc, profit, losscut)

    def sheet_set_column(self, sheet, sheetname):
        if 'raw' in sheetname:
            sheet.freeze_panes(1, 0)
        if 'filtered' in sheetname:
            sheet.freeze_panes('E8')
        if '목표' in sheetname:
            sheet.freeze_panes(7, 0)

        if 'raw' in sheetname or 'filtered' in sheetname:
            sheet.set_column('A:A',   16)
            sheet.set_column('B:B',    4)
            sheet.set_column('D:D',   12)
            sheet.set_column('E:E',   16)

            sheet.set_column('G:G',   10)
            sheet.set_column('H:H',    7)
            sheet.set_column('I:I',   10)
            sheet.set_column('J:J',    7)
            sheet.set_column('K:K',   10)
            sheet.set_column('L:L',    7)
            sheet.set_column('M:M',   10)
            sheet.set_column('N:N',    7)

            sheet.set_column('O:T',    5)
            sheet.set_column('U:U',   10)
            sheet.set_column('V:V',    6)
            sheet.set_column('W:X',   10)
            sheet.set_column('Y:Y',    5)
            sheet.set_column('Z:Z',   10)
            sheet.set_column('AA:AA',  5)
            sheet.set_column('AB:AB', 10)

            sheet.set_column('AC:AJ',  5)
            sheet.set_column('AK:AK', 10)
            sheet.set_column('AL:AX',  5)
            sheet.set_column('AY:AY', 10)
            sheet.set_column('AZ:AZ',  5)
            sheet.set_column('BA:BE',  7)
            sheet.set_column('BF:BF', 20)
        elif '목표' in sheetname:
            sheet.set_column('A:A',   16)
            sheet.set_column('B:B',    4)
            sheet.set_column('D:D',   12)
            sheet.set_column('E:E',   16)

            sheet.set_column('G:G',   10)
            sheet.set_column('H:H',    6)
            sheet.set_column('I:I',   10)
            sheet.set_column('J:J',    6)
            sheet.set_column('K:K',   10)
            sheet.set_column('L:L',    6)
            sheet.set_column('M:M',   10)
            sheet.set_column('N:N',    6)

            sheet.set_column('O:T',    5)
            sheet.set_column('U:U',   10)
            sheet.set_column('V:V',    6)
            sheet.set_column('W:X',   10)
            sheet.set_column('Y:Y',    5)
            sheet.set_column('Z:Z',   10)
            sheet.set_column('AA:AA',  5)
            sheet.set_column('AB:AB', 10)
            sheet.set_column('AC:AD', 10)
            sheet.set_column('AF:AM',  6)

            sheet.set_column('AN:AN', 10)
            sheet.set_column('AO:AO',  5)
            sheet.set_column('AP:AP', 10)
            sheet.set_column('AQ:AQ',  5)
            sheet.set_column('AR:AR', 10)
            sheet.set_column('AS:AS',  5)
            sheet.set_column('AT:AT', 10)
            sheet.set_column('AU:AU',  5)
            sheet.set_column('AV:AV', 10)
            sheet.set_column('AW:AW',  5)
            sheet.set_column('AX:AX', 20)

    def print_sheet_raw(self, discs, workbook):
        print('print_sheet_raw')
        sheet = workbook.add_worksheet('raw')
        self.sheet_set_column(sheet, 'raw')

        self.print_header(sheet, self.header_raw, 0)
        row = 1
        for disc in discs:
            self.print_body_raw(sheet, row, disc)
            row = row + 1

    def print_filter_sum(self, sheet):
        sheet.write_formula('AQ6', '=SUM(AQ8:AQ9999)')
        sheet.write_formula('AR6', '=SUM(AR8:AR9999)')
        sheet.write_formula('AS6', '=SUM(AS8:AS9999)')
        sheet.write_formula('AT6', '=SUM(AT8:AT9999)')
        sheet.write_formula('AU6', '=SUM(AU8:AU9999)')
        sheet.write_formula('AV6', '=SUM(AV8:AV9999)')
        sheet.write_formula('AW6', '=SUM(AW8:AW9999)')
        sheet.write_formula('AX6', '=SUM(AX8:AX9999)')

    def print_sheet_filter(self, discs, workbook, sheetname, filtering):
        print('print_sheet_filter', sheetname)
        sheet = workbook.add_worksheet(sheetname)
        self.sheet_set_column(sheet, sheetname)

        row = self.print_filter(sheet, sheetname)
        self.print_filter_sum(sheet)

        self.print_header(sheet, self.header_filter, row)

        row = row + 1
        for disc in discs:
            if not filtering(disc):
                continue
            self.print_body_filter(sheet, row, disc)
            row = row + 1

    def print_sheet_trade(self, discs, workbook, trades):
        for trade in trades:
            profit, losscut = trade
            sheetname = f'목표{profit}%로스컷{losscut}%'
            print('print_sheet_trade', sheetname)
            sheet = workbook.add_worksheet(sheetname)
            self.sheet_set_column(sheet, sheetname)
            sheet.write(0, 0, 'filtered2 대상')
            sheet.write(1, 0, '전략1: 로스컷, 목표수익률, 1주뒤 음수, 4주후')
            sheet.write(1, 4, '전략2: 로스컷, 목표수익률, 2주뒤 음수, 4주후')
            sheet.write(2, 0, '전략3: 1주뒤 음수, 4주후')
            sheet.write(2, 4, '전략4: 2주뒤 음수, 4주후')
            sheet.write(3, 0, '전략5: 1주뒤 음수면 로스컷 체크, 2주뒤 음수, 4주후')

            self.print_trade_sum(sheet, profit, losscut)
            self.print_header(sheet, self.header_trade, 6)

            sheet.set_column('G:G', None, None, {'hidden': True})
            sheet.set_column('I:I', None, None, {'hidden': True})
            sheet.set_column('K:K', None, None, {'hidden': True})
            sheet.set_column('M:M', None, None, {'hidden': True})
            sheet.set_column('O:T', None, None, {'hidden': True})
            sheet.set_column('U:U', None, None, {'hidden': True})
            sheet.set_column('X:X', None, None, {'hidden': True})
            sheet.set_column('Z:Z', None, None, {'hidden': True})
            sheet.set_column('AB:AB', None, None, {'hidden': True})
            sheet.set_column('AE:AE', None, None, {'hidden': True})
            sheet.set_column('AF:AF', None, None, {'hidden': True})
            sheet.set_column('AL:AL', None, None, {'hidden': True})
            sheet.set_column('AM:AM', None, None, {'hidden': True})
            row = 7
            for disc in discs:
                if not self.filter2(disc):
                    continue
                self.print_body_trade(sheet, row, disc, profit, losscut)
                row = row + 1

    def do_simula(self, begin, end):
        discs = Disc.objects.raw({
            'rcept_dt':{'$gte':begin,'$lte':end},
            'report_nm':{'$regex':'상증자결정'}
        }).raw({
            'report_nm':{'$regex':'무'}
        }).order_by([('rcept_dt',1)])

        if discs.count() == 0:
            return

        workbook = self.new_workbook()

        self.print_sheet_raw(discs, workbook)
        self.print_sheet_filter(discs, workbook, 'filtered1', self.filter1)
        self.print_sheet_filter(discs, workbook, 'filtered2', self.filter2)

        trades = [
          #  ( 5,5),
          #  (10,5), (10,10),
          #  (15,5), (15,10), (15,15),
            (20,10), (20,15), (20,20),
            (30,10), (30,15), (30,20), #(30,30),
            (40,10), (40,15), (40,20), #(40,30), (40,40),
            (50,10), (50,15), (50,20), #(50,30), (50,40), (50,50),
          # (60,5), (60,10), (60,15), (60,20), (60,30), (60,40), (60,50),
          # (70,5), (70,10), (70,15), (70,20), (70,30), (70,40), (70,50),
          # (80,5), (80,10), (80,15), (80,20), (80,30), (80,40), (80,50),
          # (90,5), (90,10), (90,15), (90,20), (90,30), (90,40), (90,50),
          #(100,5),(100,10),(100,15),(100,20),(100,30),(100,40),(100,50),
        ]
        self.print_sheet_trade(discs, workbook, trades)

        workbook.close()

