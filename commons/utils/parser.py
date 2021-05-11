# beautifulsoap 를 쓰면 속도가 너무 느리다.

def exists_value(text):
    e_idx = text.lower().find('</tr>')
    idx = text[:e_idx].lower().find('<td')
    if idx < 0:
        return False
    return True

def search_key(text, key):
    pos = 0
    while True:
        idx = text[pos:].find(key[0])
        if idx < 0:
            return idx

        pos = pos + idx
        if compare_key(text[pos:], key):
            if exists_value(text[pos:]):
                return pos
        pos = pos + 1
    return 0

def compare_key(text, key):
    key = key.strip()
    if key.__len__() < 1:
        return True

    text = text.strip()
    if key[0] != text[0]:
        return False

    return compare_key(text[1:], key[1:])

def with_commas(value):
    return '{:,}'.format(value)

def get_rowspan(text):
    s_idx = text.lower().rfind('<td')

    key = 'rowspan='
    idx = text[s_idx:].lower().find(key)
    if idx < 0: return 1

    s_idx = s_idx + idx + key.__len__()
    e_idx = s_idx + 3   #rowspan="2"
    rowspan = int(text[s_idx:e_idx].replace("'",'').replace('"',''))
    return rowspan

    """
    idx = text[s_idx:].find('>')
    if idx < 0: return 1

    e_idx = idx + s_idx

    rowspan = int(text[s_idx:e_idx].replace("'",'').replace('"',''))
    return rowspan
    """

def is_number(value):
    if '0' <= value <= '9' or value in (',', '.'):
        return True
    else:
        return False
        
def to_number(data):
    value, n_idx = find_number(data)
    if not value:
        return None
    return int(value.strip().rstrip('.').replace(',','').replace('주',''))

def find_number(data):
    s_idx, e_idx = -1, data.__len__()
    for idx, d in enumerate(data):
        if is_number(d):
            s_idx = idx if s_idx == -1 else s_idx
        else:
            if s_idx == -1:
                continue
            e_idx = idx + 1
            break
    value = data[s_idx:e_idx].strip().strip(',')
    return value, e_idx

def get_key_value(data):
    idx = data.find(':')
    if idx == -1:
        return {}
    key = data[:idx]
    value, n_idx = find_number(data[idx:])
    if not value:
        return {}
    dict1 = {key:value}
    dict2 = get_key_value(data[idx+n_idx:])
    return dict(dict1, **dict2)

def get_table_row(text, key):
    text = text.replace('&nbsp;','')

    s_idx = search_key(text, key)

    if s_idx < 0: return '-'

    rowspan = get_rowspan(text[:s_idx])

    s_idx = s_idx + key.__len__()
    s_idx = text[s_idx:].lower().find('</td>') + s_idx

    idx = 0
    e_idx = 0
    for i in range(rowspan):
        idx = text[s_idx+idx:].lower().find('</tr>') + '</tr>'.__len__()
        e_idx = e_idx + idx
    e_idx = e_idx + s_idx

    #e_idx = text[s_idx:].lower().find('</tr>') + s_idx
    return text[s_idx:e_idx]

#before and after cell
def get_ba_cell(text, key):
    row = get_table_row(text, key)

    tds = row.lower().split('<td')

    if tds.__len__() < 3:
        value = elim_tag(row)
    else:
        value = elim_tag(tds[1]) + ' -> ' + elim_tag(tds[2])
    return value

def get_rows_cell(html, key):
    row = get_table_row(html, key)

    value = ''
    for tr in row.lower().split('</tr>'):
        if not tr: continue
        tds = tr.split('<td')
        if tds.__len__() < 3: continue

        cell1, cell2 = elim_tag(tds[1]), elim_tag(tds[2])
        if cell2 == '-': continue

        v = f'{cell1}:{cell2}'
        value = v if not value else f'{value}, {v}'
    return value

def del_white_space(value):
    if not value: return value
    return value.replace('  ','').replace('\n','').replace('\r','')

#tag가 미완성일때 왼쪽 테그제거 ex) '="font-size:10pt;">판매공급계약...'
def elim_ltrim(text, l_tag, a_tag, r_tag):
    if not text:
        return ''

    r_idx = text.find(r_tag)
    if r_idx < 0:
        return text

    return text[r_idx + 1:]

#tag가 미완성일때 오른쪽 테그제거 ex) '<"font-size:10pt;"'
def elim_rtrim(text, l_tag, a_tag, r_tag):
    if not text:
        return ''

    l_idx = text.find(l_tag)
    if l_idx < 0:
        return text

    return text[:l_idx]

def find_l_idx(text, l_tag):
    if text.find(l_tag) == -1:
        return 0;
    s_idx = text.find(l_tag) + l_tag.__len__()
    return s_idx + find_l_idx(text[s_idx:], l_tag)

