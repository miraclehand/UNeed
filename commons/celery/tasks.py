import sys
sys.path.append('../../')

from celery import Celery
from Collector.back_end.gen_data import insert_stock, insert_candle
from Collector.back_end.gen_data import upsert_stock, upsert_candle
from Collector.back_end.gen_data import delete_stock, delete_candle
from Pair.back_end.gen_data import gen_node_pair, gen_picked_pair
from Pair.back_end.gen_data import save_xls_picked_pair

app = Celery('uneed', broker='pyamqp://guest@localhost//')
#app = Celery('uneed', backend='rpc://guest@localhost//', broker='pyamqp://guest@localhost//')

@app.task(name='commons.celery.tasks.post_stock')
def post_stock(cntry):
    insert_stock(cntry)

@app.task(name='commons.celery.tasks.put_stock')
def put_stock(cntry):
    upsert_stock(cntry)

@app.task(name='commons.celery.tasks.del_stock')
def del_stock(cntry):
    delete_stock(cntry)

@app.task(name='commons.celery.tasks.post_candle')
def post_candle(cntry, code):
    insert_candle(cntry, code)

@app.task(name='commons.celery.tasks.put_candle')
def put_candle(cntry, code):
    upsert_candle(cntry, code)
    gen_picked_pair(cntry)

@app.task(name='commons.celery.tasks.del_candle')
def del_candle(cntry, code):
    delete_candle(cntry, code)

@app.task(name='commons.celery.tasks.put_node_pair')
def put_node_pair(cntry):
    gen_node_pair(cntry)

@app.task(name='commons.celery.tasks.put_picked_pair')
def put_picked_pair(cntry):
    gen_picked_pair(cntry)
