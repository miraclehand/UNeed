import pandas as pd
import statsmodels.tsa.stattools as ts
import numpy as np
import requests
import abc
from calendar import monthrange
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from utils.datetime import add_year
from constants import *

from basedb.models import Stock, StockKr, StockUs
from basedb.models import Candle, CandleKr, CandleUs

from app import app
from db.models import Figure
from db.models import PickedPairKr, NodePairKr
from db.models import PickedPairUs, NodePairUs
from task.mfg.reproduce import get_valid_ohlcv_pool, get_df_spread
from task.mfg.reproduce import get_ohlcv_db, get_valid_intxn
from task.mfg.reproduce import get_valid_dfs_pool, get_dfs_pool
from task.mfg.reproduce import get_norm, get_corr
from task.mfg.reproduce import target_field
from task.mfg.reproduce import get_stocks_kr, get_stocks_us
from task.mfg.reproduce import valid_data
from task.mfg.figure import figure_coint_calc, figure_test
from task.mfg.figure import figure_density, figure_place, figure_pam

#import plotly.plotly as py

# Abstract Factory Pattern
#AbstractFactory
class AbstractPairFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_node_pair(self):
        pass

    @abc.abstractmethod
    def create_picked_pair(self):
        pass

    @classmethod
    def get_factory(self, cntry):
        if cntry == 'kr':
            return ConcretePairKrFactory()
        if cntry == 'us':
            return ConcretePairUsFactory()
        return None

#ConcreteFactory1
class ConcretePairKrFactory(AbstractPairFactory):
    def create_node_pair(self):
        return ConcreteProductNodePairKr()

    def create_picked_pair(self):
        return ConcreteProductPickedPairKr()

#ConcreteFactory2
class ConcretePairUsFactory(AbstractPairFactory):
    def create_node_pair(self):
        return ConcreteProductNodePairUs()

    def create_picked_pair(self):
        return ConcreteProductPickedPairUs()

