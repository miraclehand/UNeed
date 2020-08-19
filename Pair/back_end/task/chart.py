import os, glob
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import abc
from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from app import app
from utils.datetime import add_year

from basedb.models import Stock, StockKr, StockUs
from basedb.models import Candle, CandleKr, CandleUs

from task.mfg.reproduce import get_dfs_db
from task.mfg.reproduce import get_corr, get_norm, get_df_spread
from task.mfg.figure import figure_coint_calc, figure_coint_fit, figure_test
from task.mfg.figure import figure_place, get_bins, get_idx_from_bins
from task.mfg.figure import figure_density

#pc 에서사용할때,
#import matplotlib
#try:
#    matplotlib.use('pdf')
#except:
#    pass

pd.plotting.register_matplotlib_converters()

# ref statsmodels.tsa.stattools.coint

# Abstract Factory Pattern
#AbstractFactory
class AbstractChartFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_norm_chart(self):
        pass

    @abc.abstractmethod
    def create_log_chart(self):
        pass

    @abc.abstractmethod
    def create_hist_chart(self):
        pass

    @abc.abstractmethod
    def create_vol_chart(self):
        pass

    @classmethod
    def get_factory(self, cntry):
        if cntry == 'kr':
            return ConcreteChartKrFactory()
        if cntry == 'us':
            return ConcreteChartUsFactory()
        return None

#ConcreteFactory1
class ConcreteChartKrFactory(AbstractChartFactory):
    def create_norm_chart(self):
        return ConcreteProductNormChartKr()

    def create_log_chart(self):
        return ConcreteProductLogChartKr()

    def create_hist_chart(self):
        return ConcreteProductHistChartKr()

    def create_vol_chart(self):
        return ConcreteProductVolChartKr()

#ConcreteFactory2
class ConcreteChartUsFactory(AbstractChartFactory):
    def create_norm_chart(self):
        return ConcreteProductNormChartUs()

    def create_log_chart(self):
        return ConcreteProductLogChartUs()

    def create_hist_chart(self):
        return ConcreteProductHistChartUs()

    def create_vol_chart(self):
        return ConcreteProductVolChartUs()

class AbstractProductChart(metaclass=abc.ABCMeta):
    Stock  = None
    Candle = None

    def __init__(self, Stock, Candle, **kwargs):
        super().__init__(**kwargs)
        self.Stock  = Stock
        self.Candle = Candle

    def get_dfs(self, date1, date2, code1, code2):
        if isinstance(date1, str): date1 = datetime.strptime(date1, '%Y-%m-%d')
        if isinstance(date2, str): date2 = datetime.strptime(date2, '%Y-%m-%d')
        #from pymodm import connect
        #connect('mongodb://localhost:27017/basedb')
        try:    
            code1 = self.Stock.objects.get({'$or':[{'code':code1},
                                                   {'name':code1}]}).code
            code2 = self.Stock.objects.get({'$or':[{'code':code2},
                                                   {'name':code2}]}).code
        except:
            return None, None

        df1, df2 = get_dfs_db(self.Candle, date1, date2, code1, code2)
        return df1, df2

    def save_file(self, fig, name):
        absolute_path = app.static_folder + '/image'
        # Remove old plot files
        for filename in glob.glob(os.path.join(absolute_path, '*' + name)):
            os.remove(filename)
        filename = str(time.time()) + name
        plotfile = os.path.join(absolute_path, filename)
        fig.savefig(plotfile)

        return 'dist/image/' + filename

    def draw_line_chart(self, title, name, xaxis, *yaxises):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        for yaxis in yaxises:
            ax.plot(xaxis, yaxis)

        if yaxises.__len__() > 1:
            plt.legend(['corr','coint','ks_pvalue','adf_pvalue','coint_pvalue'])
        if yaxises.__len__() == 3:
            plt.legend(['log','sine','cos'])

        ax.set_xlabel('date')
        ax.set_ylabel('value')
        ax.set_title(title)
        ax.grid(True)

        """
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m'))

        ax.xaxis.set_minor_locator(mdates.YearLocator())
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))

        ax.tick_params(axis='both', which='major', labelsize=7)
        """

        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%Y'))

        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))

        ax.tick_params(axis='both', which='minor', labelsize=7)

        fig.tight_layout()

        filename = self.save_file(fig, name)
        plt.close(fig)

        return filename

#AbstractProductA
class AbstractProductNormChart(AbstractProductChart):
    def draw_chart(self, date1, date2, code1, code2):
        df1, df2 = self.get_dfs(date1, date2, code1, code2)

        norm1, norm2 = get_norm(df1, df2)
        corr = get_corr(norm1, norm2)

        dfs = norm1 - norm2

        title = 'Normalization Spread Chart:Correlation=%0.3f' % corr
        name = '_norm_done.png'

        return self.draw_line_chart(title, name, dfs.index.values, dfs.values)

