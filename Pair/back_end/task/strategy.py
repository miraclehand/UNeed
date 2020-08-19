import pandas as pd
import numpy as np
import abc
from datetime import datetime, timedelta
from constants import *
from utils.datetime import str_to_datetime
from task.singleton import pool_ohlcv, pool_variant
from task.mfg.reproduce import get_ohlcv_pool
from task.mfg.reproduce import target_field
from task.mfg.entry import calc_cost, calc_yield
from db.models import StockKr, CandleKr, PickedPairKr
from db.models import StockUs, CandleUs, PickedPairUs
from db.models import BasketKr, EntryKr, StrainerKr
from db.models import BasketUs, EntryUs, StrainerUs
from db.models import TradingReportKr, SimulaReportKr
from db.models import TradingReportUs, SimulaReportUs

#import plotly.plotly as py

# Abstract Factory Pattern
#AbstractFactory
class AbstractStrategyFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_trading_report(self):
        pass

    @abc.abstractmethod
    def create_simula_report(self):
        pass

    @classmethod
    def get_factory(self, cntry):
        if cntry == 'kr':
            return ConcreteStrategyKrFactory()
        if cntry == 'us':
            return ConcreteStrategyUsFactory()
        return None

#ConcreteFactory1
class ConcreteStrategyKrFactory(AbstractStrategyFactory):
    def create_trading_report(self):
        return ConcreteProductTradingReportKr()

    def create_simula_report(self):
        return ConcreteProductSimulaReportKr()

#ConcreteFactory2
class ConcreteStrategyUsFactory(AbstractStrategyFactory):
    def create_trading_report(self):
        return ConcreteProductTradingReportUs()

    def create_simula_report(self):
        return ConcreteProductSimulaReportUs()

class AbstractProductStrategy(metaclass=abc.ABCMeta):
    username = None
    Stock    = None
    Basket   = None
    Entry    = None
    Strainer = None
    Report   = None

    def __init__(self, Stock, Basket, Entry, Strainer, Report, **kwargs):
        super().__init__(**kwargs)

        self.Stock    = Stock
        self.Basket   = Basket
        self.Entry    = Entry
        self.Strainer = Strainer
        self.Report   = Report

    def setup(self, username):
        self.username = username

    def get_report_seq(self):
        today = datetime.today().date()
        create_date = datetime(year=today.year,month=today.month,day=today.day)

        report = self.get_last_report()

        if report and report.create_date == create_date:
            seq = report.seq + 1
        else:
            seq = 1
        return create_date, seq

    def new_trading_report(self, strainer):
        create_date, seq = self.get_report_seq()

        report = self.Report(self.username, create_date, seq)
        if strainer:
            report.strainer = strainer
        report.save()

        return report

    def new_simula_report(self, date1, date2, strainer):
        create_date, seq = self.get_report_seq()

        report = self.Report(self.username, create_date, seq)

        report.date1 = date1
        report.date2 = date2
        report.save()

        report = self.get_last_report()
        strainer.name = str(report._id)
        strainer.label = strainer.name

        report.strainer = strainer
        report.save()

        return report

    def get_last_report(self):
        reports = self.Report.objects.raw({'username':{'$eq':self.username}})
        reports = reports.order_by([('create_date',-1),('seq',-1)])

        if reports.count() > 0:
            return reports.first()
        else:
            return None

    def get_open_entries(self):
        report = self.get_last_report()

        if not report:
            return []

        entries = []
        for entry in report.entries:
            if not entry.Long.exit_date:
                entries.append(entry)

        return entries

    def get_all_entries(self, Report):
        report = self.get_last_report()

        if not report:
            return []

        return report.entries

    def new_basket(self, stock, pos, date, uv, qty):
        if isinstance(stock, str):
            stock = self.Stock.objects.get({'code':stock})
        if isinstance(uv, str):
            uv = int(uv)
        if isinstance(qty, str):
            qty = int(qty)
        if isinstance(date, str):
            date = str_to_datetime(date, '%Y-%m-%d')

        amt = uv * qty

        cost = calc_cost(stock, pos, amt)

        return self.Basket(stock, pos, date, uv, qty, amt, cost)

    def new_entry(self, basket1, basket2):
        if basket1.pos == '+':
            coint = basket2.entry_amt / basket1.entry_amt
            Long  = basket1
            Short = basket2
        else:
            coint = basket1.entry_amt / basket2.entry_amt
            Long  = basket2
            Short = basket1

        Long.coint = 1
        Short.coint = coint

        Long.label  = '%s(+%d)'   % (Long.stock.name, 1)
        Short.label = '%s(-%.2f)' % (Short.stock.name, coint)

        label = '%s(+1)-%s(-%.2f)' % (Long.stock.name, Short.stock.name, coint)

        # generate entry_id
        report = self.get_last_report()
        if report:
            entry_id = report.entries.__len__() + 1
        else:
            entry_id = 1

        return self.Entry(entry_id, Long, Short, coint, label)

