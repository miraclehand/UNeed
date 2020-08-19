import inspect
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from db.models import CandleKr, PickedPairKr
from task.mfg.reproduce import get_dfs_pool
from task.mfg.reproduce import target_field
from constants import *
from util import write_simul, write_new_simul

class Stock:
    def __init__(self, stock, close):
        self.code = stock.code
        self.name = stock.name
        self.close = close

    code = ''
    name = ''
    close = 0

class Basket:
    def __init__(self, pair):
        if pair.fig_str.value > 0:
            #A고평가, B저평가
            self.pos1 = D_POS_SHORT
            self.pos2 = D_POS_LONG
        else:
            #A저평가, B고평가
            self.pos1 = D_POS_LONG
            self.pos2 = D_POS_SHORT

        self.date = pair.date2
        self.code1 = pair.stock1.code
        self.name1 = pair.stock1.name
        self.buy_close1 = pair.close1
        self.sell_close1 = None

        self.code2 = pair.stock2.code
        self.name2 = pair.stock2.name
        self.buy_close2 = pair.close2
        self.sell_close2 = None

        self.coint = float('%.3f' % pair.fig_str.coint_calc)
        self.coint_std = pair.coint_std
        self.density = pair.fig_str.density
        self.ks_pvalue = pair.fig_str.ks_pvalue
        self.adf_pvalue = pair.fig_str.adf_pvalue
        self.coint_pvalue = pair.fig_str.coint_pvalue
        self.value = pair.fig_str.value
        self.spread_min = pair.fig_str.spread_min
        self.spread_max = pair.fig_str.spread_max
        self.corr_std = pair.corr_std
        self.cy10_cnt = pair.fig_str.cy10_cnt
        self.cy15_cnt = pair.fig_str.cy15_cnt

    date = ''
    code1 = ''
    name1 = ''
    pos1 = ''
    close1 = 0

    code2 = ''
    name2 = ''
    pos2 = ''
    close2 = 0

    coint = 0
    coint_std = 0
    corr_std = 0
    density = 0
    ks_pvalue = 0
    adf_pvalue = 0
    coint_pvalue = 0
    value = 0
    spread_min = 0
    spread_max = 0
    cy10_cnt = 0
    cy15_cnt = 0

def exists(code1, code2, baskets):
    for basket in baskets:
        if code1 == basket.code1 and code2 == basket.code2:
            return True
        if code1 == basket.code2 and code2 == basket.code1:
            return True

        if code1 in (basket.code1, basket.code2):
            return True
        if code2 in (basket.code1, basket.code2):
            return True
    return False

def calc_prrt(basket, date):
    df1,df2 = get_dfs_pool(CandleKr, date, date, basket.code1, basket.code2)
    basket.sell_close1 = df1['close'][0]
    basket.sell_close2 = df2['close'][0]

    if basket.sell_close1 == 0 or basket.sell_close2 == 0:
        return 0

    prrt1 = (basket.sell_close1 - basket.buy_close1) / basket.buy_close1 * 100
    prrt2 = (basket.sell_close2 - basket.buy_close2) / basket.buy_close2 * 100 * basket.coint

    if basket.pos1 == D_POS_LONG:
        prrt = prrt1 - prrt2
    else:
        prrt = prrt2 - prrt1

    return prrt

#파는시점은 정규성이 떨어졌을 때?
def popup_basket1(date, baskets):
    to_remove = list()
    up   =  10  # 5%
    #up   =  15  # 5%
    down = -20  # 5%
    up   =  30  # 5%
    #down = -10  # 5%
    o_prrt = 0

    """
    up = 10
    down = -20
    days = 30
    """

    up = 15
    down = -10
    days = 30

    for basket in baskets:
        #up = abs(basket.value)
        #down = -abs(basket.value)
        prrt = calc_prrt(basket, date)

        interval = date.date() - basket.date.date()
        #if prrt > up or prrt < down or interval.days > 60:
        if prrt > up or prrt < down or interval.days > days:
            to_remove.append(basket)
            repr0 ='[%s] SELL %s' % (date.date(), basket.date.date())
            """
            repr1 ='%s(%s1) %d=>%d' % (basket.name1, basket.pos1, basket.buy_close1, basket.sell_close1)
            repr2 ='%s(%s%.3f) %d=>%d'%(basket.name2,basket.pos2,basket.coint,basket.buy_close2, basket.sell_close2)
            """
            repr1 ='%s(%s1)' % (basket.name1, basket.pos1)
            repr2 ='%s(%s%.3f)'%(basket.name2,basket.pos2,basket.coint)
            repr3 = '%3.f%%' % (prrt)

            #print(basket.coint, basket.coint_std, basket.corr_std, basket.density, basket.ks_pvalue, basket.adf_pvalue, basket.coint_pvalue, basket.value, basket.spread_min, basket.spread_max, basket.cy10_cnt, basket.cy15_cnt)
            repr4 = '%.3f;%.3f;%.3f;%.3f;%.3f;%.3f;%.3f;%.3f;%.3f;%d;%d;' % (basket.coint, basket.coint_std, basket.corr_std, basket.ks_pvalue, basket.adf_pvalue, basket.coint_pvalue, basket.value, basket.spread_min, basket.spread_max, basket.cy10_cnt, basket.cy15_cnt)

            write_simul('%s %s - %s ; %s ; %s' % (repr0, repr1, repr2, repr3, repr4))
            o_prrt += prrt


    for b in to_remove:
        baskets.remove(b)
    return o_prrt

