import sys
sys.path.append('../../')
import time
import requests
from task.reportparser import report_1, report_2
from db.models import Disc
from commons.utils.parser import get_ba_cell, get_rows_cell, elim_tag, get_key_value, with_commas, to_number
from task.parser import valid_value, correct_value, get_ratio, get_sales_yoy

discs = Disc.objects.raw({'rcept_dt':{'$gte':'20160101','$lte':'20211231'}}).order_by([('rcept_dt',1)])
f = 0
for disc in discs:
    #if disc.content.find('배정비율:') < 0:
    #    continue
    if disc.report_nm.find('상증자결정') < 0:
        continue
    if disc.report_nm.find('무') < 0:
        continue
    if disc.report_nm.find('첨부정정') >= 0:
        continue
    f = f + 1
    print(disc.rcept_dt, disc.report_nm, disc.url)
    html = requests.get(disc.url).text
    disc.content = report_2(html)
    if not disc.content:
        disc.content = disc.report_nm
    disc.save()
    print(disc.content)
    time.sleep(0.8)


