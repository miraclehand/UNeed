import os
import sys
sys.path.append('../../')
sys.path.append(os.path.dirname(__file__))

from datetime import datetime, timedelta
from commons.utils.datetime import add_year, str_to_datetime
from task.pair import AbstractPairFactory
from task.xls import reorganize_xls_picked_pair, save_xls_picked_pair

def gen_node_pair(cntry, begin=None, end=None):
    if not begin:
        today = datetime.today()
        begin = datetime(today.year, today.month, today.day)
        end   = begin
    elif not end:
        begin = str_to_datetime(begin, "%Y%m%d")
        end   = begin
    else:
        begin = str_to_datetime(begin, "%Y%m%d")
        end   = str_to_datetime(end,   "%Y%m%d")

    factory = AbstractPairFactory.get_factory(cntry)
    node_pair = factory.create_node_pair()

    delta = end - begin
    for i in range(delta.days + 1):
        date2 = begin + timedelta(i)
        node_pair.make_model(date2)

def gen_picked_pair(cntry, begin=None, end=None):
    if not begin:
        today = datetime.today()
        begin = datetime(today.year, today.month, today.day)
        end   = begin
    elif not end:
        begin = str_to_datetime(begin, "%Y%m%d")
        end   = begin
    else:
        begin = str_to_datetime(begin, "%Y%m%d")
        end   = str_to_datetime(end,   "%Y%m%d")

    factory = AbstractPairFactory.get_factory(cntry)
    picked_pair = factory.create_picked_pair()

    delta = end - begin 
    for i in range(delta.days + 1):
        date2 = begin + timedelta(i)
        date, cnt = picked_pair.make_model(date2)
        if cnt > 0:
            save_xls_picked_pair(cntry, date, date)
        reorganize_xls_picked_pair(cntry, date)

def gen_save_xls_picked_pair(cntry, date1, date2):
    date1 = str_to_datetime(date1, "%Y%m%d")
    date2 = str_to_datetime(date2, "%Y%m%d")
    save_xls_picked_pair(cntry, date1, date2)

if __name__ == '__main__':
    #put_candle_kr()
    #gen_node_pair  ('us', '20200816', '20200816')
    #gen_picked_pair('us', '20200825', '20200825')
    #gen_save_xls_picked_pair('kr', '20200824', '20200824')
    #reorganize_xls_picked_pair('us', date2)

    #gen_node_pair('kr', '20200822', '20200822')
    #save_xls_picked_pair('us', '20200829', '20200829')
    #gen_node_pair('us', '20200823', '20200823')
    #gen_picked_pair('us')
    """
    cntry = 'us'
    factory = AbstractPairFactory.get_factory(cntry)
    picked_pair = factory.create_picked_pair()
    date, cnt = picked_pair.make_model()
    save_xls_picked_pair(cntry, date, date)
    reorganize_xls_picked_pair(cntry, date)
    """
    #gen_node_pair('kr', '20200101', '20210507')
    #gen_node_pair('us', '20210825', '20211027')
    gen_picked_pair('kr', '20211118', '20211118')
    #gen_picked_pair('us', '20211111', '20211111')
    #reorganize_xls_picked_pair('kr', str_to_datetime('20210430', "%Y%m%d"))
    
