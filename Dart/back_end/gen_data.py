import sys
import time
sys.path.append('../../')
from server import api
from job import post_disc_kr
from db.models import StdDisc, Disc
from task.htmlparser import get_doc_url
from datetime import datetime, timedelta
from commons.utils.datetime import str_to_datetime, datetime_to_str
   
def new_doc_url(begin, end):
    date1 = str_to_datetime(begin,'%Y%m%d')
    date2 = str_to_datetime(end,  '%Y%m%d')

    delta = date2 - date1
    for i in range(delta.days + 1):
        date = datetime_to_str(date1 + timedelta(i),'%Y%m%d')
        print(date)
        discs = Disc.objects.raw({'rcept_dt':date})
        cnt =  discs.count() 
        for index, disc in enumerate(discs):
            print(f'{index} / {cnt}', disc.rcept_dt, disc.corp.corp_name, disc.report_nm, disc._id)
            disc.url = get_doc_url(disc.rcept_no)
            disc.save()
            time.sleep(0.7)

if __name__ == '__main__':
    #2017/01/01 ~ 현재
    #post_disc_kr('20160101', '20161231')
    post_disc_kr('20160122', '20161231')
    #new_doc_url('20210226','20211231')
    