"""
* 페어 잡는 전략
    1. density 0.5 이상 삭제
    2. 같은 계열사 같은 업종만
    3. 너무 많은 비율 차이가 나면 안됨.
    
* 수익률 극대화 전략
    1. 사는타이밍
        a. 괴리가 많이 벌어졌을때,
        b. 괴리가 0이 되었을때,
        c. 괴리가 절대값 이상 벌어졌을 때
    2. 파는타이밍
        a. 괴리가 어느정도 좁혀졌을 때
        b. 괴리가 0이 되었을때
        c. 괴리가 일정수준 줄어들었을 때
        d. 일정시간이 지났을 경우
"""

def check_base_factor(pair):
    if pair.corr <= 0:
        return False

    if pair.fig_str.density >= 0.5:
        return False

    if 0.2 < pair.fig_str.place / pair.fig_str.place_cnt < 0.8:
        return False

    # 너무 많은 비율 차이가 있으면 매매하기 적합하지 않음
    if 0.5 <= pair.fig_str.coint_calc <= 1.5:
        pass
    else:
        return False

    if pair.stock1.industry == '제약' or pair.stock2.industry == '제약':  #bio
        return False

    if pair.stock1.code[5] != '0' or pair.stock2.code[5] != '0':  #우선주
        return False

    if pair.stock1.avg_v50 < 2000 or pair.stock2.avg_v50 < 2000:
        return False

    if pair.close1 < 2000 or pair.close2 < 2000:
        return False

    return True

#82%
def putin_basket_strong_constraint(pair):
    if exists(pair.stock1.code, pair.stock2.code, baskets):
        return None

    if check_base_factor(pair) == False:
        return None

    #if pair.ks_pvalue < 0.05:       # 정규성
    if pair.fig_str.ks_pvalue < 0.5:       # 정규성
        return None
    if pair.fig_str.adf_pvalue >= 0.05:     # 정상성
        return None
    if pair.fig_str.coint_pvalue >= 0.05:   # 공적분
        return None

    if 0.05 < pair.fig_str.place / pair.fig_str.place_cnt < 0.95:
        return None
    if 0.3 < pair.fig_rev.place / pair.fig_rev.place_cnt < 0.7:
        return None

    if pair.corr_std >= 0.2:
        return None
    if pair.coint_std >= 0.2:
        return None

    # 너무 비대칭인 페어는, 제대로 동작 안할 확률이 높다.
    """
    if pair.adf_pvalue_r >= 0.05 * 2:
        continue
    if pair.coint_pvalue_r >= 0.05 * 2:
        continue
    if pair.ks_pvalue_r < 0.05 * 2:
        continue
    """

    if abs(pair.fig_str.value) < 15:
        # 충분히 벌어지지 않았다.
        return None

    if pair.fig_str.cy10_cnt < 10:
        return None

    basket = Basket(pair)

    repr0 ='[%s] BUY' % (basket.date.date())
    repr1 ='%s(%s1) %d' % (basket.name1, basket.pos1, basket.buy_close1)
    repr2 ='%s(%s%.3f) %d'%(basket.name2,basket.pos2,basket.coint,basket.buy_close2)
    #inspect.stack()[0][3]
    write_simul('%s %s - %s' % (repr0, repr1, repr2))

    return basket

