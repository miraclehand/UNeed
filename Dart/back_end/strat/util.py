from task.parser import get_value
from commons.utils.parser import find_number
from commons.utils.datetime import str_to_datetime, datetime_to_str

def get_max_value(df):
    max_date  = df.idxmax()
    max_value = df[max_date]
    return datetime_to_str(max_date,'%Y/%m/%d'), max_value

def get_prrt(base_close, close):
    if base_close == 0:
        return 0
    return round((close - base_close) / base_close * 100,2)

def get_d_prrt(d_df, close):
    if d_df.__len__() <= 0 or close <= 0:
        return 0, 0
    d_close = int(d_df[-1:]['close'].values[0])
    d_rt    = round((d_close - close) / close * 100,2)
    return d_close, d_rt

def get_losscut_date(df, close, loss):
    if df.__len__() <= 0 or close <= 0:
        return '-'

    losscut = close - (close * loss / 100)
    series = df[(0 < df) & (df <= losscut)].head(1)
    if series.empty:
        return '-'
    return datetime_to_str(series.index[0],'%Y/%m/%d')

def get_content_value(content, key):
    s_idx = content.find(key)

    if s_idx < 0:
        return '-'
    s_idx = s_idx + key.__len__()
    e_idx = content[s_idx:].find('\n')
    if e_idx < 0:
        e_idx = content.__len__()
    else:
        e_idx = e_idx + s_idx
    return content[s_idx:e_idx]

def extract_key_value(value, key):
    s_idx = value.find(key)
    if s_idx < 0:
        value, e_idx = find_number(value)
        return value
    value, e_idx = find_number(value[s_idx:])
    return value

def get_chk_adj(df, prrt):
    dates = df[(df < -prrt) | (df > prrt)].index
    return [datetime_to_str(date,'%Y/%m/%d') for date in dates]

def get_bigo_adj(df):
    date1 = str_to_datetime('2015/06/14', '%Y/%m/%d').date()
    date2 = str_to_datetime('2015/06/15', '%Y/%m/%d').date()

    adj1 = get_chk_adj(df[:date1], 15+1)  #2015/06/14일까지는 변동폭 15%
    adj2 = get_chk_adj(df[date2:], 30+1)  #2015/06/15일부터는 변동폭 30%

    adj = adj1 + adj2
    if not adj:
        return '-'

    adj = str(adj).replace("'",'').replace('[','').replace(']','')

    return f'{adj}일에 수정주가가 반영되지 않았습니다.'

def get_reprt_name(reprt_code):
    if reprt_code == '11013': # 1분기보고서
        return '1분기'
    if reprt_code == '11012': # 반기보고서
        return '2분기'
    if reprt_code == '11014': # 3분기보고서
        return '3분기'
    if reprt_code == '11011': # 사업보고서
        return '4분기'
    return ''