#tag가 왼쪽 오른쪽 있는경우
def elim_lr_tag(text, l_tag, r_tag):
    if not text:
        return ''

    l_idx = text.find(l_tag)
    r_idx = text[l_idx:].find(r_tag) if l_idx > 0 else text.find(r_tag)

    r_pos = r_idx + r_tag.__len__()

    if l_idx < 0 and r_idx < 0:
        return text

    if l_idx < 0:
        return elim_lr_tag(text[r_pos:], l_tag, r_tag)

    if r_idx < 0:
        return elim_lr_tag(text[:l_idx], l_tag, r_tag)

    r_pos = l_idx + r_idx + r_tag.__len__()

    return elim_lr_tag(text[:l_idx] + ' ' + text[r_pos:], l_tag, r_tag)

    
    """
    #l_tag, a_tag, r_tag = '<', '/>', '>'
    #가장 깊이 있는 l_tag 찾기
    l_idx = find_l_idx(text, l_tag) - l_tag.__len__()
    a_idx = text.find(a_tag)
    r_idx = text[l_idx:].find(r_tag)

    new_text = ''
    if l_idx >= 0:
        new_text += 

    print(l_idx, a_idx, r_idx)
    if l_idx < 0 and a_idx < 0 and r_idx < 0:
        return text
    if l_idx == a_idx == r_idx:
        return text
    a_len = a_tag.__len__()
    l_len = text[l_idx:].find(r_tag)
    print(1, text[:l_idx])
    print(2, text[l_idx + l_len + 1: a_idx - a_len])
    print(3, text[r_idx:])
    new_text = text[:l_idx] + ' ' \
             + text[l_idx + l_len + 1: a_idx - a_len] + ' '  \
             + text[r_idx:]
    print(new_text)
    return elim_lr_tag2(new_text, l_tag, a_tag, r_tag)
    """

"""
#tag가 왼쪽 오른쪽 있는경우
def elim_lr_tag(text, l_tag, a_tag, r_tag):
    if not text:
        return ''

    #l_tag, a_tag, r_tag = '<', '/>', '>'
    l_idx = find_l_idx(text, l_tag) - l_tag.__len__()
    a_idx = text[l_idx:].find(a_tag) + l_idx + a_tag.__len__()
    r_idx = text[a_idx:].find(r_tag) + a_idx + r_tag.__len__()

    print(l_idx, a_idx, r_idx)
    if l_idx < 0 or a_idx < 0 or r_idx < 0:
        return text
    if l_idx == a_idx == r_idx:
        return text
    a_len = a_tag.__len__()
    l_len = text[l_idx:].find(r_tag)
    print(1, text[:l_idx])
    print(2, text[l_idx + l_len + 1: a_idx - a_len])
    print(3, text[r_idx:])
    new_text = text[:l_idx] + ' ' \
             + text[l_idx + l_len + 1: a_idx - a_len] + ' '  \
             + text[r_idx:]
    print(new_text)
    return elim_lr_tag(new_text, l_tag, a_tag, r_tag)
"""

# left, anchor, right
"""
def elim_tag(text):
    l_tag, a_tag, r_tag = '<', '/>', '>'
    if not text:
        return None
    text = del_white_space(text)
    new_text = elim_lr_tag(text, l_tag, a_tag, r_tag)
    new_text = elim_ltrim(new_text, l_tag, a_tag, r_tag)
    new_text = elim_rtrim(new_text, l_tag, a_tag, r_tag)
    return new_text.strip()
"""

def elim_tag(text):
    l_tag, r_tag = '<', '>'
    if not text:
        return None
    text = del_white_space(text)
    new_text = elim_lr_tag(text, l_tag, r_tag)
    return new_text.strip()

def get_value(text, l_tag, r_tag):
    if not text:
        return ''

    s_fnd = text.find(l_tag)
    s_idx = s_fnd + l_tag.__len__()

    e_fnd = text[s_idx:].find(r_tag)
    e_idx = e_fnd + s_idx

    n_idx = e_idx + r_tag.__len__()

    if s_fnd < 0 or e_fnd < 0:
        return ''

    value = ''.join(text[s_idx:e_idx].split())

    if value == 'N/A':
        value = ''

    return value

def test_elim_tag():
    tags = ['<a href="url">test url</a>',
            '<a href="url"><b>test url</b></a>',
            '<a href="url"><b>test url</b></a>',
            'href="url"><b>test url</b></a>',
            '<a href="url"><b>test url</b></a',
            '<b><br/>test url</b><br/>',
            'span>        test url<span',
    ]

    for tag in tags:
        if 'test url' != elim_tag(tag):
            print('error', tag)
    
if __name__ == '__main__':
    test_elim_tag()