#AbstractProductA
class AbstractProductSimulaReport(AbstractProductStrategy):
    Candle = None
    PickedPair = None

    entries  = None
    strainer = None

    def __init__(self, Stock, Candle, PickedPair, Basket, Entry, Strainer, Report, **kwargs):
        super().__init__(Stock, Basket, Entry, Strainer, Report, **kwargs)
        self.Candle = Candle
        self.PickedPair = PickedPair

    def set_strainer(self, strainer):
        self.strainer = strainer

    def get_close(self, code, date):
        if isinstance(date, datetime): date = date.date()

        df = get_ohlcv_pool(self.Candle, code)

        if date not in df.index:
            return 0
        close = df.loc[date]['close']

        return close

    def strat_buy(self, pair):
        # 이미 보유하고 있으면 return
        for entry in self.entries:
            if not pair.stock1 in (entry.Long.stock, entry.Short.stock):
                continue
            if not pair.stock2 in (entry.Long.stock, entry.Short.stock):
                continue
            if entry.Long.exit_date or entry.Short.exit_date:
                continue
            return None
                
        fig_str = pair.fig_str
        stock1  = pair.stock1
        stock2  = pair.stock2
        date1   = pair.date2
        date2   = pair.date2
        close1  = pair.close1
        close2  = pair.close2

        if not close1 or not close2:
            return None

        #stock filter
        if self.strainer.close > close1:
            return None

        if self.strainer.close > close2:
            return None

        """
        df1 = get_ohlcv_pool(self.Candle, stock1.code)
        df2 = get_ohlcv_pool(self.Candle, stock2.code)

        date = date2.date()
        df1 = df1[(df1.index <= date)]
        df2 = df2[(df2.index <= date)]

        avg1 = np.average(df1.close)
        avg2 = np.average(df2.close)

        if self.strainer.avg_v50 > avg1:
            return None

        if self.strainer.avg_v50 > avg2:
            return None
        """

        #1:보통주, 2:보통주+우선주
        if self.strainer.stock_type == 1:
            if stock1.code[5] != '0' or stock2.code[5] != '0':
                return None

        #1:같은산업, 2:모든산업
        if self.strainer.stock_ind == 1:
            if not target_field(stock1, stock2):
                return None

        if stock1.industry in self.strainer.stock_exc_ind:
            return None

        if stock2.industry in self.strainer.stock_exc_ind:
            return None

        #pair spread
        if self.strainer.density < fig_str.density:
            return None

        place = fig_str.place / fig_str.place_cnt
        if self.strainer.place < place < 1 - self.strainer.place:
            return None

        if not 1 - self.strainer.coint < fig_str.coint_calc < 1 + self.strainer.coint:
            return None

        if self.strainer.coint_std < pair.coint_std:
            return None

        if self.strainer.dist_yield > abs(fig_str.value):
            return None

        if self.strainer.hit0_cnt > fig_str.hit0_cnt:
            return None

        if self.strainer.cy10_cnt > fig_str.cy10_cnt:
            return None

        if self.strainer.cy20_cnt > fig_str.cy20_cnt:
            return None

        #pair null hypothese test
        if self.strainer.ks_pvalue > fig_str.ks_pvalue:
            return None

        if self.strainer.adf_pvalue <= fig_str.adf_pvalue:
            return None

        if self.strainer.coint_pvalue <= fig_str.coint_pvalue:
            return None

        if fig_str.value < 0:
            #A저평가, B고평가
            pos1 = '+'
            pos2 = '-'
        else:
            #A고평가, B저평가
            pos1 = '-'
            pos2 = '+'

        if pos1 == '+':
            qty1 = 100
            qty2 = int(close1 * qty1 * fig_str.coint_calc / close2)
        else:
            qty2 = 100
            qty1 = int(close2 * qty2 * 1 / fig_str.coint_calc / close1)

        basket1 = self.new_basket(stock1, pos1, date1, close1, qty1)
        basket2 = self.new_basket(stock2, pos2, date2, close2, qty2)
        entry   = self.new_entry(basket1, basket2)
        return entry

    def strat_sell(self, date):
        for entry in self.entries:
            if entry.Long.exit_date or entry.Short.exit_date:
                continue

            entry_date  = min(entry.Long.entry_date, entry.Short.entry_date)

            days = (date - entry_date).days

            L_exit_uv = self.get_close(entry.Long.stock.code,  date)
            S_exit_uv = self.get_close(entry.Short.stock.code, date)

            #continue if weekend
            if 0 in (L_exit_uv, S_exit_uv):
                continue
            yld = calc_yield(entry, L_exit_uv, S_exit_uv)

            if days < self.strainer.days and self.strainer.loss_yield < yld <  self.strainer.clear_yield:
                continue

            entry.Long.exit_date  = date
            entry.Long.exit_uv    = L_exit_uv
            entry.Short.exit_date = date
            entry.Short.exit_uv   = S_exit_uv
            entry.yld = yld
            return entry
        return None

    def play(self, date1, date2):
        if isinstance(date1, str): date1 = datetime.strptime(date1, '%Y-%m-%d')
        if isinstance(date2, str): date2 = datetime.strptime(date2, '%Y-%m-%d')

        start = datetime.now()
        report = self.new_simula_report(date1, date2, self.strainer)

        delta = date2 - date1
        self.entries = list()

        progress = 0
        progress_day = 1 / delta.days * 100
        for i in range(delta.days + 1):
            if not pool_variant.get('simula_valid'):
                break

            date = date1 + timedelta(i)
            print(date)

            pairs = self.PickedPair.objects.raw({'date2':{'$eq':date}})
            pair_cnt = pairs.count()

            entry = self.strat_sell(date)
            if entry:
                report.yld += entry.yld
                print('EXIT', date.date(), entry.Long.stock.label, entry.Short.stock.label, entry.Long.entry_uv, entry.Short.entry_uv, entry.coint, entry.Long.exit_uv, entry.Short.exit_uv)
                continue

            for j, pair in enumerate(pairs):
                if j % 20 == 0:
                    report.progress = progress + progress_day * j / pair_cnt
                    report.seconds  = (datetime.now() -  start).seconds
                    report.save()

                entry = self.strat_buy(pair)
                if not entry:
                    continue

                self.entries.append(entry)
                print('ENTRY', date.date(), entry.Long.stock.label, entry.Short.stock.label, entry.Long.entry_uv, entry.Short.entry_uv, entry.coint)
            progress = i / delta.days * 100

            report.progress = progress
            report.seconds  = (datetime.now() -  start).seconds
            report.save()

        if not pool_variant.get('simula_valid'):
            report.progress = 100
            report.valid = True
        else:
            report.valid = False

        report.seconds = (datetime.now() -  start).seconds
        if self.entries:
            report.entries = self.entries
        report.save()
        pool_ohlcv.clear()
        pool_variant.set('simula_valid', True)

