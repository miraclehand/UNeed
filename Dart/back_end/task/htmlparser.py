import requests
from datetime import datetime
from task.parser import get_value
from task.reportparser import report_1, report_2
from util import trim

def regex_content(report_nm, html):
    content = ''
    if report_nm.find('[첨부정정]') >= 0:
        content = report_nm
    if report_nm.find('단일판매ㆍ공급계약체결') >= 0:
        content = report_1(html)
    elif report_nm.find('상증자결정') >= 0: #무상증자,유상증자,유무상증자
        if report_nm.find('철회') >= 0 or report_nm.find('무') < 0:
            content = report_nm
        else:
            content = report_2(html)
    else:
        content = report_nm

    if not content:
        content = report_nm
    return content

def regex_content_zip(html):
    title = get_value(html, 'font-weight:bold;text-align:center;">', '</span>')
    report_nm = title
    #report_nm = get_value(title, '/', '/')
    #print('regex_content1', '[' + title + ']')
    #title = None
    if not title:
        title = get_value(html, '<DOCUMENT-NAME', '</DOCUMENT-NAME>')
        s_idx = title.find('>') + 1
        report_nm = title[s_idx:]
        #print('regex_content2', '[' + title + ']', '[' + report_nm + ']')

    if not title:
        title = get_value(html, '<a name="#2">', '</a>')
        report_nm = title
        #print('regex_content3', '[' + title + ']', '[' + report_nm + ']')

    if not title:
        print('############################################################')

    #print('regex_content', title, report_nm)

    content = ''
    print(report_nm)
    if report_nm.find('단일판매ㆍ공급계약체결') >= 0:
        content = report_nm
    else:
        content = report_nm

    return content

def regex_stock_code(html):
    s_idx = html.find('<th scope="col">종목코드')
    value = get_value(html[s_idx:s_idx+100], '<td>', '</td>')
    return value

def get_doc_url(rcept_no):
    url = f'http://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}'
    r = requests.get(url)
    html = r.text
    r.close()

    s_idx = html.rfind('click: function() {viewDoc')

    if s_idx < 0:
        s_idx = html.find('alertInvestNotice')

    if s_idx < 0:
        return rcept_no

    viewDoc = html[s_idx:s_idx+100].split(',')
    dcmNo   = viewDoc[1].replace('\'','').strip()
    eleId   = viewDoc[2].replace('\'','').strip()
    offset  = viewDoc[3].replace('\'','').strip()
    length  = viewDoc[4].replace('\'','').strip()
    dtd     = viewDoc[5].replace('\'','').strip().split(')')[0]

    return f'http://dart.fss.or.kr/report/viewer.do?rcpNo={rcept_no}&dcmNo={dcmNo}&eleId={eleId}&offset={offset}&length={length}&dtd={dtd}'

def regex_tot_page(html):
    value = get_value(html, 'page_info">',']')
    return int(get_value(value, '/',''))

def regex_disc_board(html):
    disc_page = {}

    s_idx = html.find('table_list')
    text = html[s_idx:]
    for index, tr in enumerate(text.split('<tr')):
        if index < 2:
            continue
        tds = tr.split('<td')
        reg_time = get_value(tds[1], '>', '<')  #시간
        rcept_no = get_value(tds[3], "openReportViewer('", "')")  #보고서번호
        disc_page[rcept_no] = reg_time
    return disc_page

def regex_disc_page(html):
    page = dict()

    page['status']      = get_value(html, '"status":',     ',')
    page['page_no']     = get_value(html, '"page_no":',     ',')
    page['page_count']  = get_value(html, '"page_count":',  ',')
    page['total_count'] = get_value(html, '"total_count":', ',')
    page['total_page']  = get_value(html, '"total_page":',  ',')
    page['list']        = get_value(html, '"list":[', ']}')

    if page['status'] != '"000"':
        return None
    if not page['page_no']:
        return None
    return page

