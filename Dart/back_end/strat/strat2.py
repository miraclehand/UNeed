from strat.abstrat import AbstractStratFactory, AbstractProductStratKr
from strat.util import get_content_value
from db.models import StdDisc, Disc

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
    headers = []

    def __init__(self, strat, **kwargs):
        super().__init__(strat, **kwargs)

        self.headers  = self.header1    #공통-공시
        self.headers += [
            '배정비율',
            '증자 전 수량',
            '배정 수량',
            '증자 후 수량',
            '신주배정기준일',
            '신주의 상장 예정일',
            '이사회결의일(결정일)',
        ]
        self.headers += self.header2    #공통-공시후 가격추이

    def print_header(self, sheet):
        row = 0

        for column, header in enumerate(self.headers):
            sheet.write(row, column, header)

    def print_body(self, sheet, row, disc):
        #공통1
        column = 0
        column = self.print_body1(sheet, row, column, disc)    #공통1

        asgn_ratio = get_content_value(disc.content,'배정비율:')
        before_qty = get_content_value(disc.content,'증자 전 수량:')
        asgn_qty   = get_content_value(disc.content,'배정 수량:')
        after_qty  = get_content_value(disc.content,'증자 후 수량:')
        base_date  = get_content_value(disc.content,'신주배정기준일:')
        list_date  = get_content_value(disc.content,'신주의 상장 예정일:')
        decn_date  = get_content_value(disc.content,'이사회결의일(결정일):')

        sheet.write(row, column + 0, asgn_ratio)   #배정비율
        sheet.write(row, column + 1, before_qty)   #증자 전 수량
        sheet.write(row, column + 2, asgn_qty)     #배정 수량
        sheet.write(row, column + 3, after_qty)    #증자 후 수량
        sheet.write(row, column + 4, base_date)    #신주배정기준일
        sheet.write(row, column + 5, list_date)    #신주의 상장 예정일
        sheet.write(row, column + 6, decn_date)    #이사회결의일(결정일)

        column = column + 7
        column = self.print_body2(sheet, row, column, disc)    #공통2

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
        sheet = workbook.add_worksheet('raw')

        self.print_header(sheet)
        row = 1
        for disc in discs:
            if disc.report_nm.find('첨부정정') >= 0:
                continue
            self.print_body(sheet, row, disc)
            row = row + 1

        workbook.close()