#ConcreteProductA
class ConcreteProductNormChartKr(AbstractProductNormChart):
    def __init__(self, **kwargs):
        super().__init__(StockKr, CandleKr, **kwargs)

    def draw_chart(self, date1, date2, code1, code2):
        return super().draw_chart(date1, date2, code1, code2)

#ConcreteProductB
class ConcreteProductNormChartUs(AbstractProductNormChart):
    def __init__(self, **kwargs):
        super().__init__(StockUs, CandleUs, **kwargs)

    def setup(self, date1, date2, code1, code2):
        super().setup(date1, date2, code1, code2)

    def draw_chart(self, date1, date2, code1, code2):
        return super().draw_chart(date1, date2, code1, code2)

#AbstractProductA
class AbstractProductLogChart(AbstractProductChart):
    def draw_chart(self, date1, date2, code1, code2):
        df1, df2 = self.get_dfs(date1, date2, code1, code2)
        coint_calc = figure_coint_calc(df1, df2)
        coint_fit  = figure_coint_fit(df1, df2)
        if -2 < coint_fit < 2:
            coint_select = coint_fit
        else:
            coint_select = coint_calc
        coint_select = coint_calc
        dfs = get_df_spread(df1, df2, coint_select)

        title = 'Log Spread Chart:Cointegration=%0.3f, %0.3f, %0.3f' % (coint_fit, coint_calc, coint_select)
        name = '_log.png'

        """
        avg = (abs(min(dfs['value'])) + abs(max(dfs['value'])) ) / 2
        sample = dfs.__len__()
        pendulum = 4   # 진자
        x = np.arange(sample)
        y1 = np.sin(2 * np.pi * pendulum * x / sample) * avg
        y2 = np.cos(2 * np.pi * pendulum * x / sample) * avg
        sim1 = cosine_similarity(dfs['value'], y1)
        sim2 = cosine_similarity(dfs['value'], y2)
        title = 'Log Spread Chart:Cointegration=%0.3f, %0.3f, %0.3f, %0.3f, %0.3f' % (coint_fit, coint_calc, coint_select, sim1, sim2)
        url = draw_line_chart(title, '_log_done.png', dfs.index.values,dfs['value'], y1, y2)
        """
        return self.draw_line_chart(title, name, dfs.index.values, dfs['value'])

#ConcreteProductA
class ConcreteProductLogChartKr(AbstractProductLogChart):
    def __init__(self, **kwargs):
        super().__init__(StockKr, CandleKr, **kwargs)

    def draw_chart(self, date1, date2, code1, code2):
        return super().draw_chart(date1, date2, code1, code2)

#ConcreteProductB
class ConcreteProductLogChartUs(AbstractProductLogChart):
    def __init__(self, **kwargs):
        super().__init__(StockUs, CandleUs, **kwargs)

    def draw_chart(self, date1, date2, code1, code2):
        return super().draw_chart(date1, date2, code1, code2)

