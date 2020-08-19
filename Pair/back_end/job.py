import requests
from flask import url_for
from datetime import datetime
from app import app
from task.singleton import pool_ohlcv
from task.xls import reorganize_xls_simula

def put_node_pair_kr():
    with app.app_context():
        requests.put(url_for('node_pair', cntry='kr'))

def put_node_pair_us():
    with app.app_context():
        requests.put(url_for('node_pair', cntry='us'))

def put_picked_pair_kr():
    with app.app_context():
        requests.put(url_for('picked_pair', cntry='kr'))

def put_picked_pair_us():
    with app.app_context():
        requests.put(url_for('picked_pair', cntry='us'))

def put_classify():
    with app.app_context():
        requests.put(url_for('classify'))

def job_daily_kr():
    reorganize_xls_simula('kr', datetime.today())
    pool_ohlcv.clear()

def job_daily_us():
    reorganize_xls_simula('us', datetime.today())
    pool_ohlcv.clear()
