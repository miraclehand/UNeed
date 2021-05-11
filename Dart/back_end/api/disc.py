from flask_restful import Resource
from flask import request
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from commons.utils.datetime import str_to_datetime, datetime_to_str
from db.models import User, Corp, Disc, NewDisc, UserDisc, UserWatch, Watch, StdDisc, StdDisc
#from db.models import Alert, Room
from db.models import UserChatRoom, ChatRoom, Chat
from flask import url_for
from app import app
from util import write_log, trim
from api.util import to_json, make_payload, post_broadcast_async
from api.tick import fetch_tick
from api.corp import fetch_corps
from constants import *
from task.htmlparser import regex_disc_page, regex_tick, regex_new_disc
from task.htmlparser import regex_content_zip, regex_content, regex_stock_code
from task.parser import elim_tag
from task.singleton import pool_corps, pool_std_discs, ua, od
from task.mfg.reproduce import get_ohlcv_pool
from bson import ObjectId
from random import randint
import json
import aiohttp
import asyncio
import xml.etree.ElementTree as elemTree
import time
import requests, zipfile, io, os

FETCH_CNT = 1
PAGE_COUNT = 50

def get_std_disc(report_nm):
    report_nm = elim_tag(report_nm, '[', '', ']')
    report_nm = elim_tag(report_nm, '(', '', ')')
    if not report_nm:
        return None
    try:
        std_disc = StdDisc.objects.get({'report_nm':report_nm})
    except:
        id = StdDisc.objects.count() + 1
        std_disc = StdDisc(id, report_nm)
        std_disc.save()
    return std_disc


def get_std_disc2(report_nm):
    print('get_std_disc', report_nm)

    if pool_std_discs.count() == 0:
        for s in StdDisc.objects.all():
            pool_std_discs.set(s.to_dict)

    std_disc = pool_std_discs.get(report_nm)

    if not std_disc:
        report_nm = elim_tag(report_nm, '[', '', ']')
        report_nm = elim_tag(report_nm, '(', '', ')')
        id = 1000 + pool_std_discs.count() + 1
        print('new_std_disc', id, report_nm)
        std_disc = StdDisc(id, report_nm)
        std_disc.save()
        pool_std_discs.set(std_disc.to_dict)

    """ javascript는 속도가 너무 안좋음
    std_disc = StdDisc.objects.raw({
        '$where': 'function() { \
            var list_keyword = this.keyword.split("|"); \
            for( var i in list_keyword) { \
                if ( \'' + report_nm + '\'.match(list_keyword[i])) { \
                    return true\
                } \
            }; \
            return false\
        }'
    })
    """
    return std_disc._id

def zip_down(content):
    try:
        z = zipfile.ZipFile(io.BytesIO(content))
        for name in z.namelist():
            filename = z.extract(name, 'data/')
            os.system(f'iconv -f euc-kr -t utf-8 {filename} > {filename}.out')
            os.system(f'rm {filename}')
    except Exception as ex:
        print('except zip_down', content.__len__(),ex)

def save_if_new_corp(disc):
    corp_code, corp_name = disc['corp_code'], disc['corp_name']
    try:
        corp = Corp.objects.get({'corp_code':corp_code})
        if corp.stock_code.strip():
            return corp
        else:
            corp.delete()
    except:
        print('save_if_new_corp', corp_code)

    if pool_corps.is_empty():
        pool_corps.set(fetch_corps())

    new_corp = pool_corps.get(corp_code)

    if not new_corp:
        new_corp = {'corp_code'  : corp_code,
                    'corp_name'  : corp_name,
                    'stock_code' : ' ',
                    'modify_date': datetime.now().strftime('%Y%m%d')}
    else:
        stock_code = new_corp.findtext('stock_code')
        if not stock_code.strip():
            #종목코드가 아직 다트에 안들어 왔을때,
            url = f'http://dart.fss.or.kr/dsae001/selectPopup.ax?selectKey={corp_code}'
            r = requests.get(url)
            stock_code = regex_stock_code(r.text)
            r.close()
        new_corp = {'corp_code'  : corp_code,
                    'corp_name'  : corp_name,
                    'stock_code' : stock_code,
                    'modify_date': datetime.now().strftime('%Y%m%d')}

    corp = Corp(new_corp).save()

    return corp

