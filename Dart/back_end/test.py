import sys
sys.path.append('../../')
import time
import requests
from task.reportparser import report_1, report_2
from db.models import Disc
from commons.utils.parser import get_ba_cell, get_rows_cell, elim_tag, get_key_value, with_commas, to_number
from task.parser import valid_value, correct_value, get_ratio, get_sales_yoy

import requests
import sys
sys.path.append('../../')
import aiohttp
import asyncio
from datetime import datetime
from task.parser import get_value
from task.reportparser import report_1, report_2
from task.htmlparser import regex_content
from util import trim
from constants import *

url = 'http://dart.fss.or.kr/report/viewer.do?rcpNo=20210527000053&dcmNo=8085979&eleId=2&offset=3079&length=6097&dtd=dart3.xsd'
url = http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20200914900081
#html = requests.get(url).text

async def fetch_html(corp_name, report_nm, url_rcept):
    #http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20200914900081
    print('fetch_html:', datetime.now(), corp_name, url_rcept)
    async with aiohttp.ClientSession() as session:
        async with session.get(url_rcept) as response:
            html = await response.read()
            html = html.decode('euc-kr', 'ignore')
            #print(html)
            content = regex_content(report_nm, html)
    return content

asyncio.run(fetch_html('위더스제약', '무상증자결정', url))

"""
import sys
sys.path.append('../../')
from api.disc import fetch_html
import asyncio

corp_name = '알리코제약'
report_nm = '주요사항보고서(무상증자결정)'
url_rcept = 'http://dart.fss.or.kr/report/viewer.do?rcpNo=20210601000036&dcmNo=8094327&eleId=2&offset=3061&length=6873&dtd=dart3.xsd'

asyncio.run(fetch_html(corp_name, report_nm, url_rcept))

권리락일은 신주배정일  T-2 일  26일-1 => 23일,  26일-2 => 22일

"""

"""
import requests
import json
import pprint
import time
import sys
sys.path.append('../../')
from commons.basedb.models import Ohlcv, StockKr, CandleKr, StockUs, CandleUs
from constants import *
from db.models import Corp, Fnltt

codes = [stock.code for stock in StockKr.objects.raw({'aimed':{'$ne':'ETF'}})]
codes.__len__()

corps = [{'corp_code':corp.corp_code,'corp_name':corp.corp_name,'stock_code':corp.stock_code} for corp in Corp.objects.raw({'stock_code':{'$in':codes}}).raw({'stock_code':{'$gte':'000000'}}).order_by([('stock_code',1)])]


bsns_years = [
     '2016'
    ,'2017'
    ,'2018'
    ,'2019'
    ,'2020'
    ,'2021'
]

reprt_codes = [
     '11013' # 1분기보고서
    ,'11012' # 반기보고서
    ,'11014' # 3분기보고서
    ,'11011' # 사업보고서
]

n = 800
for i in range(0, corps.__len__(), n):
    print('loop', f'[{i}~{i+n}] / {corps.__len__()}')
    corp_codes = str([corp['corp_code'] for corp in corps[i:i+n]]).replace("'",'').replace(' ','').replace('[','').replace(']','')
    for bsns_year in bsns_years:
        for reprt_code in reprt_codes:
            url = DART_FNLTT_MUL_URL.format(corp_codes, bsns_year, reprt_code)
            html = requests.get(url).text
            time.sleep(2)
            if html.find('"status":"000"') < 0:
                continue
            dict = json.loads(html)
            for index, d in enumerate(dict['list']):
                if d['fs_div'] != 'CFS': # 연결재무제표
                    continue
                if d['sj_div'] != 'IS':  # 손익계산서
                    continue
                if d['ord'] != '27':     # 법인세차감전 순이익
                    continue
                Fnltt(d).save()

cnt = corps.__len__()
for index, corp in enumerate(corps):
    print(corp['corp_code'], corp['corp_name'], corp['stock_code'], f'{index}/{cnt}')
    for bsns_year in bsns_years:
        for reprt_code in reprt_codes:
            url = DART_FNLTT_SGL_URL.format(corp['corp_code'],bsns_year, reprt_code)
            html = requests.get(url).text
            time.sleep(10)  #10초에 한건 하루 만건이하로 해야함.
            if html.find('"status":"000"') < 0:
                continue
            dict = json.loads(html)
            for d in dict['list']:
                print(bsns_year, corp['stock_code'], f'{index}/{cnt}')
                Fnltt(d).save()

#Fnltt.objects.raw({'stock_code':'104540','bsns_year':{'$gte':'2018'}}).delete()

#url= f'https://opendart.fss.or.kr/api/fnlttMultiAcnt.json?crtfc_key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&corp_code={cs8}&bsns_year=2018&reprt_code=11011'
#r = requests.get(url)
#r.status_code
#cs8 = cs[0:7992]
"""


#url = DART_FNLTT_URL.format('00126380', '2021', '11013')
#url = DART_FRIC_DECSN_URL.format('00172945','20211014','20211014')

#2021/10/27 오후 5시20분에 조회함
#url = DART_PIIC_DECSN_URL.format('00585219','20211027','20211027')
#requests.get(url).text

