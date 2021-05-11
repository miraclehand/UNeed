from flask_restful import Resource
from datetime import datetime, timedelta
from task.htmlparser import regex_tick, regex_ticks
from task.singleton import pool_ticks
from task.mfg.reproduce import get_ohlcv_pool
from commons.utils.datetime import str_to_datetime
import requests
import asyncio
import aiohttp
import pandas as pd
import numpy as np
from constants import *
from db.models import Disc

def get_ticks_pool(code):
    ticks = pool_ticks.get(code)
    if ticks is None:
        thistime = datetime.now().strftime('%Y%m%d') + '1540'
        ticks = fetch_ticks(thistime, code)
        pool_ticks.set(code, ticks)
    return ticks

async def async_request_ticks(url):
    ticks = dict()
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=REQUESTS_HEADERS) as response:
            html = await response.read()
            html = html.decode('euc-kr', 'ignore')
            ticks = regex_ticks(html)
    return ticks

def fetch_ticks(thistime, code):
    #390분동안 매매가 가능하기 때문에 최대 39페이지를 조회해야 한다.
    urls = [f'https://finance.naver.com/item/sise_time.nhn?code={code}&thistime={thistime}00&page={page}' for page in range(1,30)]

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    tasks = [asyncio.ensure_future(async_request_ticks(url)) for url in urls]
    fetched_ticks = event_loop.run_until_complete(asyncio.gather(*tasks))
    event_loop.close()

    ticks = dict()
    for tick in fetched_ticks:
        ticks.update(tick)

    df = pd.DataFrame.from_dict(ticks, orient='index', columns=['tick'])

    return df

def get_high_tick(time, df):
    value = df.loc[:time].max().values[0]
    if np.isnan(value):
        return df['tick'][0]
    else:
        return value

def get_low_tick(time, df):
    value = df.loc[:time].min().values[0]
    if np.isnan(value):
        return df['tick'][0]
    else:
        return value

def get_tick_date(time, df, tick):
    values = df[df['tick'] == tick].loc[:time]
    if values.empty:
        return df[df['tick'] == tick]['tick'].index[0]
    else:
        return values.index[-1]

def fetch_tick(code, thistime):
    tick = 0

    thisdate = str_to_datetime(thistime[0:8], '%Y%m%d').date()
    today = datetime.now().date()

    if thisdate == today:
        url = f'https://finance.naver.com/item/sise_time.nhn?code={code}&thistime={thistime}00&page=1'
        r = requests.get(url, headers=REQUESTS_HEADERS)
        tick = regex_tick(r.text)
        r.close()

    if tick == 0:
        df = get_ohlcv_pool(code)
        if not df.loc[:thisdate]['close'].empty:
            tick = df.loc[:thisdate]['close'][-1]   #전일종가
    return tick

class TickAPI(Resource):
    def __init__(self):
        super(TickAPI, self).__init__()

    def get(self, cntry=None, code=None, thistime=None):

        tick = fetch_tick(code, thistime)
        return tick

    #update-task
    def put(self, cntry=None):
        today = datetime.now().strftime('%Y%m%d')

        discs = Disc.objects.raw({'rcept_dt':today})
        print('put tick', cntry, today, discs.count())
        for disc in discs:
            code, rcept_time = disc.corp.stock_code, disc.reg_time
            ticks = get_ticks_pool(code)
            if ticks.empty:
                continue

            disc.high_tick = get_high_tick(rcept_time, ticks)
            disc.high_time = get_tick_date(rcept_time, ticks, disc.high_tick)
            disc.low_tick  = get_low_tick (rcept_time, ticks)
            disc.low_time  = get_tick_date(rcept_time, ticks, disc.low_tick)
            print(disc.corp.corp_name, rcept_time, disc.high_time, disc.high_tick, disc.low_time, disc.low_tick)
            disc.save()

    #add-task
    def post(self, cntry=None, begin=None, end=None):
        pass

    #delete-task
    def delete(self, cntry=None):
        pass

