from datetime import datetime
import numpy as np

F = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ',
     'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ',
     'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];
S = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ',
     'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ',
     'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'];
T = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ',
     'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ',
     'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ',
     'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];

def getDisassembled(value):
    fst = ''

    if not value:
        return ''
    for i in range(0, value.__len__()):
        uni = ord(value[i])

        if uni < 44032 or uni > 55203:
            fst += value[i]
            continue

        uni = uni - 44032
        tn = int(uni % 28); # 종성
        sn = int(((uni - tn) / 28 ) % 21); # 중성
        fn = int((((uni - tn) / 28 ) - sn ) / 21); # 초성

        fst += F[fn] + S[sn] + T[tn]
    return fst

def trim(value):
    if not value: return value
    return value.replace('  ','').replace('\n','').replace('\r','')

def write_log(*logs):
    fileName = 'log/%s.log' % (datetime.today().strftime('%Y%m%d'))
    f = open(fileName, 'a+')
    f.write('[%s]' % (datetime.today().strftime('%H:%M:%S')))
    for log in logs:
        f.write(str(log) + ' ')
    f.write('\n')
    f.close()


def date_to_str(date, formatter):
    if not date:
        return ''
    return date.strftime(formatter)

def str_to_date(date, formatter):
    if not date:
        return ''
    return datetime.strptime(date, formatter).date()