def putin_basket_naive(pair):
    if exists(pair.stock1.code, pair.stock2.code, baskets):
        return None

    if check_base_factor(pair) == False:
        return None

    #if pair.ks_pvalue < 0.05:       # 정규성
    if pair.ks_pvalue < 0.3:       # 정규성
        return None
    if pair.adf_pvalue >= 0.05:     # 정상성
        return None
    if pair.coint_pvalue >= 0.05:   # 공적분
        return None

    if 0.1 < pair.fig_str.place / pair.fig_str.place_cnt < 0.9:
        return None
    """
    if 0.3 < pair.fig_rev.place / pair.fig_rev.place_cnt < 0.7:
        return None
    """

    if pair.corr_std >= 0.4:
        return None
    if pair.coint_std >= 0.4:
        return None

    # 너무 비대칭인 페어는, 제대로 동작 안할 확률이 높다.
    """
    if pair.adf_pvalue_r >= 0.05 * 2:
        continue
    if pair.coint_pvalue_r >= 0.05 * 2:
        continue
    if pair.ks_pvalue_r < 0.05 * 2:
        continue
    """

    if abs(pair.fig_str.value) < 15:
        # 충분히 벌어지지 않았다.
        return None

    if pair.fig_str.cy10_cnt < 6:
        return None

    basket = Basket(pair)
    repr0 ='[%s] BUY' % (basket.date.date())
    repr1 ='%s(%s1) %d' % (basket.name1, basket.pos1, basket.buy_close1)
    repr2 ='%s(%s%.3f) %d'%(basket.name2,basket.pos2,basket.coint,basket.buy_close2)
    #inspect.stack()[0][3]
    write_simul('%s %s - %s' % (repr0, repr1, repr2))

    return basket

def strat1(date1, date2, baskets):
    prrt = 0
    saved_date = None

    if date1 == date2:
        pairs = PickedPairKr.objects.raw({'date2':{'$eq':date2}})
    else:
        pairs = PickedPairKr.objects.raw({'date2':{'$gte':date1,'$lte':date2}}
                ).order_by([('date2', 1)])

    for pair in pairs:
        if saved_date != pair.date2.date():
            saved_date = pair.date2.date()
            prrt += popup_basket1(pair.date2, baskets)
            print(' ', saved_date)
            
        #basket = putin_basket_naive(pair)
        #basket = putin_basket_strong_constraint(pair)
        #basket = putin_gg(pair)  #20191105, 66%, 15번 매매
        #basket = putin_gg1(pair) #20191105, 62%, 19번 매매
        basket = putin_gg2(pair) #20191105, 74%, 149번 매매
        #basket = putin_gg3(pair)  #20191105, -141%, 87번 매매
        #basket = putin_category(pair) 같은 category면 수치를 좀더 느슨하게
        #basket = putin_gg5(pair)
        if basket:
            baskets.append(basket)  # FIXME too slow
    return prrt