async def request_tick(disc, req_date=None):
    tick = 0
    code     = disc['corp'].stock_code
    rcept_dt = disc['rcept_dt']

    if rcept_dt != datetime.now().strftime('%Y%m%d'):
        # tick데이터는 당일이 아니면 공시일자 익영업일 시가로 계산
        df = get_ohlcv_pool(code)
        af1 = str_to_datetime(rcept_dt, '%Y%m%d').date() + relativedelta(days=1)
        tick = df.loc[af1:].head(1)['open'].values[0]

        return tick

    if req_date:
        thistime = req_date
    else:
        reg_time = disc['reg_time']
        thistime = rcept_dt + reg_time.replace(':','')

    # end of recursive 
    if int(rcept_dt) - int(thistime[0:8]) > 50:
        return 0

    url = f'https://finance.naver.com/item/sise_time.nhn?code={code}&thistime={thistime}00&page=1'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=REQUESTS_HEADERS) as response:
            html = await response.read()
            html = html.decode('euc-kr', 'ignore')

            tick = regex_tick(html)
            print('request_tick', code, rcept_dt, url, tick)

            # 장시작전에는 틱 데이터가 없다. 전일자 틱 데이터를 가져온다.
            if not tick:
                yday = datetime.strptime(thistime, "%Y%m%d%H%M") - relativedelta(days=1)
                pre_thistime = yday.strftime("%Y%m%d") + "2350"
                return await request_tick(disc, pre_thistime)
    return tick

def being_watched(stock_code, std_disc):
    watchers = UserWatch.objects.raw({
        'watchs.std_disc': std_disc._id,
        'watchs.detail.qty': 10,
        '$or': [
            { 'watchs.stock_codes':{'$eq':'000000'} },
            { 'watchs.stock_codes':{'$regex':stock_code} },
        ]
    }).project({
        'user': '1',
        'watchs': {
            '$elemMatch': {
                'std_disc': std_disc._id,
                'detail.qty': 10,
                '$or': [
                    { 'stock_codes':{'$eq':'000000'} },
                    { 'stock_codes':{'$regex':stock_code} },
                ]
            } 
        }
    })

    """
    #함수가 들어가는 where 절은 속도가 느리다.
    watchers = UserWatch.objects.raw({ \
        '$where': 'function() { \
            return this.watchs.some(function(obj) { \
                return \'' + report_nm + '\'.match(obj.report_nm) \
                    && (obj.stock_codes.match( \'' + stock_code + '\' ) \
                      ||obj.stock_codes == \'' + '000000' + '\' \
                       ) \
            }) \
        }' \
    })

    watchers = UserWatch.objects.raw({}).aggregate(
        {'$unwind': { 'path': "$watchs", 'preserveNullAndEmptyArrays': True } },
        {'$group': { '_id': {'user':"$user", 'watch': "$watchs.name"} } },
        {'$match': { "_id.watch": {'$regex': report_nm} } }
    )

    db.watch_list.aggregate([
        {
            $project: {
                watchs: {
                    $filter: {
                        input: "$watchs",
                        as: "watch",
                        cond: { $eq: [ "$$watch.name", "테스트2"]}
                    }
                }
            }
        }
    ])
    """

    return watchers

def get_room(ucr, watch):
    for room in ucr.rooms:
        if room.watch == watch:
            return room
    return ChatRoom(watch)

def add_chat(ucr, watch, chat):
    room = get_room(ucr, watch)
    room.add_chat(chat)
    room.save()
    ucr.add_or_replace_room(room)

async def exact_content(url_rcept, cnt):
    if cnt > FETCH_CNT:
        return None

    async with aiohttp.ClientSession() as session:
        async with session.get(url_rcept) as response:
            #print(response.content)
            content = await response.read()
            if 1 < cnt < FETCH_CNT:
                print(url_rcept, cnt)

            if content.__len__() < 500:
                if cnt != FETCH_CNT:
                    await time.sleep(5)
                return await exact_content(url_rcept, cnt + 1)
            else:
                return content
    return None

    """
    r = requests.get(url_rcept)
    print(url_rcept, cnt)

    if 1 < cnt < FETCH_CNT:
        print(url_rcept, cnt)

    if r.content.__len__() < 500:
        if cnt != FETCH_CNT:
            time.sleep(10)
        return exact_content(url_rcept, cnt + 1)

    try:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        name = z.namelist()[0]
        filename = z.extract(name, 'data/')
        os.system(f'iconv -f euc-kr -t utf-8 {filename} > {filename}.out')
        os.system(f'rm {filename}')
    except Exception as ex:
        print('except exact_content', ex)
    return f'{filename}.out'
    """

