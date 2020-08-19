# classify
D_ALL = 9
D_PARENT = 1
D_INDUSTRY = 2
D_AIMED = 3
D_EXCHANGE = 4

# position
D_POS_LONG = '+'
D_POS_SHORT = '-'

# direction
D_NONE = -1
D_RISE =  1
D_DROP =  2

exclude_code = ['190620',   # KINDEX 단기통안채
                '157450',   # TIGER 단기통안채
                '196230',   # KBSTAR 단기통안채
                '153130',   # KODEX 단기채권
                '214980',   # KODEX 단기채권PLUS
]

general_industry = [
    ['디스플레이패널','디스플레이장비및부품','핸드셋','전자제품','전기제품'],
    ['IT서비스','소프트웨어'],
    ['자동차','자동차부품'],
    ['식품','식품과기본식료품소매'],
]