def putin_gg3(pair):
    if exists(pair.stock1.code, pair.stock2.code, baskets):
        return None

    if check_base_factor(pair) == False:
        return None

    if pair.fig_str.ks_pvalue < 0.05:       # 정규성
        return None
    if pair.fig_str.adf_pvalue >= 0.05:     # 정상성
        return None
    if pair.fig_str.coint_pvalue >= 0.1:   # 공적분
        return None

    if not target_field(pair.stock1, pair.stock2):
        return None

    if 0.05 < pair.fig_str.place / pair.fig_str.place_cnt < 0.95:
    #if 0.1 < pair.fig_str.place / pair.fig_str.place_cnt < 0.9:
        return None

    # 너무 많은 비율 차이가 있으면 매매하기 적합하지 않음
    """
    if 0.5 <= pair.fig_str.coint_calc <= 1.5:
        pass
    else:
        return None
    """

    if pair.coint_std >= 0.5:
        return None

    """
    if pair.coint_std >= 0.4:
        return None

    if pair.fig_str.cy15_cnt < 6:
        return None
    if pair.corr_std >= 0.2:
        return None
    """

    """
    if abs(abs(pair.fig_str.spread_max) - abs(pair.fig_str.spread_min)) > 5:
        return None
    if abs(abs(pair.fig_str.spread_max) - abs(pair.fig_str.value)) > 5:
        return None
    if abs(abs(pair.fig_str.spread_min) - abs(pair.fig_str.value)) > 5:
        return None

    """

    # 최근5일동안 등락이 10%이상이었다면, 뭔가 비정상
    e_date = pair.date2
    s_date = e_date - relativedelta(days=10)
    df1,df2 = get_dfs_pool(CandleKr, s_date, e_date, pair.stock1.code, pair.stock2.code)
    df1 = df1[-5:]
    df2 = df2[-5:]

    s = df1['close'].pct_change().dropna()
    if True in (abs(s.values) > 0.1):
        return None

    s = df2['close'].pct_change().dropna()
    if True in (abs(s.values) > 0.1):
        return None

    # 너무 비대칭인 페어는, 제대로 동작 안할 확률이 높다.
    """
    if 0.3 < pair.fig_rev.place / pair.fig_rev.place_cnt < 0.7:
        return None
    if pair.fig_rev.ks_pvalue < 0.1:       # 정규성
        return None
    if pair.fig_rev.adf_pvalue >= 0.05 * 2:
        return None
    if pair.fig_rev.coint_pvalue >= 0.05 * 2:
        return None
    if pair.fig_rev.ks_pvalue < 0.05 * 2:
        return None
    """

    """
    if abs(pair.fig_str.value) >= 30:
        # 너무 벌어졌다.
        return None
    """
        
    """
    if abs(pair.fig_str.value) < 10:
        # 충분히 벌어지지 않았다.
        return None
    """

    basket = Basket(pair)

    repr0 ='[%s] BUY' % (basket.date.date())
    repr1 ='%s(%s1) %d' % (basket.name1, basket.pos1, basket.buy_close1)
    repr2 ='%s(%s%.3f) %d'%(basket.name2,basket.pos2,basket.coint,basket.buy_close2)
    #inspect.stack()[0][3]
    write_simul('%s %s - %s' % (repr0, repr1, repr2))

    return basket


def putin_gg2(pair):
    if exists(pair.stock1.code, pair.stock2.code, baskets):
        return None

    if check_base_factor(pair) == False:
        return None

    #if pair.fig_str.ks_pvalue < 0.05:       # 정규성
    if pair.fig_str.ks_pvalue < 0.4:       # 정규성
        return None
    if pair.fig_str.adf_pvalue >= 0.05:     # 정상성
        return None
    if pair.fig_str.coint_pvalue >= 0.05:   # 공적분
        return None

    """
    if not target_field(pair.stock1, pair.stock2):
        return None
    """

    """
    if pair.stock1.avg_v50 < 3000 or pair.stock2.avg_v50 < 3000:
        return None
    """

    #if 0.05 < pair.fig_str.place / pair.fig_str.place_cnt < 0.95:
    if 0.1 < pair.fig_str.place / pair.fig_str.place_cnt < 0.9:
        return None

    # 너무 많은 비율 차이가 있으면 매매하기 적합하지 않음
    if 0.6 <= pair.fig_str.coint_calc <= 1.4:
        pass
    else:
        return None

    """
    if pair.coint_std >= 0.4:
        return None


    if pair.fig_str.cy15_cnt < 6:
        return None
    """

    """
    if pair.corr_std >= 0.2:
        return None
    if pair.coint_std >= 0.2:
        return None

    """

    #print(pair.fig_str.spread_min, pair.fig_str.spread_max, pair.fig_str.value)
    
    if pair.coint_std >= 0.5:
        return None

    if abs(abs(pair.fig_str.spread_max) - abs(pair.fig_str.spread_min)) > 5:
        return None
    if abs(abs(pair.fig_str.spread_max) - abs(pair.fig_str.value)) > 5:
        return None
    if abs(abs(pair.fig_str.spread_min) - abs(pair.fig_str.value)) > 5:
        return None

    # 최근5일동안 등락이 10%이상이었다면, 뭔가 비정상
    e_date = pair.date2
    s_date = e_date - relativedelta(days=10)
    df1,df2 = get_dfs_pool(CandleKr, s_date, e_date, pair.stock1.code, pair.stock2.code)
    df1 = df1[-5:]
    df2 = df2[-5:]

    s = df1['close'].pct_change().dropna()
    if True in (abs(s.values) > 0.1):
        return None

    s = df2['close'].pct_change().dropna()
    if True in (abs(s.values) > 0.1):
        return None

    # 너무 비대칭인 페어는, 제대로 동작 안할 확률이 높다.
    """
    if 0.3 < pair.fig_rev.place / pair.fig_rev.place_cnt < 0.7:
        return None
    if pair.fig_rev.ks_pvalue < 0.1:       # 정규성
        return None
    if pair.fig_rev.adf_pvalue >= 0.05 * 2:
        return None
    if pair.fig_rev.coint_pvalue >= 0.05 * 2:
        return None
    if pair.fig_rev.ks_pvalue < 0.05 * 2:
        return None
    """

    """
    if abs(pair.fig_str.value) >= 30:
        # 너무 벌어졌다.
        return None
    """
        
    """
    if abs(pair.fig_str.value) < 10:
        # 충분히 벌어지지 않았다.
        return None
    """

    basket = Basket(pair)

    repr0 ='[%s] BUY' % (basket.date.date())
    repr1 ='%s(%s1) %d' % (basket.name1, basket.pos1, basket.buy_close1)
    repr2 ='%s(%s%.3f) %d'%(basket.name2,basket.pos2,basket.coint,basket.buy_close2)
    #inspect.stack()[0][3]
    write_simul('%s %s - %s' % (repr0, repr1, repr2))

    return basket

