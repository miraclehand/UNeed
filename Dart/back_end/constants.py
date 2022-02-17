############ URL ############
#DART
DART_KEY = '6098e3b50b714eb7db7486633471a55589dfd52e'
DART_URL = 'https://opendart.fss.or.kr/api/{}?crtfc_key=' + DART_KEY

DART_LIST_URL = DART_URL.format('list.json') + '&page_count={}'
DART_DOC_URL  = DART_URL.format('document.xml') + '&rcept_no={}'
DART_FNLTT_SGL_URL= DART_URL.format('fnlttSinglAcnt.json') + '&corp_code={}&bsns_year={}&reprt_code={}'
DART_FNLTT_MUL_URL= DART_URL.format('fnlttMultiAcnt.json') + '&corp_code={}&bsns_year={}&reprt_code={}'
DART_FRIC_DECSN_URL = DART_URL.format('fricDecsn.json') + '&corp_code={}&bgn_de={}&end_de={}'
DART_PIFRIC_DECSN_URL = DART_URL.format('pifricDecsn.json') + '&corp_code={}&bgn_de={}&end_de={}'
DART_PIIC_DECSN_URL = DART_URL.format('piicDecsn.json') + '&corp_code={}&bgn_de={}&end_de={}'

REQUESTS_HEADERS = {
    "Accept-Language":"en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
    "Connection":"keep-alive",
    "User-Agent":"Mozilla/5.0"
}

#BroadCast
BCAST_URL = 'https://exp.host/--/api/v2/push/send'
BCAST_HDR = {
    'Accept': 'application/json',
    'Accept-encoding': 'gzip, deflate',
    'Content-Type': 'application/json',
}

