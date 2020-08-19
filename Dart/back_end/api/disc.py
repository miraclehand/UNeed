from flask_restful import Resource
from flask import request
from datetime import datetime
from dateutil.relativedelta import relativedelta
from db.models import User, Corp, Disc, NewDisc, UserDisc, UserWatch, Watch, StdDisc
from db.models import Alert, Room
from app import app
from util import write_log, trim
from api.util import to_json
from api.corp import fetch_corps
from constants import *
from task.htmlparser import regex_disc, regex_tick, regex_new_disc
from task.htmlparser import regex_content
from task.parser import elim_tag
from task.singleton import pool_corps, ua, od
from bson import ObjectId
from random import randint
import aiohttp
import asyncio
import xml.etree.ElementTree as elemTree
import time
import requests, zipfile, io, os

FETCH_CNT = 1

def get_std_disc(report_nm):
    report_nm = elim_tag(report_nm, '[', '', ']')
    report_nm = elim_tag(report_nm, '(', '', ')')
    try:
        std_disc = StdDisc.objects.get({'report_nm':report_nm})
    except:
        id = StdDisc.objects.count() + 1
        std_disc = StdDisc(id, report_nm)
        std_disc.save()
    return std_disc

def fetch_retrive_disc(corp_cls, page_no):
    url = DART_LIST_URL.format(100) + f'page_no={page_no}&corp_cls={corp_cls}'
    r = requests.get(url)

    disc = regex_disc(r.text)
    if not disc:
        return {'list':''}
    if page_no == int(disc['total_page']):
        return disc

    return {'total_page':disc['total_page'],
            'total_count':disc['total_count'],
            'list':disc['list'] + fetch_retrive_disc(cls, page_no + 1)['list']
    }

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
                    'stock_code'   : ' ',
                    'modify_date': datetime.now().strftime('%Y%m%d')}

    corp = Corp(new_corp).save()

    return corp

async def request_tick(disc, req_date=None):
    tick = 0
    code     = disc['corp'].stock_code
    rcept_dt = disc['rcept_dt']

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
        async with session.get(url) as response:
            html = await response.read()
            html = html.decode('euc-kr', 'ignore')

            tick = regex_tick(html)

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

def get_watch_room(alert, watch):
    for room in alert.rooms:
        if room.watch._id == watch._id:
            return room
    return Room(watch)

def new_user_disc(alert, watchs, disc):
    for watch in watchs:
        room = get_watch_room(alert, watch)

        room.discs.append(disc)
        alert.add_or_replace_room(room)

def post_broadcast_bak(user, disc):
    body = {
        to: user.PushToken,
        sound: 'default',
        title: 'title of dart.uneed',
        body: 'body of dart.uneed',
        data: { disc: disc.to_dict },
        _displayInForeground: true,
    }
    """
    body = json.dumps({
        to: PushToken,
        sound: 'default',
        title: title,
        body: body,
        data: { data: content },
        _displayInForeground: true,
    })
    """

    requests.post(BROAD_CAST_URL, headers=BROAD_CAST_HEADERS, data=body)

def post_broadcast(user, disc):
    body = json.dumps({
        'to': user.PushToken,
        'sound': 'default',
        'title': 'title of dart.uneed',
        'body': 'body of dart.uneed',
        'data': { 'disc': disc.to_dict },
        '_displayInForeground': 1,
    })
    """
    body = json.dumps({
        to: PushToken,
        sound: 'default',
        title: title,
        body: body,
        data: { data: content },
        _displayInForeground: true,
    })
    """

    requests.post(BROAD_CAST_URL, headers=BROAD_CAST_HEADERS, data=body)