def regex_new_disc(disc_list, last_disc):
    hhmm = datetime.now().strftime('%H:%M')
    new_discs = list()
    new_disc  = dict()
    
    for disc in disc_list.split('{'):
        if disc.find('corp_code') < 0:
            continue

        new_disc['corp_cls']  = get_value(disc, '"corp_cls":"',  '",') 
        if new_disc['corp_cls'] not in ('Y', 'K'):
            continue

        new_disc['reg_time']  = hhmm
        new_disc['corp_code'] = get_value(disc, '"corp_code":"', '",')
        new_disc['corp_name'] = get_value(disc, '"corp_name":"', '",') 
        new_disc['stk_code']  = get_value(disc, '"stk_code":"',  '",') 
        new_disc['report_nm'] = get_value(disc, '"report_nm":"', '",') 
        new_disc['rcept_no']  = get_value(disc, '"rcept_no":"',  '",') 
        new_disc['flr_nm']    = get_value(disc, '"flr_nm":"',    '",') 
        new_disc['rcept_dt']  = get_value(disc, '"rcept_dt":"',  '",') 
        new_disc['rm']        = get_value(disc, '"rm":"',        '"}') 
        new_disc['url']       = get_doc_url(new_disc['rcept_no'])

        if not new_disc['rm']:
            new_disc['rm'] = ' '

        if is_new_disc(last_disc, new_disc) == False:
            return new_discs    # 뒤에 더 확인할 필요가 없다.

        new_discs.append(new_disc.copy())
    return new_discs

def regex_new_disc_bak3(discs, od_discs):
    new_discs = list()
    new_disc  = dict()

    if 'total_count' not in discs:
        return new_discs

    if 'total_count' in od_discs:
        if discs['total_count'] <= od_discs['total_count']:
            return new_discs

    for disc in discs['list'].split('{'):
        if disc.find('corp_code') < 0:
            continue
        if 'list' in od_discs:
            if disc.find(od_discs['list']) > 0:
                continue

        #new_disc['reg_time']  = hhmm
        new_disc['corp_code'] = get_value(disc, 'corp_code:', ',')
        new_disc['corp_name'] = get_value(disc, 'corp_name:', ',') 
        new_disc['stk_code']  = get_value(disc, 'stk_code:',  ',') 
        new_disc['corp_cls']  = get_value(disc, 'corp_cls:',  ',') 
        new_disc['report_nm'] = get_value(disc, 'report_nm:', ',') 
        new_disc['rcept_no']  = get_value(disc, 'rcept_no:',  ',') 
        new_disc['flr_nm']    = get_value(disc, 'flr_nm:',    ',') 
        new_disc['rcept_dt']  = get_value(disc, 'rcept_dt:',  ',') 
        new_disc['rm']        = get_value(disc, 'rm:',        '}') 

        new_discs.append(new_disc.copy())
    return new_discs

def regex_disc_bak2(html, last_disc, hhmm):
    new_discs = list()
    disc = dict()

    html = html.replace('"', '')

    for line in html.split('{'):
        if line.find('corp_code') < 0:
            continue

        disc['reg_time']  = hhmm
        disc['corp_code'] = get_value(line, 'corp_code:', ',')
        disc['corp_name'] = get_value(line, 'corp_name:', ',') 
        disc['stk_code']  = get_value(line, 'stk_code:',  ',') 
        disc['corp_cls']  = get_value(line, 'corp_cls:',  ',') 
        disc['report_nm'] = get_value(line, 'report_nm:', ',') 
        disc['rcept_no']  = get_value(line, 'rcept_no:',  ',') 
        disc['flr_nm']    = get_value(line, 'flr_nm:',    ',') 
        disc['rcept_dt']  = get_value(line, 'rcept_dt:',  ',') 
        disc['rm']        = get_value(line, 'rm:',        '}') 

        if disc['corp_cls'] not in ('Y', 'K'):
            continue

        if is_new_disc(last_disc, disc) == False:
            return new_discs    # 뒤에 더 확인할 필요가 없다.
        new_discs.append(disc.copy())
    return new_discs

