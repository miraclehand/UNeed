import requests
from flask import url_for
from datetime import datetime
from app import app
from task.singleton import pool_corps, pool_ohlcv, od

def post_corp_kr():
    with app.app_context():
        r = requests.post(url_for('corp', cntry='kr'))
        r.close()

def put_corp_kr():
    with app.app_context():
        r = requests.put(url_for('corp', cntry='kr'))
        r.close()

def post_disc_kr(begin, end):
    with app.app_context():
        r = requests.post(url_for('disc', cntry='kr', begin=begin, end=end))
        r.close()

def put_disc_kr():
    with app.app_context():
        r = requests.put(url_for('disc', cntry='kr'))
        r.close()

def put_user_disc_kr():
    with app.app_context():
        r = requests.put(url_for('user_disc', cntry='kr'))
        r.close()

def put_tick_kr():
    with app.app_context():
        r = requests.put(url_for('tick', cntry='kr'))
        r.close()

def post_alert_kr():
    with app.app_context():
        r = requests.post(url_for('alert', cntry='kr', usid='yepark'))
        r.close()

def job_weekday():
    pass

def job_weekly():
    pass

def job_daily():
    put_corp_kr()
    pool_corps.clear()
    pool_ohlcv.clear()
    od.clear()

def job_seconds():
    put_disc_kr()
    #put_user_disc_kr()

def job_tick():
    put_tick_kr()