def putin_gg1(pair):
    if exists(pair.stock1.code, pair.stock2.code, baskets):
        return None

    if check_base_factor(pair) == False:
        return None

    #if pair.fig_str.ks_pvalue < 0.05:       # 정규성
    if pair.fig_str.ks_pvalue < 0.1:       # 정규성
        return None
    if pair.fig_str.adf_pvalue >= 0.05:     # 정상성
        return None
    if pair.fig_str.coint_pvalue >= 0.05:   # 공적분
        return None

    if not target_field(pair.stock1, pair.stock2):
        return None

    """
    if pair.stock1.avg_v50 < 3000 or pair.stock2.avg_v50 < 3000:
        return None
    """

    #if 0.05 < pair.fig_str.place / pair.fig_str.place_cnt < 0.95:
    #if 0.05 < pair.fig_str.place / pair.fig_str.place_cnt < 0.95:
    if 0.1 < pair.fig_str.place / pair.fig_str.place_cnt < 0.9:
        return None

    # 너무 많은 비율 차이가 있으면 매매하기 적합하지 않음
    #if 0.6 <= pair.fig_str.coint_calc <= 1.6:
    if 0.5 <= pair.fig_str.coint_calc <= 1.5:
        pass
    else:
        return None

    if pair.coint_std >= 0.5:
        return None

    """
    if pair.fig_str.cy10_cnt < 6:
        return None
    """

    """
    if pair.corr_std >= 0.2:
        return None
    if pair.coint_std >= 0.2:
        return None

    """

    if pair.fig_str.value > 0:
        if pair.fig_str.spread_max > pair.fig_str.value + 5:
            return None
    else:
        if pair.fig_str.spread_min < pair.fig_str.value - 5:
            return None

    # 너무 비대칭인 페어는, 제대로 동작 안할 확률이 높다.
    """
    if 0.3 < pair.fig_rev.place / pair.fig_rev.place_cnt < 0.7:
        return None
    if pair.fig_rev.ks_pvalue < 0.1:       # 정규성
        return None
    if pair.fig_rev.adf_pvalue >= 0.05 * 2:
        return None
    if pair.fig_rev.coint_pvalue >= 0.05 * 2:
        return None
    if pair.fig_rev.ks_pvalue < 0.05 * 2:
        return None
    """

    """
    if abs(pair.fig_str.value) >= 30:
        # 너무 벌어졌다.
        return None
        
    if abs(pair.fig_str.value) < 10:
        # 충분히 벌어지지 않았다.
        return None
    """

    basket = Basket(pair)

    repr0 ='[%s] BUY' % (basket.date.date())
    repr1 ='%s(%s1) %d' % (basket.name1, basket.pos1, basket.buy_close1)
    repr2 ='%s(%s%.3f) %d'%(basket.name2,basket.pos2,basket.coint,basket.buy_close2)
    #inspect.stack()[0][3]
    write_simul('%s %s - %s' % (repr0, repr1, repr2))

    return basket

