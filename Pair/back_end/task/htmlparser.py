import re
import math
import numpy as np
import abc
from datetime import datetime

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

    def get_value(self, text, l_tag, r_tag):
        if not text:
            return None, None,

        s_idx = text.find(l_tag) + l_tag.__len__()
        e_idx = text[s_idx:].find(r_tag) + s_idx
        n_idx = e_idx + r_tag.__len__()

        if s_idx < 0 or e_idx < 0:
            return None, None

        value = ''.join(text[s_idx:e_idx].split()).replace(',','')

        if value.__len__() > 100:
            value = None

        if value == 'N/A':
            value = None

        return text[n_idx:], value

#ConcreteProductA
class ConcreteProductParserKr(AbstractProductParser):
    def regex_parents(self, html):
        l_tag = 'style="padding-left:10px;">'
        s_idx = html.find(l_tag)
        text = html[s_idx:s_idx+100]
        text, name = self.get_value(text, l_tag, '</td>')

        regex = '<a href="/item/main.nhn.code=(.*)">(.*)</a>'
        return name, dict(self.regex_compile(regex, html))

    def regex_group_no(self, html):
        regex = '/sise/sise_group_detail.nhn.type=group&no=([0-9]+)'
        return self.regex_compile(regex, html)

    def regex_exchange(self, url):
        text, m = self.get_value(url, 'sosok=', '&')

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
        text, capital = self.get_value(text, l_tag, '</em>')

        idx = capital.find('조')
        if idx > 0:
            capital = capital[0:idx]+capital[idx+1: capital.__len__()].zfill(4)

        s_idx = html.find('업종명')
        text = html[s_idx:s_idx+100]
        text, industry = self.get_value(text, '">', '</a>')

        s_idx = html.find('<div class="h_company">')
        html = html[s_idx:]
        s_idx = html.find('<em class="e_summary">')
        html = html[s_idx:]

        l_tag = '<span class="blind">'
        s_idx = html.find(l_tag)
        text = html[s_idx:s_idx+100]
        text, aimed = self.get_value(text, l_tag, '개요</span>')

        detail['industry'] = industry
        detail['aimed']    = aimed
        detail['capital']  = int(capital)

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
        l_tag = 'window.location.reload();">'
        s_idx = html.find(l_tag)
        text = html[s_idx:s_idx+100]
        text, name = self.get_value(text, l_tag, '</a>')

        s_idx = html.find('<table summary="투자의견 정보" class="rwidth">')
        text = html[s_idx:s_idx+400]
        text, option1 = self.get_value(text, '<em>', '</em>')
        text, option2 = self.get_value(text, '', '</span>')

        if option1 and option2:
            invt_opinion = option1 + option2
        else:
            invt_opinion = 'N/A'

        text, tgt_price = self.get_value(text, '<em>', '</em>')
        s_idx = html.find('<table summary="PER/EPS 정보" class="per_table">')
        text = html[s_idx:s_idx+1000]
        text, per = self.get_value(text, '<em id="_per">', '</em>')

        text = html[s_idx:s_idx+3000]
        text, cns_per = self.get_value(text, '<em id="_cns_per">', '</em>')
        text, cns_eps = self.get_value(text, '<em id="_cns_eps">', '</em>')
        s_idx = html.find('<em id="_dvr">')
        text = html[s_idx:s_idx+100]
        text, dividend = self.get_value(text, '<em id="_dvr">',  '</em>')

        s_idx = html.find('<table summary="동일업종 PER 정보">')
        text = html[s_idx:s_idx+500]
        text, per_field = self.get_value(text, '<em>', '</em>')

        if cns_eps is None or cns_eps.find('N/A') > 0: cns_eps = ''
        if per     is None or per.find('N/A') > 0: per = ''

        try:
            cns_eps   = format(int(cns_eps), ',')+'원'
        except:
            cns_eps   = 'N/A'

        try:
            tgt_price = format(int(tgt_price), ',')+'원'
        except:
            tgt_price = 'N/A'

        per_field = 'N/A' if not per_field else per_field + '배'
        per       = 'N/A' if not per else per + '배'
        dividend  = 'N/A' if not dividend else dividend + '%'

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
    def regex_parents(self):
        pass

    def regex_exchange(self, url):
        text, m = self.get_value(url, 'exchange=', '&')

        exchange = m
        return exchange

    def regex_stocks(self, html):
        exchange = html[0:6]
        html = html[6:]

        #regex = '<a href="https://www.nasdaq.com/symbol/([ a-zA-Z0-9]+)">'
        regex = '<a href="/symbol/([ a-zA-Z0-9]+)">'
        symbols = [symbol.strip() for symbol in self.regex_compile(regex, html)]

        regex = '<td style="width:105px">(.*)</td>'
        subsectors = self.regex_compile(regex, html)

        names = list()
        if exchange == 'NASDAQ':
            s_idx = html.find('<!-- begin data rows -->')
            e_idx = html[s_idx:].find('</table>')
            text = html[s_idx:s_idx+e_idx]

            while(1):
                if not text:
                    break
                s_idx, e_idx = text.find('<tr>'), text.find('</tr>') + 10
                if s_idx < 0 or e_idx < 0:
                    break

                tr_text = text[s_idx:e_idx]
                text = text[e_idx:]

                if tr_text.find('target="_blank">') > 0:
                    tr_text, name = self.get_value(tr_text, 'target="_blank">','</a>')
                else:
                    tr_text, name = self.get_value(tr_text, '<td>','</td>')

                if name:
                    names.append(name)
        else:   #NYSE
            s_idx = html.find('<!-- begin data rows -->')
            e_idx = html[s_idx:].find('</table>')
            text = html[s_idx:s_idx+e_idx]

            while(1):
                idx = text.find('<tr>')
                if idx < 0:
                    break
                text, name = self.get_value(text[idx:], '<td>','</td>')

                if name:
                    names.append(name)
        return np.stack([symbols, names, subsectors],axis=1)

    def regex_stock_detail(self, html):
        detail = {}

        s_idx = html.find('<span id="qbar_sectorLabel">')
        text = html[s_idx:s_idx+300]

        #regex = '<a href="https://www.nasdaq.com/screening/.*">(.*)</a>'
        regex = '<a href="/screening/.*">(.*)</a>'
        industry = self.regex_compile(regex, text)
        if industry.__len__() == 0:
            industry = 'N/A'
        else:
            industry = industry[0]

        s_idx = html.find('Daily Volume')
        text = html[s_idx:s_idx+200]
        text, avg_v50 = self.get_value(text,'<div class="table-cell">','</div>')

        s_idx = html.find('Market Cap')
        text = html[s_idx:s_idx+200]

        text, capital = self.get_value(text,'<div class="table-cell">','</div>')

        detail['avg_v50'] = avg_v50
        detail['industry'] = industry
        detail['capital']  = capital / 100000000    # 단위 억달러

        return detail

    def regex_ohlcv(self, code, html):
        ohlcvs = list()

        lines = html.split('<TR>')
        for line in lines:
            text = line
            text, date   = self.get_value(text, 'DrillDownDate>', '</TD>')
            text, close  = self.get_value(text, 'DrillDownData>', '</TD>')
            text, volume = self.get_value(text, 'DrillDownData>', '</TD>')
            if not date:
                continue

            close = float(close)
            date = datetime.strptime(date, '%m/%d/%Y')
            open = close    # TODO
            high = close    # TODO
            low  = close    # TODO
            log  = math.log(close)

            ohlcvs.append({'code'  :code,
                           'date'  :date,
                           'close' :close,
                           'open'  :open,
                           'high'  :high,
                           'low'   :low,
                           'volume':volume,
                           'log'   :log})

        return ohlcvs

    def regex_token(self, html):
        return token

    def regex_company(self, html, close):
        s_idx = html.find('-STOK=')
        e_idx = html.find('-STOK=')
        token = html[s_idx:e_idx]

        #'FREQ=1-STOK=A6gWAFGFO/zJlQfzIKfIrgE+N7f2tyEOYG0+GvELTnEbpEoASgjTke5qRSDfEYLo";'

        pass

if __name__ == '__main__':
    pass

