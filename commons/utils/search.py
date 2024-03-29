
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