#ConcreteProductA
class ConcreteProductSimulaReportKr(AbstractProductSimulaReport):
    def __init__(self, **kwargs):
        super().__init__(StockKr, CandleKr, PickedPairKr, BasketKr, EntryKr, StrainerKr, SimulaReportKr, **kwargs)

#ConcreteProductB
class ConcreteProductSimulaReportUs(AbstractProductSimulaReport):
    def __init__(self, **kwargs):
        super().__init__(StockUs, CandleUs, PickedPairUs, BasketUs, EntryUs, StrainerUs, SimulaReportUs, **kwargs)

#AbstractProductA
class AbstractProductTradingReport(AbstractProductStrategy):
    def __init__(self, Stock, Basket, Entry, StrainerKr, Report, **kwargs):
        super().__init__(Stock, Basket, Entry, StrainerKr, Report, **kwargs)

    def open_entry(self, basket1, basket2):
        try:
            report = self.Report.objects.get({'username':self.username})
        except:
            today = datetime.today()
            date2 = datetime(year=today.year, month=today.month, day=today.day)
            date2 = datetime(year=3000, month=12, day=31)
            report = self.new_trading_report(None)

        entry = self.new_entry(basket1, basket2)
        report.entries.append(entry)
        report.save()

    def close_entry(self, entry_id, L_exit_uv, S_exit_uv):
        try:
            report = self.Report.objects.get({'username':self.username})
        except:
            return

        today  = datetime.today()
        date   = datetime(year=today.year, month=today.month, day=today.day)

        for i, entry in enumerate(report.entries):
            if str(entry.entry_id) != entry_id:
                continue
            entry.Long.exit_date  = date
            entry.Long.exit_uv    = L_exit_uv
            entry.Short.exit_date = date
            entry.Short.exit_uv   = S_exit_uv
            entry.yld = calc_yield(entry, L_exit_uv, S_exit_uv)

            report.entries[i] = entry
            report.yld = report.yld + entry.yld
            report.save()
            break

#ConcreteProductA
class ConcreteProductTradingReportKr(AbstractProductTradingReport):
    def __init__(self, **kwargs):
        super().__init__(StockKr, BasketKr, EntryKr, StrainerKr, TradingReportKr, **kwargs)

#ConcreteProductB
class ConcreteProductTradingReportUs(AbstractProductTradingReport):
    def __init__(self, **kwargs):
        super().__init__(StockUs, BasketUs, EntryUs, StrainerUs, TradingReportUs, **kwargs)


#페어가 잘 맞는 놈들은 coint of std가 작고
#위아래롤 흔들리는 수가 1년에 4번 이상
if __name__ == '__main__':
    date1 = datetime(2017, 12, 28, 0, 0)
    date2 = datetime(2019,  8, 16, 0, 0)

    factory = AbstractStrategyFactory.get_factory('kr')
    report = factory.create_simula_report()
    report.setup(None, None)
    report.make_model(date1, date2)

