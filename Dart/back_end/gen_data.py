import sys
import time
import requests
sys.path.append('../../')
from server import api
from job import post_disc_kr
from db.models import StdDisc, Disc
from task.htmlparser import get_doc_url, regex_tot_page, regex_disc_board
from task.parser import get_value
from task.reportparser import report_2, report_2_new, report_3
from datetime import datetime, timedelta
from api.disc import get_std_disc
from commons.utils.datetime import str_to_datetime, datetime_to_str
from constants import *
   
def new_doc_url(begin, end):
    date1 = str_to_datetime(begin,'%Y%m%d')
    date2 = str_to_datetime(end,  '%Y%m%d')

    delta = date2 - date1
    for i in range(delta.days + 1):
        date = datetime_to_str(date1 + timedelta(i),'%Y%m%d')
        print(date)
        discs = Disc.objects.raw({'rcept_dt':date})
        cnt =  discs.count() 
        for index, disc in enumerate(discs):
            print(f'{index} / {cnt}', disc.rcept_dt, disc.corp.corp_name, disc.report_nm, disc._id)
            disc.url = get_doc_url(disc.rcept_no)
            disc.save()
            time.sleep(0.7)

def get_disc_board(date):
    disc_board = {}
    selectDate = datetime_to_str(str_to_datetime(date,'%Y%m%d'),'%Y.%m.%d')
    for sosok in ['Y', 'K']:
        for page in range(1, 1000):
            time.sleep(1)
            url = f'http://dart.fss.or.kr/dsac001/main{sosok}.do?selectDate={selectDate}&sort=&series=&mdayCnt=0&currentPage={page}'
            html = requests.get(url).text
            tot_page  = regex_tot_page(html)
            disc_page = regex_disc_board(html)
            disc_board.update(disc_page)
            print(url, f'{sosok} {page}/{tot_page}')
            if page >= tot_page:
                break
    return disc_board

def set_disc_time(begin, end):
    date1 = str_to_datetime(begin,'%Y%m%d')
    date2 = str_to_datetime(end,  '%Y%m%d')

    delta = date2 - date1
    for i in range(delta.days + 1):
        date  = datetime_to_str(date1 + timedelta(i),'%Y%m%d')
        discs = Disc.objects.raw({'rcept_dt':date})
        if discs.count() == 0:
            continue

        disc_board = get_disc_board(date)
        for index, disc in enumerate(discs):
            if disc.rcept_no in disc_board:
                disc.reg_time = disc_board[disc.rcept_no]
                disc.save()

# 무상증자 결정
def set_contents_report_2_bak(begin, end):
    discs = Disc.objects.raw({'rcept_dt':{'$gte':begin,'$lte':end}}).order_by([('rcept_dt',1)])
    for disc in discs:
        if disc.report_nm.find('상증자결정') < 0:
            continue
        if disc.report_nm.find('무') < 0:
            continue
        if disc.report_nm.find('첨부정정') >= 0:
            continue
        if disc.report_nm.find('유') > 0:
            continue
        print(disc.rcept_dt, disc.report_nm, disc.url)
        corp_code, bgn_de, end_de = disc.corp.corp_code, disc.rcept_dt, disc.rcept_dt

        url = DART_FRIC_DECSN_URL.format(corp_code,bgn_de,end_de)
        html = requests.get(url).text
        if html.find('"status":"000"') < 0:
            print('EEEEE', corp_code,bgn_de, url)
            break
        disc.content = report_2_new(html)
        disc.save()
        print(disc.content)
        time.sleep(10)  #10초에 한건 하루 만건이하로 해야함.

        """
        html = requests.get(disc.url).text
        disc.content = report_2(html)
        if not disc.content:
            disc.content = disc.report_nm
        disc.save()
        print(disc.content)
        #time.sleep(0.8)
        time.sleep(10)
        """
#무상증자결정
def set_contents_report_2(begin, end):
    discs = Disc.objects.raw({'rcept_dt':{'$gte':begin,'$lte':end}}).order_by([('rcept_dt',1)])
    for disc in discs:
        if disc.report_nm.find('무상증자결정') < 0:
            continue
        if disc.report_nm.find('기재정정') > 0:
            continue
        print(disc.rcept_dt, disc.report_nm, disc.url)
        corp_code, bgn_de, end_de = disc.corp.corp_code, disc.rcept_dt, disc.rcept_dt

        url = DART_FRIC_DECSN_URL.format(corp_code,bgn_de,end_de)
        html = requests.get(url).text
        if html.find('"status":"000"') < 0:
            print('EEEEE', corp_code,bgn_de, url)
            break
        disc.content = report_2_new(html)
        disc.save()
        print(disc.content)
        time.sleep(10)  #10초에 한건 하루 만건이하로 해야함.

# 유무상증자결정
def set_contents_report_3(begin, end):
    discs = Disc.objects.raw({'rcept_dt':{'$gte':begin,'$lte':end}}).order_by([('rcept_dt',1)])
    for disc in discs:
        if disc.report_nm.find('유무상증자결정') < 0:
            continue
        if disc.report_nm.find('기재정정') > 0:
            continue
        print(disc.rcept_dt, disc.report_nm, disc.url)
        corp_code, bgn_de, end_de = disc.corp.corp_code, disc.rcept_dt, disc.rcept_dt
        url = DART_PIFRIC_DECSN_URL.format(corp_code,bgn_de,end_de)
        html = requests.get(url).text
        if html.find('"status":"000"') < 0:
            print('EEEEE', corp_code,bgn_de, url)
            break
        disc.content = report_3(html)
        disc.save()
        print(disc.content)
        time.sleep(10)  #10초에 한건 하루 만건이하로 해야함.

def set_std_disc(begin, end):
    discs = Disc.objects.raw({'rcept_dt':{'$gte':begin,'$lte':end}}).order_by([('rcept_dt',1)])

    for disc in discs:
        print(disc.rcept_dt)
        std_disc = get_std_disc(disc.report_nm)
        disc.std_disc = std_disc._id
        disc.save()

if __name__ == '__main__':
    pass
    #2010/01/01 ~ 현재
    #post_disc_kr('20130809', '20131231')
    #set_disc_time('20130101','20131231')
    #set_std_disc('20130101', '20131231')
    #new_doc_url('20210226','20211231')
    #set_contents_report_2('20100101', '20301231')

    #post_disc_kr('20101001', '20101231')
    #set_disc_time('20100101','20101231')
    #set_contents_report_2('20210501', '20210611')
    #set_contents_report_2('20210826', '20220830')
    set_contents_report_3('20210826', '20220830')
    #set_std_disc('20120101', '20121231')

