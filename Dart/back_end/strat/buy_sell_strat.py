from datetime import datetime
from dateutil.relativedelta import relativedelta
from commons.utils.datetime import str_to_datetime
from strat.util import get_d_prrt

#매도:목표수익률,로스컷,1주뒤 음수, 4주후 강제청산
def buy_sell_strat1(disc, df, profit, losscut):
    rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()

    af01 = rcept_date + relativedelta(days = +1)
    af1w = rcept_date + relativedelta(weeks  = +1)
    af4w = rcept_date + relativedelta(weeks  = +4)

    d_close  = df.loc[rcept_date:].head(1)['close'].values[0]
    d_change = df.loc[rcept_date:].head(1)['change'].values[0]

    #if d_change >= 20:
    #    return None, None

    df_h = df.loc[af01:af4w]['high']
    df_l = df.loc[af01:af4w]['low']

    p_close = d_close + (d_close * profit / 100)   #목표가격
    l_close = d_close - (d_close * losscut/ 100)   #로스컷가격

    df_profit = df_h[df_h >= p_close].head(1)
    df_loss   = df_l[df_l <= l_close].head(1)

    profit_date = datetime.max.date() if df_profit.empty else df_profit.index[0]
    losscut_date= datetime.max.date() if df_loss.empty   else df_loss.index[0] 

    af1w_close, af1w_rt = get_d_prrt(df.loc[:af1w], d_close)
    af4w_close, af4w_rt = get_d_prrt(df.loc[:af4w], d_close)

    if af1w_rt >= 0:
        af1w = datetime.max.date()
    sell_dates = [profit_date, losscut_date, af1w, af4w]
    sell_date = min(sell_dates)

    if sell_date == profit_date:
        return profit_date, profit
    if sell_date == losscut_date:
        return losscut_date, -losscut

    sell_close, sell_rt = get_d_prrt(df.loc[:sell_date], d_close)

    if not sell_close or not sell_rt:
        return None, None

    return sell_date, sell_rt

#매도:목표수익률,로스컷,2주뒤 음수, 4주후 강제청산
def buy_sell_strat2(disc, df, profit, losscut):
    rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()

    af01 = rcept_date + relativedelta(days = +1)
    af2w = rcept_date + relativedelta(weeks  = +2)
    af4w = rcept_date + relativedelta(weeks  = +4)

    d_close  = df.loc[rcept_date:].head(1)['close'].values[0]
    d_change = df.loc[rcept_date:].head(1)['change'].values[0]

    #if d_change >= 20:
    #    return None, None

    df_h = df.loc[af01:af4w]['high']
    df_l = df.loc[af01:af4w]['low']

    p_close = d_close + (d_close * profit / 100)   #목표가격
    l_close = d_close - (d_close * losscut/ 100)   #로스컷가격

    df_profit = df_h[df_h >= p_close].head(1)
    df_loss   = df_l[df_l <= l_close].head(1)

    profit_date = datetime.max.date() if df_profit.empty else df_profit.index[0]
    losscut_date= datetime.max.date() if df_loss.empty   else df_loss.index[0] 

    af2w_close, af2w_rt = get_d_prrt(df.loc[:af2w], d_close)
    af4w_close, af4w_rt = get_d_prrt(df.loc[:af4w], d_close)

    if af2w_rt >= 0:
        af2w = datetime.max.date()
    sell_dates = [profit_date, losscut_date, af2w, af4w]
    sell_date = min(sell_dates)

    if sell_date == profit_date:
        return profit_date, profit
    if sell_date == losscut_date:
        return losscut_date, -losscut

    sell_close, sell_rt = get_d_prrt(df.loc[:sell_date], d_close)

    if not sell_close or not sell_rt:
        return None, None

    return sell_date, sell_rt

#매도:1주뒤 음수, 4주후 강제청산
def buy_sell_strat3(disc, df, profit, losscut):
    rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()

    af1w = rcept_date + relativedelta(weeks  = +1)
    af4w = rcept_date + relativedelta(weeks  = +4)

    d_close  = df.loc[rcept_date:].head(1)['close'].values[0]

    af1w_close, af1w_rt = get_d_prrt(df.loc[:af1w], d_close)
    af4w_close, af4w_rt = get_d_prrt(df.loc[:af4w], d_close)

    if af1w_rt >= 0:
        af1w = datetime.max.date()
    sell_dates = [af1w, af4w]
    sell_date = min(sell_dates)

    sell_close, sell_rt = get_d_prrt(df.loc[:sell_date], d_close)

    if not sell_close or not sell_rt:
        return None, None

    return sell_date, sell_rt

#매도:2주뒤 음수, 4주후 강제청산
def buy_sell_strat4(disc, df, profit, losscut):
    rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()

    af2w = rcept_date + relativedelta(weeks  = +2)
    af4w = rcept_date + relativedelta(weeks  = +4)

    d_close  = df.loc[rcept_date:].head(1)['close'].values[0]

    af2w_close, af2w_rt = get_d_prrt(df.loc[:af2w], d_close)
    af4w_close, af4w_rt = get_d_prrt(df.loc[:af4w], d_close)

    if af2w_rt >= 0:
        af2w = datetime.max.date()
    sell_dates = [af2w, af4w]
    sell_date = min(sell_dates)

    sell_close, sell_rt = get_d_prrt(df.loc[:sell_date], d_close)

    if not sell_close or not sell_rt:
        return None, None

    return sell_date, sell_rt

#매도:로스컷,2주뒤 음수, 4주후 강제청산
def buy_sell_strat5(disc, df, profit, losscut):
    rcept_date = str_to_datetime(disc.rcept_dt, '%Y%m%d').date()

    af01 = rcept_date + relativedelta(days = +1)
    af1w = rcept_date + relativedelta(weeks  = +1)
    af2w = rcept_date + relativedelta(weeks  = +2)
    af4w = rcept_date + relativedelta(weeks  = +4)

    d_close  = df.loc[rcept_date:].head(1)['close'].values[0]
    d_change = df.loc[rcept_date:].head(1)['change'].values[0]

    #if d_change >= 20:
    #    return None, None

    #df_l = df.loc[af01:af4w]['low']
    #로스컷은 1주일 뒤부터 체크 함
    df_l = df.loc[af1w:af4w]['low']

    l_close = d_close - (d_close * losscut/ 100)   #로스컷가격

    df_loss   = df_l[df_l <= l_close].head(1)

    losscut_date= datetime.max.date() if df_loss.empty   else df_loss.index[0] 

    af1w_close, af1w_rt = get_d_prrt(df.loc[:af1w], d_close)
    af2w_close, af2w_rt = get_d_prrt(df.loc[:af2w], d_close)
    af4w_close, af4w_rt = get_d_prrt(df.loc[:af4w], d_close)

    if af2w_rt >= 0:
        af2w = datetime.max.date()
    #1주뒤에 음수면 로스컷 체크함
    if af1w_rt < 0:
        sell_dates = [losscut_date, af2w, af4w]
    else:
        sell_dates = [af2w, af4w]
    #sell_dates = [losscut_date, af2w, af4w]
    sell_date = min(sell_dates)

    if sell_date == losscut_date:
        return losscut_date, -losscut

    sell_close, sell_rt = get_d_prrt(df.loc[:sell_date], d_close)

    if not sell_close or not sell_rt:
        return None, None

    return sell_date, sell_rt