#AbstractProductA
class AbstractProductHistChart(AbstractProductChart):
    def draw_chart(self, date1, date2, code1, code2):
        df1, df2 = self.get_dfs(date1, date2, code1, code2)
        coint_calc = figure_coint_calc(df1, df2)
        """
        coint_fit  = figure_coint_fit(df1, df2)
        if -2 < coint_fit < 2:
            coint_select = coint_fit
        else:
            coint_select = coint_calc
        """
        coint_select = coint_calc
        dfs = get_df_spread(df1, df2, coint_select)

        #density = figure_density(dfs)

        #ks  test: 정규성검증, 0.05보다 크면 정규적이다.
        #adf test: 정상성검증, 0.05보다 작으면 정상적이다.
        #coint test: 공적분검증, 0.05보다 작으면 공적분이다.
        n, ks_pvalue, adf_pvalue, coint_pvalue = figure_test(df1, df2, dfs)
        X = dfs['value']

        bins = get_bins(X)

        place = figure_place(X)
        cnt_of_place  = X.__len__()

        ratio_of_place  = place / cnt_of_place * 100
        title = 'Log Histogram:[pvalue] ks=%0.4f, adf=%0.4f, coint=%0.4f' % (ks_pvalue, adf_pvalue, coint_pvalue)

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        nn, bin_edges, patches = ax.hist(X, bins=bins, rwidth=0.7, alpha=0.75)
        fig.tight_layout()

        text1 = ax.yaxis.get_major_ticks()[0].label1.get_text()  
        text2 = ax.yaxis.get_major_ticks()[1].label1.get_text()  
        step = float(text2) -  float(text1)

        idx = get_idx_from_bins(X[-1], bin_edges)
        rect = patches[idx]
        xy = (rect.get_x() + rect.get_width() / 2, rect.get_height() + 1)
        xytext = (0, (min(nn)+ max(nn))//4 + step*10)

        xx = np.arange(X.min(), X.max()+0.5, 0.5)
        ax.plot(xx, 350*n.pdf(xx))
        ax.set_title(title)
        ax.grid(True)

        place_repr = '%d/%d(%.2f%%)' % (place, cnt_of_place, ratio_of_place)
        ax.annotate('x axis:%0.3f, place:%s' % (dfs[-1:].value,place_repr),xy=xy,textcoords='offset points', xytext=xytext,arrowprops={'color':'green','shrink':0.05}, horizontalalignment='center')

        fig.tight_layout()

        filename = self.save_file(fig, '_hist.png')
        plt.close(fig)
        return filename

#ConcreteProductA
class ConcreteProductHistChartKr(AbstractProductHistChart):
    def __init__(self, **kwargs):
        super().__init__(StockKr, CandleKr, **kwargs)

    def draw_chart(self, date1, date2, code1, code2):
        return super().draw_chart(date1, date2, code1, code2)

#ConcreteProductB
class ConcreteProductHistChartUs(AbstractProductHistChart):
    def __init__(self, **kwargs):
        super().__init__(StockUs, CandleUs, **kwargs)

    def draw_chart(self, date1, date2, code1, code2):
        return super().draw_chart(date1, date2, code1, code2)

#AbstractProductA
class AbstractProductVolChart(AbstractProductChart):
    def draw_chart(self, date1, date2, code1, code2):
        dates = list()
        corrs = list()
        coints = list()
        densities = list()
        ks_pvalues = list()
        adf_pvalues = list()
        coint_pvalues = list()

        if isinstance(date1, str): date1 = datetime.strptime(date1, '%Y-%m-%d')
        if isinstance(date2, str): date2 = datetime.strptime(date2, '%Y-%m-%d')
        start = date1
        end   = date2

        date = end 
        while True:
            date1 = add_year(date, -2)
            date2 = date

            df1, df2 = self.get_dfs(date1, date2, code1, code2)
            coint_calc = figure_coint_calc(df1, df2)
            """
            coint_fit  = figure_coint_fit(df1, df2)
            if -2 < coint_fit < 2:
                coint_select = coint_fit
            else:
                coint_select = coint_calc
            """
            coint_select = coint_calc
            dfs        = get_df_spread(df1, df2, coint_select)
            density    = figure_density(dfs)

            if dfs is None:
                break

            #ks  test: 정규성검증, 0.05보다 크면 정규적이다.
            #adf test: 정상성검증, 0.05보다 작으면 정상적이다.
            #coint test: 공적분검증, 0.05보다 작으면 공적분이다.
            n, ks_pvalue, adf_pvalue, coint_pvalue = figure_test(df1, df2, dfs)

            norm1, norm2 = get_norm(df1, df2)
            corr = get_corr(norm1, norm2)

            dates.append(date2)
            corrs.append(corr)
            coints.append(coint_calc)
            densities.append(density)
            ks_pvalues.append(ks_pvalue)
            adf_pvalues.append(adf_pvalue)
            coint_pvalues.append(coint_pvalue)

            date = date - relativedelta(months=1)
            date = date.replace(day=monthrange(date.year, date.month)[1])
            #print(date, coint_calc)
            if date <= start:
                break

        title = 'Volatile Graph: std of cointegration=%0.3f' % (np.std(coints))
        name =  '_volatile.png'
        return self.draw_line_chart(title, name, dates, corrs, coints, ks_pvalues, adf_pvalues, coint_pvalues)

#ConcreteProductA
class ConcreteProductVolChartKr(AbstractProductVolChart):
    def __init__(self, **kwargs):
        super().__init__(StockKr, CandleKr, **kwargs)

    def draw_chart(self, date1, date2, code1, code2):
        return super().draw_chart(date1, date2, code1, code2)

#ConcreteProductB
class ConcreteProductVolChartUs(AbstractProductVolChart):
    def __init__(self, **kwargs):
        super().__init__(StockUs, CandleUs, **kwargs)

    def draw_chart(self, date1, date2, code1, code2):
        return super().draw_chart(date1, date2, code1, code2)

#sudo pip3 install Cython
#sudo pip3 install scikit-learn
#from sklearn.metrics.pairwise import cosine_similarity
#cosine_similarity(dfs1,dfs2)
def cosine_similarity2(x):
    Fs = x.__len__() - 1
    f = 2
    sample = x.__len__() - 1
    x = np.arange(x)
    y = np.sin(2 * np.pi * f * x / Fs)

    return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))

def cosine_similarity(x, y):
    return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))

def draw_log_spread_chart(code1, code2, date1, date2):
    factory = ConcreteChartKrFactory()
    log_chart = factory.create_log_chart()
    url = log_chart.draw_chart(date1, date2, code1, code2)

    return url

def draw_log_hist_chart(code1, code2, date1, date2):
    factory = ConcreteChartKrFactory()
    hist_chart = factory.create_hist_chart()
    url = hist_chart.draw_chart(date1, date2, code1, code2)

    return url

def draw_vol_chart(code1, code2, date):
    factory = ConcreteChartKrFactory()
    vol_chart = factory.create_vol_chart()

    start = date - relativedelta(months=25)
    end   = date
    url = vol_chart.draw_chart(start, end, code1, code2)

    return url
