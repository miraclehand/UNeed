from commons.utils.parser import get_ba_cell, get_rows_cell, elim_tag, get_key_value, with_commas, to_number
from task.parser import valid_value, correct_value, get_ratio, get_sales_yoy
import json

# 단일판매 공급계약체결
def report_1(html):
    content = ''

    cont = get_ba_cell(html, '공급계약내용')
    if cont == '-':
        cont = get_ba_cell(html, '체결계약명')

    sales_counter = get_ba_cell(html, '계약상대')
    sales_ratio   = get_ba_cell(html, '매출액대비')
    sales_bgn_de  = get_ba_cell(html, '시작일')
    sales_end_de  = get_ba_cell(html, '종료일')
    cont_amount   = get_ba_cell(html, '계약금액')
    last_sales_amount = get_ba_cell(html, '최근매출액')
    
    sales_ratio = sales_ratio.replace('%', '').replace(']','').replace(',','')

    print('['+sales_bgn_de+']', '['+sales_end_de+']', '['+sales_ratio+']')
    try:
        bgn_de1, bgn_de2 = correct_value(sales_bgn_de)
        end_de1, end_de2 = correct_value(sales_end_de)
        ratio1,  ratio2  = correct_value(sales_ratio)

        ratio1 = get_ratio(ratio1)
        ratio2 = get_ratio(ratio2)

        sales_yoy1 = get_sales_yoy(bgn_de1, end_de1, ratio1)

        if not bgn_de2 and not end_de2 and not ratio2:
            sales_yoy2 = ''
        else:
            bgn   = bgn_de2 if bgn_de2 else bgn_de1
            end   = end_de2 if end_de2 else end_de1
            ratio = ratio2  if ratio2  else ratio1
            sales_yoy2 = get_sales_yoy(bgn, end, ratio)

        sales_yoy = f'{sales_yoy1}' if sales_yoy1 else ''
        sales_yoy = f'{sales_yoy}->{sales_yoy2}' if sales_yoy2 else sales_yoy

    except Exception as ex:
        print('except yoy', ex)
        sales_yoy = 'NaN'

    content = content+' * 계약내용:' + cont + '\n'
    content = content+' * 계약상대:' + sales_counter + '\n'
    content = content+' * 계약금액:' + cont_amount + '\n'
    content = content+' * 최근매출:' + last_sales_amount + '\n'
    content = content+' * 매출대비:' + sales_ratio + '\n'
    content = content+' * 연환산:'   + sales_yoy +'\n'
    content = content+' * 계약시작:' + sales_bgn_de + '\n'
    content = content+' * 계약종료:' + sales_end_de + '\n'

    return content 

