import re
import math
import numpy as np
import abc
import sys
from datetime import datetime
from utils.datetime import to_yyyymmdd
from utils.parser import get_value, elim_tag

class AbstractParserFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_parser(self):
        pass

    @classmethod
    def get_factory(self, cntry):
        if cntry == 'kr':
            return ConcreteParserKrFactory()
        if cntry == 'us':
            return ConcreteParserUsFactory()
        return None

class ConcreteParserKrFactory(AbstractParserFactory):
    def create_parser(self):
        return ConcreteProductParserKr()

class ConcreteParserUsFactory(AbstractParserFactory):
    def create_parser(self):
        return ConcreteProductParserUs()

class AbstractProductParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def regex_parents(self):
        pass

#AbstractProductA
class AbstractProductParser(AbstractProductParser):
    @abc.abstractmethod
    def regex_parents(self):
        pass

    @abc.abstractmethod
    def regex_exchange(self, url):
        pass

    @abc.abstractmethod
    def regex_stocks(self, html):
        pass

    @abc.abstractmethod
    def regex_stock_detail(self, html):
        pass

    @abc.abstractmethod
    def regex_ohlcv(self, code, html):
        pass

    @abc.abstractmethod
    def regex_company(self, html, close):
        pass

    def regex_compile(self, regex, text):
        p = re.compile(regex)
        m = p.findall(text)
        return m

#ConcreteProductA
class ConcreteProductParserKr(AbstractProductParser):
    def regex_parents(self, html):
        l_tag = 'style="padding-left:10px;">'
        s_idx = html.find(l_tag)
        text = html[s_idx:s_idx+100]
        name = get_value(text, l_tag, '</td>')

        regex = '<a href="/item/main.nhn.code=(.*)">(.*)</a>'
        return name, dict(self.regex_compile(regex, html))

    def regex_group_no(self, html):
        regex = '/sise/sise_group_detail.nhn.type=group&no=([0-9]+)'
        return self.regex_compile(regex, html)

    def regex_exchange(self, url):
        m = get_value(url, 'sosok=', '&')

        exchange = 'KOSPI' if m == '0' else 'KOSDAQ'
        return exchange

    def regex_stocks(self, html):
        regex ='<td><a href="/item/main.nhn.code=([a-zA-Z0-9]+).*>(.*)</a></td>'
        return self.regex_compile(regex, html)

    def regex_stock_detail(self, html):
        detail = {}

        s_idx = html.find('<th scope="row">시가총액</th>')
        text = html[s_idx:s_idx+300]
        l_tag = '<em id="_market_sum">'
        capital = get_value(text, l_tag, '</em>')

        idx = capital.find('조')
        if idx > 0:
            capital = capital[0:idx]+capital[idx+1: capital.__len__()].zfill(4)

        s_idx = html.find('업종명')
        text = html[s_idx:s_idx+100]
        industry = get_value(text, '">', '</a>')

        if not industry:
            industry = 'N/A'

        s_idx = html.find('<div class="h_company">')
        html = html[s_idx:]
        s_idx = html.find('<em class="e_summary">')
        html = html[s_idx:]

        l_tag = '<span class="blind">'
        s_idx = html.find(l_tag)
        text = html[s_idx:s_idx+100]
        aimed = get_value(text, l_tag, '개요</span>')

        detail['sector']   = industry
        detail['industry'] = industry
        detail['aimed']    = aimed if aimed else 'N/A'
        detail['capital']  = int(capital.replace(',',''))

        return detail

    def regex_ohlcv(self, code, html):
        ohlcvs = list()

        for line in html.split('\n'):
            line = line.strip().replace('"','')
            if not line.startswith('<item data='):
                continue

            value = line.replace('<item data=','').replace('/>','').split('|')
            date   = value[0]
            open   = int(value[1])
            high   = int(value[2])
            low    = int(value[3])
            close  = int(value[4])
            volume = int(value[5])
            log    = math.log(close)

            if not date or not close:
                continue

            date = datetime.strptime(date, '%Y%m%d')

            ohlcvs.append({'code'  :code,
                           'date'  :date,
                           'close' :int(close),
                           'open'  :int(open),
                           'high'  :int(high),
                           'low'   :int(low),
                           'volume':int(volume),
                           'log'   :log})
        return ohlcvs

    def regex_company(self, html):
        name = get_value(html, 'window.location.reload();">', '</a>')
        invt_opinion = ''
        tgt_price = ''
        per = ''
        eps = ''
        cns_per = ''
        cns_eps = ''
        dividend = ''
        per_field = ''

        text = get_value(html, '<table summary="투자의견 정보"', '</table>')
        trs = text.split('<tr>')
        for tr in trs:
            if tr.find('목표주가') < 0:
                continue
            td = get_value(tr, '<td', '</td>')
            spans = td.split('<span')

            invt_opinion = elim_tag(spans[1]).replace(' ','')
            tgt_price = get_value(spans[2], '<em>', '</em>')
            break

        text = get_value(html, 'class="per_table">', '</table>')
        trs = text.split('<tr')
        emids = trs[1].split('emid')
        if len(emids) > 1:
            per = get_value(emids[1], '"_per">', '</em>')

        if len(emids) > 2:
            eps = get_value(emids[2], '"_eps">', '</em>')

        emids = trs[2].split('emid')
        if len(emids) > 1:
            cns_per = get_value(emids[1], '"_cns_per">', '</em>')
        if len(emids) > 2:
            cns_eps = get_value(emids[2], '"_cns_eps">', '</em>')

        if len(trs) > 4:
            emids = trs[4].split('emid')
            if len(emids) > 1:
                dividend = get_value(emids[1], '"_dvr">', '</em>')

        text = get_value(html, '<table summary="동일업종 PER 정보">','</table>')
        tds = text.split('<td')
        per_field = get_value(tds[1], '<em>', '</em>')

        tgt_price = 'N/A' if not tgt_price else tgt_price + '원'
        per       = 'N/A' if not per       else per + '배'
        eps       = 'N/A' if not eps       else eps + '원'
        cns_per   = 'N/A' if not cns_per   else cns_per + '배'
        cns_eps   = 'N/A' if not cns_eps   else cns_eps + '원'
        dividend  = 'N/A' if not dividend  else dividend + '%'
        per_field = 'N/A' if not per_field else per_field + '배'

        return {'name':name,                    #종목명
                #'close':close,                  #현재가
                'target_price':tgt_price,    #목표주가(원)
                'cns_eps':cns_eps,              #추정EPS
                #'cns_per':cns_per,              #추정PER
                'per_field':per_field,          #동일업종 PER
                'per':per,                      #PER              
                'dividend':dividend,            #현금배당수익률
                'invt_opinion':invt_opinion,    #투자의견
                }

