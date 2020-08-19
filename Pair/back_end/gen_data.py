import server

from job import put_node_pair_kr, put_picked_pair_kr
from job import put_node_pair_us, put_picked_pair_us
from job import put_classify

from datetime import datetime, timedelta
from task.pair import AbstractPairFactory
from utils.datetime import add_year, str_to_datetime
from task.xls import reorganize_xls_picked_pair, save_xls_picked_pair

def gen_node_pair(cntry, begin, end):
    begin = str_to_datetime(begin, "%Y%m%d")
    end   = str_to_datetime(end,   "%Y%m%d")

    factory = AbstractPairFactory.get_factory(cntry)
    node_pair = factory.create_node_pair()

    delta = end - begin
    for i in range(delta.days + 1):
        date2 = begin + timedelta(i)
        date1 = add_year(date2, -2)
        node_pair.make_model(date1, date2)

def gen_picked_pair(cntry, begin, end):
    begin = str_to_datetime(begin, "%Y%m%d")
    end   = str_to_datetime(end,   "%Y%m%d")

    factory = AbstractPairFactory.get_factory(cntry)
    picked_pair = factory.create_picked_pair()

    delta = end - begin 
    for i in range(delta.days + 1):
        date2 = begin + timedelta(i)
        date1 = add_year(date2, -2)
        picked_pair.make_model(date1, date2)
        save_xls_picked_pair(cntry, date2, date2)
        reorganize_xls_picked_pair(cntry, date2)

def gen_save_xls_picked_pair(cntry, date1, date2):
    date1 = str_to_datetime(date1, "%Y%m%d")
    date2 = str_to_datetime(date2, "%Y%m%d")
    save_xls_picked_pair(cntry, date1, date2)

if __name__ == '__main__':
    #put_candle_kr()
    gen_node_pair  ('us', '20200814', '20200814')
    #gen_picked_pair('kr', '20200703', '20200703')
    #gen_node_pair  ('us', '20200703', '20200703')
    #gen_picked_pair('us', '20200706', '20200706')
    #date1 = str_to_datetime('20200703', "%Y%m%d")
    #date2 = str_to_datetime('20200703', "%Y%m%d")
    #gen_save_xls_picked_pair('us', '20200706', '20200706')
    #reorganize_xls_picked_pair('us', date2)
    pass
