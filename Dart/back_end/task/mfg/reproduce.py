import sys
import pandas as pd
from dateutil.relativedelta import relativedelta
from task.singleton import pool_ohlcv

sys.path.append('/home/yepark/Production/UNeed')
from data.db.models import CandleUs, CandleKr

def get_ohlcvs(code, rcept_dt):
    df = get_ohlcv_pool(code)
    date = str_to_date(rcept_dt, '%Y%m%d')

    bf30 = date + relativedelta(months = -1)
    bf7  = date + relativedelta(days   = -7)
    af7  = date + relativedelta(days   = +7)
    af30 = date + relativedelta(months = +1)

    return [df.loc[:bf30][-1:], df.loc[:bf7][-1:], df.loc[:date][-1:], df.loc[:af7] [-1:], df.loc[:af30][-1:]]

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

def get_ohlcv_pool(code):
    df = pool_ohlcv.get(code)

    if df is None:
        df = get_ohlcv_db(CandleKr, code)
    pool_ohlcv.set(code, df)
    return df