#유상증자랑 무상증자가 한페이지에 나와있는경우 있음
def report_2(html):
    content = ''

    idx = html.find('>유상증자')
    if idx >= 0:
        s_idx = html[idx:].find('무상증자')
        if s_idx >= 0:
            s_idx = s_idx + idx
        else:
            s_idx = html.find('무상증자')
        html = html[s_idx:]

    value = get_ba_cell(html, '제출사유')
    if value.find('철회') >= 0:
        return ' * 결정철회내용:' + value + '\n'

    value = get_ba_cell(html, '결정 철회')
    if value != '-':
        return ' * 결정철회내용:' + value + '\n'

    base_date = get_ba_cell(html, '신주배정기준일')
    list_date = get_ba_cell(html, '신주의 상장 예정일')
    if list_date == '-':
        list_date = get_ba_cell(html, '신주권교부예정일')
    decn_date = get_ba_cell(html, '이사회결의일(결정일)')

    asgn_qty   = get_rows_cell(html, '신주의 종류와 수')
    before_qty = get_rows_cell(html, '증자전 발행주식총수')

    asgn_ratio = ''

    asgn_values = get_rows_cell(html, '1주당 신주배정')
    if not asgn_values:
        asgn_values = get_ba_cell(html, '1주당 신주배정')
        if asgn_values.find('-') >= 0:
            asgn_ratio = '-'
        else:
            asgn_ratio = f'{int(float(asgn_values) * 100)}%'
    else:
        for asgns in asgn_values.split(','):
            values = asgns.split(':')
            asgn_ratio = f'{asgn_ratio}, ' if asgn_ratio else asgn_ratio
            asgn_ratio = f'{asgn_ratio}{values[0]}:'
            try:
                if values[1] == '-':
                    asgn_ratio = f'{asgn_ratio}{values[1]}'
                else:
                    asgn_ratio = f'{asgn_ratio}{int(float(values[1]) * 100)}%'
            except Exception as ex:
                print('except 무상', ex)
                print(asgn_values)

    dict_asgn_qty   = get_key_value(asgn_qty)
    dict_before_qty = get_key_value(before_qty)


    dict_after_qty = {}
    for key in dict_asgn_qty.keys():
        if key in dict_before_qty.keys():
            dict_after_qty[key] = with_commas(to_number(dict_asgn_qty[key]) + to_number(dict_before_qty[key]))
        else:
            dict_after_qty[key] = dict_asgn_qty[key]

    for key in dict_before_qty.keys():
        if key not in dict_asgn_qty.keys():
            dict_after_qty[key] = dict_before_qty[key]

    after_qty = str(dict_after_qty).replace('{','').replace('}','').replace('\'','')
    
    content = content+' * 무상증자 배정비율:'    + asgn_ratio + '\n'
    content = content+' * 무상증자 전 수량:'     + before_qty + '\n'
    content = content+' * 무상증자 배정 수량:'   + asgn_qty   + '\n'
    content = content+' * 무상증자 후 수량:'     + after_qty  + '\n'
    content = content+' * 신주배정기준일:'       + base_date  + '\n'
    content = content+' * 신주의 상장 예정일:'   + list_date  + '\n'
    content = content+' * 이사회결의일(결정일):' + decn_date  + '\n'

    return content

#보통주와 기타주를 합쳐서리턴
def concat_oe(a, b):
    if type(a) is not str:
        a = str(a)
    if type(b) is not str:
        b = str(b)

    if a in ('-', '0', None): a = ''
    if b in ('-', '0', None): b = ''

    if not a and not b:
        return ''
    if a: a = a + '(보통주)'
    if b: b = b + '(기타주)'

    if a and b:
        return a + '\n' + b
    if a and not b:
        return a
    if not a and b:
        return b

#무상증자결정 open api 값으로 데이터 입력
def report_2_new(html):
    data = json.loads(html)
    for d in data['list']:
        nstk_asstd  = d['nstk_asstd']    #신주배정기준일
        bddd        = d['bddd']          #이사회결의일(결정일)
        nstk_lstprd = d['nstk_lstprd']   #신주의상장예저일

        bfic_tisstk_ostk   = d['bfic_tisstk_ostk']   #증자전 발행주식(보통주)
        bfic_tisstk_estk   = d['bfic_tisstk_estk']   #증자전 발행주식(기타주)
        nstk_ostk_cnt      = d['nstk_ostk_cnt']      #신주의 종류와 수(보통주)
        nstk_estk_cnt      = d['nstk_estk_cnt']      #신주의 종류와 수(기타주)
        nstk_ascnt_ps_ostk = d['nstk_ascnt_ps_ostk'] #주당 신주배정주식(보통주)
        nstk_ascnt_ps_estk = d['nstk_ascnt_ps_estk'] #주당 신주배정주식(기타주)

        if nstk_ascnt_ps_ostk != '-':
            nstk_ascnt_ps_ostk = str(to_number(nstk_ascnt_ps_ostk) * 100) + '%'
        if nstk_ascnt_ps_estk != '-':
            nstk_ascnt_ps_estk = str(to_number(nstk_ascnt_ps_estk) * 100) + '%'

        afic_tisstk_ostk = to_number(bfic_tisstk_ostk) +to_number(nstk_ostk_cnt)
        afic_tisstk_estk = to_number(bfic_tisstk_estk) +to_number(nstk_estk_cnt)

        afic_tisstk_ostk = f'{afic_tisstk_ostk:,}'
        afic_tisstk_estk = f'{afic_tisstk_estk:,}'

        bfic_tisstk   = concat_oe(bfic_tisstk_ostk, bfic_tisstk_estk)
        nstk_cnt      = concat_oe(nstk_ostk_cnt, nstk_estk_cnt)
        nstk_ascnt_ps = concat_oe(nstk_ascnt_ps_ostk, nstk_ascnt_ps_estk)
        afic_tisstk   = concat_oe(afic_tisstk_ostk, afic_tisstk_estk)

        content = ''
        content = content+' * 무상증자 배정비율:'    + nstk_ascnt_ps + '\n'
        content = content+' * 무상증자 전 수량:'     + bfic_tisstk   + '\n'
        content = content+' * 무상증자 배정 수량:'   + nstk_cnt      + '\n'
        content = content+' * 무상증자 후 수량:'     + afic_tisstk   + '\n'
        content = content+' * 신주배정기준일:'       + nstk_asstd    + '\n'
        content = content+' * 신주의 상장 예정일:'   + nstk_lstprd   + '\n'
        content = content+' * 이사회결의일(결정일):' + bddd          + '\n'
    return content