#82%
def putin_gg(pair):
    if exists(pair.stock1.code, pair.stock2.code, baskets):
        return None

    if check_base_factor(pair) == False:
        return None

    #if pair.fig_str.ks_pvalue < 0.05:       # 정규성
    if pair.fig_str.ks_pvalue < 0.1:       # 정규성
        return None
    if pair.fig_str.adf_pvalue >= 0.05:     # 정상성
        return None
    if pair.fig_str.coint_pvalue >= 0.05:   # 공적분
        return None

    if not target_field(pair.stock1, pair.stock2):
        return None

    """
    if pair.stock1.avg_v50 < 3000 or pair.stock2.avg_v50 < 3000:
        return None
    """

    if 0.05 < pair.fig_str.place / pair.fig_str.place_cnt < 0.95:
    #if 0.1 < pair.fig_str.place / pair.fig_str.place_cnt < 0.9:
        return None

    # 너무 많은 비율 차이가 있으면 매매하기 적합하지 않음
    if 0.6 <= pair.fig_str.coint_calc <= 1.6:
        pass
    else:
        return None

    if pair.coint_std >= 0.4:
        return None
    """
    if pair.corr_std >= 0.4:
        return None
    """
    """
    if pair.corr_std >= 0.2:
        return None
    if pair.coint_std >= 0.2:
        return None

    if pair.fig_str.cy10_cnt < 6:
        return None
    """

    if pair.fig_str.value > 0:
        if pair.fig_str.spread_max > pair.fig_str.value + 5:
            return None
    else:
        if pair.fig_str.spread_min < pair.fig_str.value - 5:
            return None

    # 너무 비대칭인 페어는, 제대로 동작 안할 확률이 높다.
    """
    if 0.3 < pair.fig_rev.place / pair.fig_rev.place_cnt < 0.7:
        return None
    if pair.fig_rev.ks_pvalue < 0.1:       # 정규성
        return None
    if pair.fig_rev.adf_pvalue >= 0.05 * 2:
        return None
    if pair.fig_rev.coint_pvalue >= 0.05 * 2:
        return None
    if pair.fig_rev.ks_pvalue < 0.05 * 2:
        return None
    """

    """
    if abs(pair.fig_str.value) >= 30:
        # 너무 벌어졌다.
        return None
    """
        
    if abs(pair.fig_str.value) < 10:
        # 충분히 벌어지지 않았다.
        return None

    basket = Basket(pair)

    repr0 ='[%s] BUY' % (basket.date.date())
    repr1 ='%s(%s1) %d' % (basket.name1, basket.pos1, basket.buy_close1)
    repr2 ='%s(%s%.3f) %d'%(basket.name2,basket.pos2,basket.coint,basket.buy_close2)
    #inspect.stack()[0][3]
    write_simul('%s %s - %s' % (repr0, repr1, repr2))

    return basket

def simul_day(start, end, strat, baskets):
    print('simul_day')

    prrt = 0
    delta = end - start

    for i in range(delta.days + 1):
        date = start + timedelta(i)
        prrt += strat(date, date, baskets)
    return prrt

def simul_month(start, end, strat, baskets):
    print('simul_month')

    prrt = 0
    date = start

    while True:
        date1 = date
        date2 = date + relativedelta(months=1) - timedelta(days=1)

        t = datetime.now()
        print('*', date1.date(), date2.date())
        prrt += strat(date1, date2, baskets)
        print('    =>', datetime.now() - t)

        date = date2 + timedelta(days=1)

        if date > end:
            break;
    return prrt

if __name__ == '__main__':
    prrt = 0
    baskets = list()
    start = datetime(2018, 1, 1, 0, 0)
    #end   = datetime(2019, 3,31, 0, 0)

    #start = datetime(2019, 6, 1, 0, 0)
    end   = datetime(2019, 9,30, 0, 0)

    #start = datetime(2018, 2,10, 0, 0)
    #end   = datetime(2018, 2,20, 0, 0)

    delta = end - start
    if delta.days <= 0:
        sys.exit()
    
    before = datetime.now()
    write_new_simul()

    write_simul('===== SIMUL', before)

    prrt = simul_day(start, end, strat1, baskets)
    prrt_hold = 0
    for basket in baskets:
        if basket.pos1 == D_POS_LONG:
            write_simul('HOLDING', basket.date.date(), basket.name1, basket.buy_close1, '-', basket.name2, basket.buy_close2)
        else:
            write_simul('HOLDING', basket.date.date(), basket.name2, basket.buy_close2, '-', basket.name1, basket.buy_close1)
        prrt_hold += calc_prrt(basket, end)

    write_simul('TOTAL PRRT:', str(prrt)[0:5])
    prrt = prrt + prrt_hold
    write_simul('TOTAL INCLUDE HOLDING PRRT:', str(prrt)[0:5])
    print('after', datetime.now() - before)