# zip file은 생성이 너무 늦게 된다. 따라서 사용할 수 없다.
async def fetch_zip_file(rcept_no, rcept_date):
    url_rcept = DART_DOC_URL.format(rcept_no)

    cnt = 1 if rcept_date == datetime.now().strftime('%Y%m%d') else FETCH_CNT
    content = await exact_content(url_rcept, cnt)

    try:
        z = zipfile.ZipFile(io.BytesIO(content))
        name = z.namelist()[0]
        filename = z.extract(name, 'data/')

        os.system(f'iconv -f euc-kr -t utf-8 {filename} > {filename}.out')
        os.system(f'rm {filename}')
    except Exception as ex:
        print(ex, url_rcept)
        return url_rcept

    filename =  f'{filename}.out'

    if not filename:
        return url_rcept

    f = open(filename, 'r')
    html = f.read()
    if not html:
        return url_rcept

    try:
        content = regex_content_zip(html)
    except Exception as ex:
        print('except regex_content_zip', ex, html[0:100])
        content = url_rcept
    finally:
        f.close()
    os.system(f'rm {filename}')
    return content

async def fetch_html(corp_name, report_nm, url_rcept):
    #http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20200914900081
    #print('fetch_html:', datetime.now(), corp_name, url_rcept)
    print(corp_name, report_nm, url_rcept)
    async with aiohttp.ClientSession() as session:
        async with session.get(url_rcept) as response:
            html = await response.read()
            html = html.decode('euc-kr', 'ignore')
            content = regex_content(report_nm, html)
    return content

async def make_content(disc):
    tick       = disc['tick']
    corp_name  = disc['corp_name']
    rcept_no   = disc['rcept_no']
    rcept_date = disc['rcept_no'][:8]
    report_nm  = disc['report_nm']
    url_rcept  = disc['url']

    #content = await fetch_zip_file(rcept_no, rcept_date)
    content = await fetch_html(corp_name, report_nm, url_rcept)

    #print('make_content',content, tick, disc['url'],'===>', disc['report_nm'] )
    return f'{content}\n * 공시알림시각 주가:{tick:,}원'

async def async_fillup_disc(disc):
    print('async_fillup_disc', disc['rcept_dt'], disc['corp_name'], disc['report_nm'])
    if disc['corp_cls'] not in ('Y', 'K'):
        return None
    if not disc['rm']:
        disc['rm'] = ' '

    disc['std_disc'] = get_std_disc(disc['report_nm'])
    if not disc['std_disc']:
        return None

    req_date = disc['rcept_dt'] + disc['reg_time'].replace(':','')

    disc['corp']     = save_if_new_corp(disc)

    code = disc['corp'].stock_code

    disc['tick'] = fetch_tick(code, req_date)

    disc['high_time'] = disc['reg_time']
    disc['high_tick'] = disc['tick']
    disc['low_time']  = disc['reg_time']
    disc['low_tick']  = disc['tick']

    disc['content'] = await make_content(disc)

    return disc

def fetch_disc_page(url):
    print('fetch_disc_page', url)
    r = requests.get(url)
    disc_page = regex_disc_page(r.text)
    r.close()
    if not disc_page:
        return None, 0, 0

    disc_list   = disc_page['list']
    total_count = int(disc_page['total_count'])
    total_page  = int(disc_page['total_page'])
    return disc_list, total_count, total_page

def make_new_discs(disc_list, last_disc):
    new_discs = regex_new_disc(disc_list, last_disc)
    if not new_discs:
        return None

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    tasks =[asyncio.ensure_future(async_fillup_disc(disc))for disc in new_discs]
    new_discs = event_loop.run_until_complete(asyncio.gather(*tasks))
    event_loop.close()

    new_discs = list(reversed(new_discs))
    new_discs = [Disc(disc) for disc in new_discs if disc]

    if new_discs.__len__() == 0:
        return None

    ids = Disc.objects.bulk_create(new_discs)

    return ids