async def fetch_content(url_rcept, cnt):
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
                    await time.sleep(10)
                return await fetch_content(url_rcept, cnt + 1)
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
        return fetch_content(url_rcept, cnt + 1)

    try:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        name = z.namelist()[0]
        filename = z.extract(name, 'data/')
        os.system(f'iconv -f euc-kr -t utf-8 {filename} > {filename}.out')
        os.system(f'rm {filename}')
    except Exception as ex:
        print('except fetch_content', ex)
    return f'{filename}.out'
    """

async def make_content(disc):
    rcept_dt = disc['rcept_dt']
    tick = disc['tick']
    url_rcept = DART_DOC_URL.format(disc['rcept_no'])
    date = disc['rcept_no'][:8]

    cnt = 1 if date == datetime.now().strftime('%Y%m%d') else FETCH_CNT
    content = await fetch_content(url_rcept, cnt)

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
        content = regex_content(html)
    except Exception as ex:
        print('except make_content', ex, html[0:100])
        content = url_rcept
    finally:
        f.close()
    os.system(f'rm {filename}')

    print('make_content', content, tick, '===>', disc['report_nm'] )
    return f'{content}\n * 공시알림시각 주가:{tick:,}원'

async def async_fetch_disc(disc):
    if disc['corp_cls'] not in ('Y', 'K'):
        return None
    if not disc['rm']:
        disc['rm'] = ' '

    disc['corp']     = save_if_new_corp(disc)
    disc['std_disc'] = get_std_disc(disc['report_nm'])
    disc['tick']     = await request_tick(disc, disc['rcept_dt'] + '1600')
    disc['content']  = await make_content(disc)

    return disc

class DiscAPI(Resource):
    def __init__(self):
        super(DiscAPI, self).__init__()

    def get(self, cntry=None, id=None):
        write_log(request.remote_addr,'disc get',cntry)

        date1 = request.args.get('date1')
        date2 = request.args.get('date2')

        if cntry == 'kr': discs = Disc.objects.order_by([('_id',-1)]).limit(100)
        if cntry == 'us': discs = Disc.objects.order_by([('_id',-1)]).limit(100)

        if id:
            discs = discs.get({'code':id})
        else:
            discs = list(discs)

        return {'discs':to_json(discs)}

    #update-task
    def put(self, cntry=None):
        url = DART_LIST_URL.format(50)
        r = requests.get(url)

        disc = regex_disc(r.text)
        if not disc:
            return
        if disc['total_count'] == od.get_total_count():
            return
        od.set_total_count(disc['total_count'])

        try:
            last_disc = Disc.objects.order_by([('_id',-1)]).first()
        except:
            last_disc = None

        hhmm = datetime.now().strftime('%H:%M')
        new_discs = regex_new_disc(hhmm, disc, last_disc)
        if not new_discs:
            return

        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        tasks = [asyncio.ensure_future(async_fetch_disc(disc)) for disc in new_discs]
        new_discs = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()

        new_discs = list(reversed(new_discs))
        ids = Disc.objects.bulk_create([Disc(disc) for disc in new_discs])

        new_discs = Disc.objects.raw({'_id' : {'$in': ids } })
        for disc in new_discs:
            watchers = being_watched(disc.corp.stock_code, disc.std_disc)
            if not watchers:
                continue

            for watcher in watchers:
                user, watchs = watcher.user, watcher.watchs
                if not watchs:
                    continue
                print('watcher', user.email, disc.corp.corp_name, disc.content)
                if user.email == 'web':
                    try:
                        alert = Alert.objects.get({'user':user._id})
                    except:
                        alert = Alert(user)
                    new_user_disc(alert, watchs, disc)
                    alert.save()
                else:
                    post_broadcast(user, disc)

    #add-task
    def post(self, cntry=None):
        write_log(request.remote_addr,'disc post',cntry)

        Disc.objects.delete()

        page_no = 1
        page_count = 1000
        total_page = 1000
        now = datetime.now()
        bgn_de = (now - relativedelta(months=1)).strftime('%Y%m%d')
        end_de = now.strftime('%Y%m%d')

        while total_page >= page_no:
            url = DART_LIST_URL.format(page_count) + f'&bgn_de={bgn_de}&end_de={end_de}&page_no={page_no}&last_reprt_at=N'

            r = requests.get(url)
            total_page = r.json()['total_page']
            new_discs  = r.json()['list']

            print(f'##### {url} fetch {page_no}/{total_page}')

            event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop)
            tasks = [asyncio.ensure_future(async_fetch_disc(disc)) for disc in new_discs]
            new_discs = event_loop.run_until_complete(asyncio.gather(*tasks))
            event_loop.close()
            #print(new_discs)

            new_discs = list(reversed(new_discs))
            ids = Disc.objects.bulk_create([Disc(disc) for disc in new_discs])

            page_no = page_no + 1
            if page_no >= total_page:
                break;

    #add-task
    def post_bak(self, cntry=None):
        write_log(request.remote_addr,'disc post',cntry)

        Disc.objects.delete()

        page_no = 1
        page_count = 1000
        total_page = 1000
        now = datetime.now()
        bgn_de = (now - relativedelta(months=3)).strftime('%Y%m%d')
        end_de = now.strftime('%Y%m%d')

        while total_page >= page_no:
            url = DART_LIST_URL.format(page_count) + f'&bgn_de={bgn_de}&end_de={end_de}&page_no={page_no}&last_reprt_at=N'

            r = requests.get(url)
            total_page = r.json()['total_page']
            new_discs  = r.json()['list']

            print(f'##### {url} fetch {page_no}/{total_page}')
            for disc in new_discs:
                if disc['corp_cls'] not in ('Y', 'K'):
                    continue
                if not disc['rm']:
                    disc['rm'] = ' '

                disc['corp'] = save_if_new_corp(disc)
                disc['tick'] = request_tick(disc, disc['rcept_dt'] + '1600')
                disc['content'] = make_content(disc)
                disc['std_disc'] = get_std_disc(disc['report_nm'])

            new_discs = list(reversed(new_discs))
            ids = Disc.objects.bulk_create([Disc(disc) for disc in new_discs])

            page_no = page_no + 1
            if page_no >= total_page:
                break;

    #delete-task
    def delete(self, cntry=None):
        write_log(request.remote_addr,'disc delete',cntry)

        Disc.objects.delete()

class UserDiscAPI(Resource):
    def __init__(self):
        super(UserDiscAPI, self).__init__()

    def get(self, cntry=None, id=None):
        write_log(request.remote_addr,'user disc get',cntry)

        date1 = request.args.get('date1')
        date2 = request.args.get('date2')

        user = User.objects.get({'email':'web'})
        """
        if cntry == 'kr': c = UserDisc.objects.raw({'user':{'$eq':user._id}})
        if cntry == 'us': c = UserDisc.objects.raw({'user':{'$eq':user._id}})

        discs = c.aggregate({'$project':{'user_discs':1}},{'$unwind': '$user_discs'}, {'$sort':{'user_discs._id':-1}})
        """
        return ''
        if cntry == 'kr': c = UserDisc.objects.get({'user':user._id}).user_discs
        if cntry == 'us': c = UserDisc.objects.get({'user':user._id}).user_discs

        # To sort the list in place...
        c.sort(key=lambda x: x.reg_time, reverse=True)

        return {'discs':to_json(c[-100:])}

        return {'discs':to_json(discs)}
        discs = discs.order_by([('rcept_dt',-1),('reg_time',-1)])

        if id:
            discs = discs.get({'code':id})
        else:
            discs = list(discs)

        return {'discs':to_json(discs)}

    #update-task
    def put(self, cntry=None):
        print('put')
        new_discs = NewDisc.objects.all()
        """
        keywords = Keyword.objects.all()

        if new_discs.count() == 0:
            return

        for keyword in keywords:
            word = keyword.keyword

            added_discs = [new_disc for new_disc in new_discs if word in new_disc.corp.corp_name + new_disc.report_nm]

            for added_disc in added_discs:
                print('send_post')
                #send_post(keyword.user, added_disc)

        NewDisc.objects.delete()
        """

        """
        for disc in new_discs:
            i = i + 1
            _ids.append(disc._id)
            print('gogo1',i )

            [added_disc for added_disc in keyword]

            for keyword in keywords:
                word = keyword.keyword
                try:
                    user_disc = UserDisc.objects.get({'user':keyword.user._id})
                except Exception as ex:
                    user_disc = UserDisc(keyword.user)

                user_discs = user_disc.user_discs
                if word in disc.corp.corp_name or word in disc.report_nm:
                    added_disc.append()
                    user_discs.append(disc)
                    user_disc.user_discs.append(disc)
                    user_disc.save()

                if aaa:
                    user_disc.user_discs.extend([disc for disc in discs  ])
                    user_disc.save()
                
        """


        """
        keywords = Keyword.objects.all()

        for keyword in keywords:
            for disc in discs:
                word = keyword.keyword
                if word in disc.corp.corp_code or word in disc.corp.corp_name or word in disc.report_nm:
                    try:
                        user_disc = UserDisc.objects.get({'user':keyword.user._id})
                    except Exception as ex:
                        user_disc = UserDisc(keyword.user)
                    user_disc.user_discs.append(disc)
                    user_disc.save()
        """


    #add-task
    def post(self, cntry=None):
        pass
        """
        discs = list(reversed(discs))

        model_discs = list()
        for disc in discs:
            model_discs.append(Disc(disc).save())

        keywords = Keyword.objects.all()

        print('len', model_discs.__len__(), keywords.__len__())
        for model_disc in model_discs:
            for keyword in keywords:
                word = keyword.keyword
                if word in model_disc.corp.corp_code or word in model_disc.corp.corp_name or word in model_disc.report_nm:
                    try:
                        user_disc = UserDisc.objects.get({'user':keyword.user._id})
                    except Exception as ex:
                        user_disc = UserDisc(keyword.user)
                    user_disc.user_discs.append(model_disc)
                    user_disc.save()
                    #print('send_push_message')
                    #send_push_message('token', 'message')
        return


        _ids = Disc.objects.bulk_create([Disc(disc) for disc in discs])

        keywords = Keyword.objects.all()
        for _id in _ids:
            disc = Disc.objects.get({'_id':_id})

            for keyword in keywords:
                word = keyword.keyword
                if word in disc.corp.corp_code or word in disc.corp.corp_name or word in disc.report_nm:
                    try:
                        user_disc = UserDisc.objects.get({'user':keyword.user._id})
                    except Exception as ex:
                        user_disc = UserDisc(keyword.user)
                    user_disc.user_discs.append(disc)
                    user_disc.save()
                    #print('send_push_message')
                    #send_push_message('token', 'message')
        """

    #delete-task
    def delete(self, cntry=None):
        pass