class AbstractProductPair(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def make_model(self, date1, date2):
        pass

    @abc.abstractmethod
    def new_model(self, date1, date2, stock1, stock2, df1, df2):
        pass

    @abc.abstractmethod
    def del_model(self, date):
        pass

    @abc.abstractmethod
    def del_models(self):
        pass
    
    @abc.abstractmethod
    def set_stocks(self, stocks):
        pass

#AbstractProductA
class AbstractProductNodePair(AbstractProductPair):
    Candle     = None
    NodePair   = None
    stocks = None

    def __init__(self, Candle, NodePair, **kwargs):
        super().__init__(**kwargs)
        self.Candle   = Candle
        self.NodePair = NodePair

    @abc.abstractmethod
    def make_model(self, date1, date2):
        self.del_model(date2)

        tot = self.stocks.__len__()
        print('make_model', tot )
        cnt = 0
        for i, stock1 in enumerate(self.stocks):
            start = datetime.now()
            print(date2.date(), i, '/', tot , stock1.code, stock1.name, end=' ')

            # 2년의 영업일은 488일
            df1 = get_valid_ohlcv_pool(self.Candle, stock1.code, 450)
            if df1 is None:
                print('===>(None)', 0, datetime.now() - start)
                continue

            for j, stock2 in enumerate(self.stocks):
                if i >= j:
                    continue
                # 두 주식 모두 ETF를 따르면, 의미 없는 데이터
                if stock1.aimed == stock2.aimed == 'ETF':
                    continue
                if not target_field(stock1, stock2):
                    continue

                # 2년의 영업일은 488일
                df2 = get_valid_ohlcv_pool(self.Candle, stock2.code, 450)
                if df2 is None:
                    continue

                df1, df2 = get_valid_intxn(date1, date2, df1, df2, 1.8)
                if df1 is None or df2 is None:
                    continue

                """
                ohlcvs1 = df1[-50:]
                ohlcvs2 = df2[-50:]

                avg1_50 = int(np.average(ohlcvs1['close'] * ohlcvs1['volume']))
                avg2_50 = int(np.average(ohlcvs2['close'] * ohlcvs2['volume']))

                if avg1_50 < 2000 * 1000000 or avg2_50 < 2000 * 1000000:
                    continue
                """

                node_pair = self.new_model(date1,date2, stock1,stock2, df1,df2)
                if node_pair:
                    node_pair.save()
                    cnt = cnt + 1

            print('===>', cnt, datetime.now() - start)
        return cnt

    def new_model(self, date1, date2, stock1, stock2, df1, df2):
        if df1 is None or df2 is None:
            return None

        # collelation
        norm1, norm2 = get_norm(df1, df2) 
        corr = get_corr(norm1, norm2)
        if not corr or corr < 0.8:
            return None

        node_pair = self.NodePair(date1, date2, stock1, stock2)
        node_pair.corr = corr
        #node_pair.coint_pvalue = ts.coint(df1['log'], df2['log'])[1]
        return node_pair

        """
        # cointegration (straight)
        coint_pvalue = ts.coint(df1['log'], df2['log'])[1]
        if coint_pvalue <= 0.1:
            node_pair = self.NodePair(date1, date2, stock1, stock2)
            node_pair.corr = corr
            node_pair.coint_pvalue = coint_pvalue
            return node_pair

        # cointegration (reverse)
        coint_pvalue = ts.coint(df2['log'], df1['log'])[1]
        if coint_pvalue <= 0.1:
            node_pair = self.NodePair(date1, date2, stock1, stock2)
            node_pair.corr = corr
            node_pair.coint_pvalue = coint_pvalue
            return node_pair
        return None
        """

    def del_model(self, date):
        self.NodePair.objects.raw({'date2':{'$eq':date}}).delete()

    def del_models(self):
        self.NodePair.objects.delete()

    def set_stocks(self, stocks):
        self.stocks = stocks

#ConcreteProductA
class ConcreteProductNodePairKr(AbstractProductNodePair):
    def __init__(self, **kwargs):
        super().__init__(CandleKr, NodePairKr, **kwargs)

    def make_model(self, date1, date2):
        if date2.weekday() != 4:     # this func execute every friday
            return None

        self.set_stocks(get_stocks_kr())

        return super().make_model(date1, date2)

#ConcreteProductB
class ConcreteProductNodePairUs(AbstractProductNodePair):
    def __init__(self, **kwargs):
        super().__init__(CandleUs, NodePairUs, **kwargs)

    def make_model(self, date1, date2):
        if date2.weekday() != 4:     # this func execute every friday
            return None

        self.set_stocks(get_stocks_us())

        return super().make_model(date1, date2)

class AbstractProductPickedPair(AbstractProductPair):
    cntry      = 'kr'
    Candle     = None
    NodePair   = None
    PickedPair = None
    stocks = None
    pers = dict()

    def __init__(self, cntry, **kwargs):
        super().__init__(**kwargs)
        self.cntry = cntry

        if self.cntry == 'kr':
            self.Candle     = CandleKr
            self.NodePair   = NodePairKr
            self.PickedPair = PickedPairKr
        if self.cntry == 'us':
            self.Candle     = CandleUs
            self.NodePair   = NodePairUs
            self.PickedPair = PickedPairUs

    @abc.abstractmethod
    def make_model(self, date1, date2):
        self.del_model(date2)

        try:
            node = self.NodePair.objects.raw({'date2':{'$lte':date2}}).order_by([('date1',-1)]).first()
        except Exception as ex:
            print ('not found NodePair', date1, date2)
            return None

        print('node_date', node.date1, node.date2)

        nodes = self.NodePair.objects.raw({'date2':{'$eq':node.date2}})
        tot = nodes.count()
        cnt = 0
        print('total count => ', tot)
        url = app.config['URL_COLLECTOR'] + '/api/crawler/company/{}/{}'

        for i, node in enumerate(nodes):
            print(date2.date(), i, '/', tot, end=' ')
            start = datetime.now()
            stock1, stock2 = node.stock1, node.stock2
            # TODO 이런 경우가 왜 있지?
            if not stock1 or not stock2:
                continue

            """
            if not target_field(stock1, stock2):
                print()
                continue
            """

            if stock1.code not in self.pers:
                company = requests.get(url.format(self.cntry, stock1.code)).json()['company']
                if company:
                    self.pers[stock1.code] = company['per']
                else:
                    self.pers[stock1.code] = 'N/A'
            if stock2.code not in self.pers:
                company = requests.get(url.format(self.cntry, stock2.code)).json()['company']
                if company:
                    self.pers[stock2.code] = company['per']
                else:
                    self.pers[stock2.code] = 'N/A'

            df1, df2 = get_valid_dfs_pool(self.Candle, date1, date2, stock1.code, stock2.code, 1.8)

            # straight
            picked_pair = self.new_model(date1, date2, stock1, stock2, df1, df2)
            if picked_pair:
                print(stock1.label, stock2.label, end=' ')
                picked_pair.save()
                cnt = cnt + 1
                print('==>', datetime.now() - start)
                continue

            # reverse
            picked_pair = self.new_model(date1, date2, stock2, stock1, df2, df1)
            if picked_pair:
                print(stock2.label, stock1.label, end=' ')
                picked_pair.save()
                cnt = cnt + 1
                print('==>', datetime.now() - start)
                continue
            print()
        return cnt

    def new_model(self, date1, date2, stock1, stock2, df1, df2):
        if df1 is None or df2 is None:
            return None

        coint_calc1, dfs1  = self.get_figure_coint_calc(df1, df2)
        place1, place_cnt1 = self.get_figure_place(dfs1)

        if not 0.5 <= coint_calc1 <= 2:
            return None

        if 0.05 < place1 / place_cnt1 < 0.95:
            return None

        coint_calc2, dfs2  = self.get_figure_coint_calc(df2, df1)
        place2, place_cnt2 = self.get_figure_place(dfs2)

        fig1 = self.new_figure(df1, df2, dfs1, coint_calc1, place1, place_cnt1)
        fig2 = self.new_figure(df2, df1, dfs2, coint_calc2, place2, place_cnt2)

        pair = self.PickedPair(date1, date2, stock1, stock2)
        pair.close1 = df1['close'][-1]
        pair.close2 = df2['close'][-1]
        pair.fig_str = fig1
        pair.fig_rev = fig2

        norm1, norm2 = get_norm(df1, df2) 
        corr = get_corr(norm1, norm2)
        pair.corr = corr

        pair.corr_std, pair.coint_std = self.get_std(stock1.code, stock2.code, date2)
        """
        if target_field(stock1, stock2):
            pair.corr_std, pair.coint_std = self.get_std(stock1.code, stock2.code, date2)
        else:
            pair.corr_std, pair.coint_std = -1, -1
        """

        pair.per1 = self.pers[stock1.code] if self.pers[stock1.code] else 'N/A'
        pair.per2 = self.pers[stock2.code] if self.pers[stock2.code] else 'N/A'
        return pair

    def del_model(self, date):
        self.PickedPair.objects.raw({'date2':{'$eq':date}}).delete()

    def del_models(self):
        self.PickedPair.objects.delete()

    def set_stocks(self, stocks):
        self.stocks = stocks

    def get_std(self, code1, code2, date):
        corrs = list()
        coints = list()

        start = add_year(date, -2)

        while True:
            date1 = add_year(date, -2)
            date2 = date

            df1, df2 = get_dfs_pool(self.Candle, date1, date2, code1, code2)
            coint_calc = figure_coint_calc(df1, df2)

            """
            coint_fit  = figure_coint_fit(df1, df2)
            if -2 < coint_fit < 2:
                coint_select = coint_fit
            else:
                coint_select = coint_calc
            """

            coint_select = coint_calc
            dfs          = get_df_spread(df1, df2, coint_select)

            if dfs is None:
                break

            norm1, norm2 = get_norm(df1, df2) 
            corr = get_corr(norm1, norm2)

            coint_calc = figure_coint_calc(df1, df2)

            if valid_data(corr) and valid_data(coint_calc):
                coints.append(coint_calc)
                corrs.append(corr)

            date = date - relativedelta(months=1)
            date = date.replace(day=monthrange(date.year, date.month)[1])
            #print(date, coint_calc)
            if date <= start:
                break

        return np.std(corrs), np.std(coints)

    def get_figure_coint_calc(self, df1, df2):
        coint_calc = figure_coint_calc(df1, df2)
        dfs        = get_df_spread(df1, df2, coint_calc)

        return coint_calc, dfs

    def get_figure_place(self, dfs):
        place      = figure_place(dfs['value'])
        place_cnt  = dfs.__len__()

        return place, place_cnt

    def new_figure(self, df1, df2, dfs, coint_calc, place, place_cnt):
        fig = Figure()

        density = figure_density(dfs)

        n, ks_pvalue, adf_pvalue, coint_pvalue = figure_test(df1, df2, dfs)
        hit0_cnt, ends, rng10, rng20, rng30, rng40, rng50, rng60, rng70, rng80 = figure_pam(dfs)

        fig.coint_fit = coint_calc
        fig.coint_calc = coint_calc
        fig.coint_select = coint_calc
        fig.ks_pvalue = ks_pvalue
        fig.adf_pvalue = adf_pvalue
        fig.coint_pvalue = coint_pvalue
        fig.value = dfs['value'][-1]
        fig.density = density
        fig.place = place
        fig.place_cnt = place_cnt

        fig.hit0_cnt = hit0_cnt
        fig.cy10_cnt = ends[0][1]
        fig.cy20_cnt = ends[1][1]
        fig.cy30_cnt = ends[2][1]
        fig.cy40_cnt = ends[3][1]
        fig.cy50_cnt = ends[4][1]
        fig.cy60_cnt = ends[5][1]
        fig.cy70_cnt = ends[6][1]
        fig.cy80_cnt = ends[7][1]
        fig.cy90_cnt = ends[8][1]

        fig.cy10_20_cnt = rng10[0][1]
        fig.cy10_30_cnt = rng10[1][1]
        fig.cy10_40_cnt = rng10[2][1]
        fig.cy10_50_cnt = rng10[3][1]
        fig.cy10_60_cnt = rng10[4][1]
        fig.cy10_70_cnt = rng10[5][1]
        fig.cy10_80_cnt = rng10[6][1]
        fig.cy10_90_cnt = rng10[7][1]

        fig.cy20_30_cnt = rng20[0][1]
        fig.cy20_40_cnt = rng20[1][1]
        fig.cy20_50_cnt = rng20[2][1]
        fig.cy20_60_cnt = rng20[3][1]
        fig.cy20_70_cnt = rng20[4][1]
        fig.cy20_80_cnt = rng20[5][1]
        fig.cy20_90_cnt = rng20[6][1]

        fig.cy30_40_cnt = rng30[0][1]
        fig.cy30_50_cnt = rng30[1][1]
        fig.cy30_60_cnt = rng30[2][1]
        fig.cy30_70_cnt = rng30[3][1]
        fig.cy30_80_cnt = rng30[4][1]
        fig.cy30_90_cnt = rng30[5][1]

        fig.cy40_50_cnt = rng40[0][1]
        fig.cy40_60_cnt = rng40[1][1]
        fig.cy40_70_cnt = rng40[2][1]
        fig.cy40_80_cnt = rng40[3][1]
        fig.cy40_90_cnt = rng40[4][1]

        fig.cy50_60_cnt = rng50[0][1]
        fig.cy50_70_cnt = rng50[1][1]
        fig.cy50_80_cnt = rng50[2][1]
        fig.cy50_90_cnt = rng50[3][1]

        fig.cy60_70_cnt = rng60[0][1]
        fig.cy60_80_cnt = rng60[1][1]
        fig.cy60_90_cnt = rng60[2][1]

        fig.cy70_80_cnt = rng70[0][1]
        fig.cy70_90_cnt = rng70[1][1]

        fig.cy80_90_cnt = rng80[0][1]

        fig.spread_min  = min(dfs['value'])
        fig.spread_max  = max(dfs['value'])

        return fig

    def contains(self, ohlcvs, filter):
        for x in ohlcvs:
            if filter(x):
                return True
        return False

    def working_day(self, date):
        if date.weekday() in (5,6):    # return if saturday or sunday
            return False

        candles = self.Candle.objects.raw({}).limit(10)
        for candle in candles:
            ohlcvs = candle.ohlcvs

            if self.contains(ohlcvs, lambda x: x.date == date):
                return True
        return False

class ConcreteProductPickedPairKr(AbstractProductPickedPair):
    def __init__(self, **kwargs):
        super().__init__('kr', **kwargs)

    def make_model(self, date1, date2):
        if not self.working_day(date2):
            return 0

        self.set_stocks(get_stocks_kr())

        return super().make_model(date1, date2)

class ConcreteProductPickedPairUs(AbstractProductPickedPair):
    def __init__(self, **kwargs):
        super().__init__('us', **kwargs)

    def make_model(self, date1, date2):
        if not self.working_day(date2):
            return 0

        self.set_stocks(get_stocks_us())

        return super().make_model(date1, date2)

"""
1. 단계(매주금요일) => make_node_pair_model
    1) 2년은 488일이다. 그중에 400일 이상 tick이 있다.
    2) 같은 계열사 혹은 업종.
    3) corr  0.8 이상.

2. 단계(매일) => make_picked_pair_model
    1) 2년은 488일이다. 그중에 450일 이상 tick이 있다.
    2) place의 값이 상위 혹은 하위 10% 보다 적다.
"""

if __name__ == '__main__':
    pass