class DiscAPI(Resource):
    def __init__(self):
        super(DiscAPI, self).__init__()

    def get(self, cntry=None, id=None):
        write_log(request.remote_addr,'disc get',cntry)

        date1 = request.args.get('date1')
        date2 = request.args.get('date2')

        if cntry == 'kr': discs = Disc.objects.order_by([('rcept_dt',-1),('_id',-1)]).limit(100)
        if cntry == 'us': discs = Disc.objects.order_by([('rcept_dt',-1),('_id',-1)]).limit(100)

        if id:
            discs = discs.get({'code':id})
        else:
            discs = list(discs)

        return {'discs':to_json(discs)}

    #update-task
    def put(self, cntry=None):
        url = DART_LIST_URL.format(PAGE_COUNT)
        disc_list, total_count, total_page = fetch_disc_page(url)
        if not disc_list or total_count == od.get_total_count():
            return None
        od.set_total_count(total_count)
        try:
            last_disc = Disc.objects.order_by([('rcept_dt',-1),('_id',-1)]).first()
        except:
            last_disc = None

        ids = make_new_discs(disc_list, last_disc)

        if not ids:
            return 
        new_discs = Disc.objects.raw({'_id' : {'$in': ids } })

        for disc in new_discs:
            watchers = being_watched(disc.corp.stock_code, disc.std_disc)
            if not watchers:
                continue

            for watcher in watchers:
                user, watchs = watcher.user, watcher.watchs
                ucr = UserChatRoom.objects.get({'user':user._id})

                if not watchs:
                    continue

                chats = []
                for watch in watchs:
                    chat = Chat(user, watch, 1, disc, 'content').save()
                    chats.append(chat)
                    add_chat(ucr, watch, chat)
                    #post_broadcast(user, watch, chat)
                ucr.save()

                payloads = [make_payload(chat) for chat in chats]
                post_broadcast_async(payloads)

    def put_bak(self, cntry=None):
        url = DART_LIST_URL.format(PAGE_COUNT)
        print('put1', url)
        r = requests.get(url)
        disc_page = regex_disc_page(r.text)
        r.close()

        total_page = disc_page['total_count']
        disc_list  = disc_page['list']
        if not disc_list:
            return
        if total_page == od.get_total_count():
            return
        od.set_total_count(total_page)

        try:
            last_disc = Disc.objects.order_by([('rcept_dt',-1),('_id',-1)]).first()
        except:
            last_disc = None

        new_discs = regex_new_disc(disc_list, last_disc)
        if not new_discs:
            return

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        tasks = [asyncio.ensure_future(async_fillup_disc(disc)) for disc in new_discs]
        new_discs = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()

        new_discs = list(reversed(new_discs))
        ids = Disc.objects.bulk_create([Disc(disc) for disc in new_discs])

        print('new_discs', new_discs)
        new_discs = Disc.objects.raw({'_id' : {'$in': ids } })
        for disc in new_discs:
            watchers = being_watched(disc.corp.stock_code, disc.std_disc)
            if not watchers:
                continue

            for watcher in watchers:
                user, watchs = watcher.user, watcher.watchs
                ucr = UserChatRoom.objects.get({'user':user._id})

                if not watchs:
                    continue

                chats = []
                for watch in watchs:
                    chat = Chat(user, watch, 1, disc, 'content').save()
                    chats.append(chat)
                    add_chat(ucr, watch, chat)
                    #post_broadcast(user, watch, chat)
                ucr.save()

                payloads = [make_payload(chat, '0') for chat in chats]
                post_broadcast_async(payloads)
    #add-task
    def post(self, cntry=None, begin=None, end=None):
        print('post', cntry, begin, end)
        write_log(request.remote_addr,'disc post',cntry)

        Disc.objects.raw({'rcept_dt':{'$gte':begin, '$lte':end}}).delete()

        date1 = str_to_datetime(begin,'%Y%m%d')
        date2 = str_to_datetime(end,  '%Y%m%d')

        delta = date2 - date1
        for i in range(delta.days + 1):
            date = date1 + timedelta(i)
            bgn_de = datetime_to_str(date,'%Y%m%d')
            end_de = datetime_to_str(date,'%Y%m%d')
            for corp_cls in ['Y','K']:
                page_no = 0
                page_count = 30
                total_page = 1000
                while total_page > page_no:
                    page_no = page_no + 1
                    url = DART_LIST_URL.format(page_count) + f'&corp_cls={corp_cls}&bgn_de={bgn_de}&end_de={end_de}&page_no={page_no}&last_reprt_at=N'

                    disc_list, total_count, total_page = fetch_disc_page(url)
                    if total_page == 0:
                        continue
                    print(f'{page_no} / {total_page}')
                    if not disc_list:
                        time.sleep(1)
                        continue
                    ids = make_new_discs(disc_list, None)
                    if not ids or ids.__len__() == 0:
                        time.sleep(1)
                        continue
                    print('========>', ids.__len__())
                    time.sleep(ids.__len__()+5)  #분당 100회 이상 요청하면 블락 당함


        """
        dt2 = begin - relativedelta(days=1)

        while True:
            dt1 = dt2 + relativedelta(days=1)
            dt2 = dt1 + relativedelta(months=3)
            if dt2 > end:
                dt2 = end
            if dt1 > dt2:
                break
            bgn_de = datetime_to_str(dt1,'%Y%m%d')
            end_de = datetime_to_str(dt2,'%Y%m%d')

            for corp_cls in ['Y','K']:
                page_no = 0
                page_count = 99 #FIXME
                total_page = 1000
                while total_page >= page_no:
                    page_no = page_no + 1
                    #FIXME
                    #pblntf_ty=I  거래소공시(단일판매 계약체결 포함)
                    url = DART_LIST_URL.format(page_count) + f'&corp_cls={corp_cls}&bgn_de={bgn_de}&end_de={end_de}&page_no={page_no}&last_reprt_at=N&pblntf_ty=I'

                    disc_list, total_count, total_page = fetch_disc_page(url)
                    print(f'{page_no} / {total_page}')
                    if not disc_list:
                        time.sleep(1)
                        continue
                    ids = make_new_discs(disc_list, None)
                    if not ids or ids.__len__() == 0:
                        time.sleep(1)
                        continue
                    print('========>', ids.__len__())
                    time.sleep(10)  #분당 100회 이상 요청하면 블락 당함
        """


    def post_bak(self, cntry=None, begin=None, end=None):
        print('post', cntry, begin, end)
        write_log(request.remote_addr,'disc post',cntry)

        begin = str_to_datetime(begin,'%Y%m%d')
        end   = str_to_datetime(end,  '%Y%m%d')

        Disc.objects.delete()

        dt2 = begin - relativedelta(days=1)
        while True:
            dt1 = dt2 + relativedelta(days=1)
            dt2 = dt1 + relativedelta(months=3)
            if dt2 > end:
                dt2 = end
            bgn_de = datetime_to_str(dt1,'%Y%m%d')
            end_de = datetime_to_str(dt2,'%Y%m%d')
            page_no = 0
            page_count = PAGE_COUNT
            total_page = 1000

            while total_page >= page_no:
                page_no = page_no + 1
                if page_no > 1:
                    time.sleep(40)

                url = DART_LIST_URL.format(page_count) + f'&bgn_de={bgn_de}&end_de={end_de}&page_no={page_no}&last_reprt_at=N'

                print(f'##### {url}')
                r = requests.get(url)
                disc_page = regex_disc_page(r.text)
                r.close()

                total_page = disc_page['total_page']
                disc_list  = disc_page['list']

                print(f'  => fetch {page_no}/{total_page}')
                new_discs = regex_new_disc(disc_list, None)
                if not new_discs:
                    continue

                event_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(event_loop)
                tasks = [asyncio.ensure_future(async_fillup_disc(disc)) for disc in new_discs]
                new_discs = event_loop.run_until_complete(asyncio.gather(*tasks))
                event_loop.close()

                new_discs = list(reversed(new_discs))
                ids = Disc.objects.bulk_create([Disc(disc) for disc in new_discs])
            if dt2 >= end:
                break

    #delete-task
    def delete(self, cntry=None):
        write_log(request.remote_addr,'disc delete',cntry)

        Disc.objects.delete()

class StdDiscAPI(Resource):
    def __init__(self):
        super(StdDiscAPI, self).__init__()

    def get(self, cntry=None, id=None):
        write_log(request.remote_addr,'std disc get',cntry)

        try:
            std_discs = StdDisc.objects.raw({'id':{'$lte':1000}})
        except:
            return {'std_discs':None}
    
        return {'std_discs':to_json(list(std_discs))}

    #update-task
    def put(self, cntry=None, id=None):
        pass

    #add-task
    def post(self, cntry=None, id=None):
        pass

    #delete-task
    def delete(self, cntry=None, id=None):
        pass