#ConcreteProductB
class ConcreteProductParserUs(AbstractProductParser):
    exchange = ''
    def regex_parents(self):
        pass

    def regex_stock_detail(self, html):
        pass

    def regex_exchange(self, url):
        exch = get_value(url, '&f=', '&')

        self.exchange = 'NASDAQ' if exch == 'exch_nasd' else 'NYSE'

    def regex_stock(self, tr):
        tds = tr.split('<td')
        capital = elim_tag(tds[7])

        multi = 1
        if capital.find('B') > 0: multi = 1000000000
        if capital.find('M') > 0: multi = 1000000
        if capital == '-': capital = '0'
        capital = float(capital.replace('B','').replace('M','')) * multi
        return {
            'no'       : elim_tag(tds[1]),
            'code'     : elim_tag(tds[2]),
            'name'     : elim_tag(tds[3]),
            'dname'    : elim_tag(tds[3]),
            'label'    : elim_tag(tds[2]) + ' ' + elim_tag(tds[3]),
            'exchange' : self.exchange,
            'sector'   : elim_tag(tds[4]),
            'industry' : elim_tag(tds[5]),
            'country'  : elim_tag(tds[6]),
            'capital'  : capital / 100000000,
            'pe'       : elim_tag(tds[8]),
            'price'    : elim_tag(tds[9]),
            'change'   : elim_tag(tds[10]),
            'volume'   : elim_tag(tds[11]),
            'parent'   : 'N/A',
            'aimed'    : 'N/A',
            'avg_v50'  : '0',
        }
        # code, name, label, exchange, aimed, industry, capital, parent, avg_v50

    def regex_stocks(self, html):
        s_idx = html.find('<table width="100%" cellpadding="3" cellspacing="1" border="0" bgcolor="#d3d3d3">')
        e_idx = html[s_idx:].find('</table>') + s_idx
        trs = html[s_idx:e_idx].split('<tr')

        stocks = [self.regex_stock(tr) for tr in trs if tr.find('screener-link') >= 0]
        # finviz.com 에서는 1건이 나온다는건 마지막 이라는 뜻이다.
        if stocks.__len__() == 1:
            return None
        return stocks

    def regex_ohlcv(self, code, html):
        html = html.replace('[','').replace('{','')

        date     = get_value(html,'timestamp', ']').split(',')
        open     = get_value(html,'open', ']').split(',')
        high     = get_value(html,'high', ']').split(',')
        low      = get_value(html,'low', ']').split(',')
        close    = get_value(html,'close', ']').split(',')
        volume   = get_value(html,'volume', ']').split(',')
        adjclose = get_value(html,'adjcloseadjclose', ']').split(',')

        ohlcvs = [
            {'code'  :code,
             'date'  :to_yyyymmdd(datetime.fromtimestamp(int(date[i]))),
             'open'  :float(open[i]),
             'high'  :float(high[i]),
             'low'   :float(low[i]),
             'close' :float(adjclose[i]),
             'volume':float(volume[i]),
             'log'   :math.log(float(adjclose[i]))
            } for i in range(len(date)) if adjclose[i].replace('null','0') > '0'
        ]
        return ohlcvs

    def regex_token(self, html):
        return token

    def regex_company(self, html):
        """
        html = html[html.find('snapshot-table2'):]
        s_idx = html.find('-STOK=')
        e_idx = html.find('-STOK=')

        return {'name':name,                    #종목명
                #'close':close,                  #현재가
                'target_price':tgt_price,    #목표주가(원)
                'cns_eps':cns_eps,              #추정EPS
                #'cns_per':cns_per,              #추정PER
                'per_field':per_field,          #동일업종 PER
                'per':per,                      #PER              
                'dividend':dividend,            #현금배당수익률
                'invt_opinion':invt_opinion,    #투자의견
                }
        """


if __name__ == '__main__':
    pass