def regex_disc_bak(html, last_disc):
    discs = list()
    disc  = dict()

    s_idx = html.find('<div class="table_list">')
    e_idx = s_idx + html[s_idx:].find('</table>')
    text  = html[s_idx:e_idx]

    text = text.replace('\r','').replace('\t','').replace('\n','')

    for tr_data in text.split('<tr'):
        td_data = tr_data.split('<td')

        if td_data.__len__() != 7:
            continue
        reg_time  = get_value(td_data[1], 'cen_txt">', '</td>')
        corp_cls  = get_value(td_data[2], 'ico_', '.gif')
        corp_code = get_value(td_data[2], 'openCorpInfo(\'', '\')')
        corp_name = get_value(td_data[2], '새창" >', '</a>')
        rcept_no  = get_value(td_data[3], 'rcpNo=', '"')
        report_nm = get_value(td_data[3], '새창" >', '</a>')
        flr_nm    = get_value(td_data[4], 'title="', '"')
        rcept_dt  = get_value(td_data[5], 'cen_txt">', '</td>').replace('.','')
        rm        = get_value(td_data[6], 'remark', '.gif')

        report_nm_info = get_value(report_nm, '임">', '</span>')
        
        if report_nm_info.__len__() > 0:
            report_nm_cont = report_nm[report_nm.find('/span>')+6:]
            report_nm = report_nm_info + report_nm_cont

        if corp_cls not in ('kospi', 'kosdaq'):
            continue

        disc['reg_time']  = reg_time
        disc['corp_cls']  = get_disc_corp_cls(corp_cls)
        disc['corp_code'] = corp_code
        disc['corp_name'] = corp_name
        disc['rcept_no']  = rcept_no
        disc['report_nm'] = report_nm.strip()
        disc['flr_nm']    = flr_nm
        disc['rcept_dt']  = rcept_dt
        disc['rm']        = get_disc_rm(rm)
        disc['url']       = get_doc_url(rcept_no)

        if is_new_disc(last_disc, disc) == False:
            return discs    # 뒤에 더 확인할 필요가 없다.

        discs.append(disc.copy())
    return discs

def regex_tick(html):
    diff = 0
    change = 0

    s_idx = html.find('mouseOver(this)')

    tds = html[s_idx:].split('<td')

    if tds.__len__() < 4:
        return 0, 0

    if tds[2].find('p11">') < 0:
        return 0, 0

    tick = get_value(tds[2], 'p11">', '</span>')

    if tds[3].find('ico_up') >= 0:
        diff = get_value(tds[3], 'red02">', '</span>')
    elif tds[3].find('ico_down') >= 0:
        diff = '-' + get_value(tds[3], 'nv01">', '</span>')
    else:
        diff = '0'

    tick = int(tick.replace(',','').strip())
    diff = int(diff.replace(',','').strip())
    base_close = tick + diff
    change = round((base_close - tick) / tick * 100,2)

    return tick, change
    
def regex_ticks(html):
    ticks = dict()
    for tr in html.split('<tr'):
        if tr.find('onMouseOver') < 0:
            continue
        tds = tr.split('<td')
        time = get_value(tds[1], '<span class="tah p10 gray03">', '</span>')
        tick = get_value(tds[2], '<span class="tah p11">', '</span>')
        if time and tick:
            ticks[time] = int(tick.replace(',',''))
    return ticks

def get_disc_corp_cls(data):
    if data == 'kospi':
        return 'Y'
    elif data == 'kosdaq':
        return 'K'
    elif data == 'konex':
        return 'N'
    elif data == 'others':
        return 'E'

    return data # error

def get_disc_rm(data):
    if data == '01':
        return '정' # 제출후 정정신고가 있다
    elif data == '02':
        return '철' # 제출후 철회함
    elif data == '03':
        return '연' # 연결부분을 포함
    elif data == '04':
        return '유' # 유가증권시장본부 소관
    elif data == '05':
        return '코' # 코스닥시장본부 소관
    elif data == '06':
        return '금' # 사용안함
    elif data == '07':
        return '채' # 채권상장법인 공시사항
    elif data == '08':
        return '공' # 공정거래위원회 소관
    elif data == '09':
        return '넥' # 코넥스시장 소관
    else:
        return ' '

    return data

def is_new_disc(last_disc, new_disc):
    if last_disc is None:
        return True

    if last_disc.rcept_dt < new_disc['rcept_dt']:
        return True

    # open api를 사용하면 시간 정보가 없음
    #print('reg_time', last_disc.reg_time,  new_disc['reg_time'])
    """
    if last_disc.reg_time < new_disc['reg_time']:
        return True
    """

    if last_disc.rcept_no != new_disc['rcept_no']:
        return True
    return False

