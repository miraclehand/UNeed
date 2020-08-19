import pandas as pd
import numpy as np
from datetime import datetime
from constants import *

from basedb.models import Stock, StockKr, StockUs
from basedb.models import Candle, CandleKr, CandleUs

from task.singleton import pool_ohlcv

def get_ohlcv_db(Candle, code):
    ohlcvs = Candle.objects.get({'code':code}).ohlcvs

    df = pd.DataFrame([{'date' : ohlcv.date.date(),
                        'close': ohlcv.close,
                        'volume':ohlcv.volume,
                        'log'  : ohlcv.log} for ohlcv in ohlcvs])
    if df.empty:
        return df
    df = df.set_index('date')
    return df

def get_ohlcv_pool(Candle, code):
    df = pool_ohlcv.get(code)

    if df is None:
        df = get_ohlcv_db(Candle, code)
    pool_ohlcv.set(code, df)
    return df

def get_valid_ohlcv_pool(Candle, code, days):
    df = pool_ohlcv.get(code)

    if df is None:
        df = get_ohlcv_db(Candle, code)
    pool_ohlcv.set(code, df)
    if days > df.__len__(): # skip if not enough data
        return None
    return df

def get_intxn(date1, date2, df1, df2):
    if df1 is None or df2 is None:
        return None, None

    if isinstance(date1, datetime): date1 = date1.date()
    if isinstance(date2, datetime): date2 = date2.date()

    #faster more then merge
    dfm1 = df1[(df1.index >= date1) & (df1.index <= date2) & df1.index.isin(df2.index)]
    dfm2 = df2[(df2.index >= date1) & (df2.index <= date2) & df2.index.isin(df1.index)]

    if dfm1.__len__() <= 0:
        return None, None

    return dfm1, dfm2

def get_valid_intxn(date1, date2, df1, df2, ratio):
    dfm1, dfm2 = get_intxn(date1, date2, df1, df2)

    if dfm1 is None or dfm2 is None:
        return None, None

    days = (date2 - date1).days
    if days / dfm1.__len__() >= ratio: # skip if not enough data
        return None, None
    return dfm1, dfm2

def get_df_spread(df1, df2, coint):
    if df1 is None or df2 is None:
        return None
    if np.isnan(coint):
        return None

    dfs = pd.DataFrame()
    dfs['value'] = df1['log'] - coint * df2['log']
    mean = dfs['value'].mean()
    dfs['value'] = (dfs['value'] - mean) * 100

    return dfs

def get_dfs_db(Candle, date1, date2, code1, code2):
    df1 = get_ohlcv_db(Candle, code1)
    df2 = get_ohlcv_db(Candle, code2)
    df1, df2 = get_intxn(date1, date2, df1, df2)

    return df1, df2

def get_dfs_pool(Candle, date1, date2, code1, code2):
    df1 = get_ohlcv_pool(Candle, code1)
    df2 = get_ohlcv_pool(Candle, code2)
    df1, df2 = get_intxn(date1, date2, df1, df2)

    return df1, df2

def get_valid_dfs_pool(Candle, date1, date2, code1, code2, ratio):
    df1 = get_ohlcv_pool(Candle, code1)
    df2 = get_ohlcv_pool(Candle, code2)
    df1, df2 = get_valid_intxn(date1, date2, df1, df2, ratio)

    return df1, df2

def get_stocks_kr():
    # exclude_code 단기통안채 (항상 우상향)
    # capital, avg_v50 단위(억원),  둘다 천억원이상인 주식
    return list(StockKr.objects.raw({'capital':{'$gte':1000},
                                     'avg_v50':{'$gte':1000},
                                     'code':{'$nin':exclude_code}}
           ).order_by([('code', 1)]))

def get_stocks_us():
    # capital, avg_v50 단위(억달러), 시총 1억달러이상(1천억), 거래대금 천만달러이상
    return list(StockUs.objects.raw({'capital':{'$gte':1},
                                     'avg_v50':{'$gte':0.1},
                                     'code':{'$nin':exclude_code}}
           ).order_by([('code', 1)]))

def get_ind_idx(ind):
    for idx, p in enumerate(general_industry):
        if ind in p:
            return idx
    return -1

def same_industry(ind1, ind2):
    if not ind1 or not ind2:
        return False

    if 'N/A' != ind1 == ind2:
        return True

    idx1, idx2 = get_ind_idx(ind1), get_ind_idx(ind2)
    if -1 in (idx1, idx2):
        return False

    if idx1 == idx2:
        return True
    return False

def target_field(stock1, stock2):
    if stock1.parent and 'N/A' != stock1.parent == stock2.parent:
        return True
    elif same_industry(stock1.industry, stock2.industry):
        return True
    else:
        return False

def get_norm(df1, df2):
    if df1 is None or df2 is None:
        return None, None
    if df1.empty or df2.empty:
        return None, None

    mean1 = df1['close'].mean()
    std1  = df1['close'].std()
    norm1 =(df1['close'] - mean1) / std1

    mean2 = df2['close'].mean()
    std2  = df2['close'].std()
    norm2 =(df2['close'] - mean2) / std2

    if std1 == 0 or std2 == 0:
        return None, None

    return norm1, norm2

def get_corr(df1, df2):
    if df1 is None or df2 is None:
        return None
    if df1.empty or df2.empty:
        return None

    corr = df1.corr(df2)

    if np.isnan(corr):
        return None
    else:
        return corr

def valid_data(data):
    if data is None:
        return False

    if np.isnan(data):
        return False
    return True