#유무상증자결정
def report_3(html):
    data = json.loads(html)
    for d in data['list']:
        #유상증자
        piic_ic_mthn= d['piic_ic_mthn']       #유상증자(증자방식)

        #무상증자
        piic_ic_mthn= d['piic_ic_mthn']       #유상증자(증자방식)
        nstk_asstd  = d['fric_nstk_asstd']    #신주배정기준일
        bddd        = d['fric_bddd']          #이사회결의일(결정일)
        nstk_lstprd = d['fric_nstk_lstprd']   #신주의상장예저일

        bfic_tisstk_ostk   = d['fric_bfic_tisstk_ostk']   #증자전 발행주식(보통주)
        bfic_tisstk_estk   = d['fric_bfic_tisstk_estk']   #증자전 발행주식(기타주)
        nstk_ostk_cnt      = d['fric_nstk_ostk_cnt']      #신주의 종류와 수(보통주)
        nstk_estk_cnt      = d['fric_nstk_estk_cnt']      #신주의 종류와 수(기타주)
        nstk_ascnt_ps_ostk = d['fric_nstk_ascnt_ps_ostk'] #주당 신주배정주식(보통주)
        nstk_ascnt_ps_estk = d['fric_nstk_ascnt_ps_estk'] #주당 신주배정주식(기타주)

        if nstk_ascnt_ps_ostk != '-':
            nstk_ascnt_ps_ostk = str(to_number(nstk_ascnt_ps_ostk) * 100) + '%'
        if nstk_ascnt_ps_estk != '-':
            nstk_ascnt_ps_estk = str(to_number(nstk_ascnt_ps_estk) * 100) + '%'

        afic_tisstk_ostk = to_number(bfic_tisstk_ostk) +to_number(nstk_ostk_cnt)
        afic_tisstk_estk = to_number(bfic_tisstk_estk) +to_number(nstk_estk_cnt)

        afic_tisstk_ostk = f'{afic_tisstk_ostk:,}'
        afic_tisstk_estk = f'{afic_tisstk_estk:,}'

        bfic_tisstk   = concat_oe(bfic_tisstk_ostk, bfic_tisstk_estk)
        nstk_cnt      = concat_oe(nstk_ostk_cnt, nstk_estk_cnt)
        nstk_ascnt_ps = concat_oe(nstk_ascnt_ps_ostk, nstk_ascnt_ps_estk)
        afic_tisstk   = concat_oe(afic_tisstk_ostk, afic_tisstk_estk)

        content = ''
        content = content+' * 유상증자 증자방식:'    + piic_ic_mthn  + '\n'
        content = content+' * 무상증자 배정비율:'    + nstk_ascnt_ps + '\n'
        content = content+' * 무상증자 전 수량:'     + bfic_tisstk   + '\n'
        content = content+' * 무상증자 배정 수량:'   + nstk_cnt      + '\n'
        content = content+' * 무상증자 후 수량:'     + afic_tisstk   + '\n'
        content = content+' * 신주배정기준일:'       + nstk_asstd    + '\n'
        content = content+' * 신주의 상장 예정일:'   + nstk_lstprd   + '\n'
        content = content+' * 이사회결의일(결정일):' + bddd          + '\n'
    return content

