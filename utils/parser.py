# beautifulsoap 를 쓰면 속도가 너무 느리다.

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
def elim_lr_tag(text, l_tag, a_tag, r_tag):
    if not text:
        return ''

    l_idx = find_l_idx(text, l_tag) - l_tag.__len__()
    a_idx = text[l_idx:].find(a_tag) + l_idx + a_tag.__len__()
    r_idx = text[a_idx:].find(r_tag) + a_idx + r_tag.__len__()

    if l_idx < 0 or a_idx < 0 or r_idx < 0:
        return text
    if l_idx == a_idx == r_idx:
        return text
    a_len = a_tag.__len__()
    l_len = text[l_idx:].find(r_tag)
    new_text = text[:l_idx] + ' ' \
             + text[l_idx + l_len + 1: a_idx - a_len] + ' '  \
             + text[r_idx:]
    return elim_lr_tag(new_text, l_tag, a_tag, r_tag)

# left, anchor, right
def elim_tag(text):
    l_tag, a_tag, r_tag = '<', '/>', '>'
    if not text:
        return None
    text = del_white_space(text)
    new_text = elim_lr_tag(text, l_tag, a_tag, r_tag)
    new_text = elim_ltrim(new_text, l_tag, a_tag, r_tag)
    new_text = elim_rtrim(new_text, l_tag, a_tag, r_tag)
    return new_text.strip()

def get_value(text, l_tag, r_tag):
    if not text:
        return None

    s_idx = text.find(l_tag) + l_tag.__len__()
    e_idx = text[s_idx:].find(r_tag) + s_idx
    n_idx = e_idx + r_tag.__len__()

    if s_idx < 0 or e_idx < 0:
        return None

    value = ''.join(text[s_idx:e_idx].split())

    if value == 'N/A':
        value = None

    return value

