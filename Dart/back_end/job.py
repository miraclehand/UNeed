import requests
from flask import url_for
from datetime import datetime
from app import app
from task.singleton import pool_corps, pool_ohlcv, od

def post_corp_kr():
    with app.app_context():
        requests.post(url_for('corp', cntry='kr'))

def put_corp_kr():
    with app.app_context():
        requests.put(url_for('corp', cntry='kr'))

def post_disc_kr():
    with app.app_context():
        requests.post(url_for('disc', cntry='kr'))

def put_disc_kr():
    with app.app_context():
        requests.put(url_for('disc', cntry='kr'))

def put_user_disc_kr():
    with app.app_context():
        requests.put(url_for('user_disc', cntry='kr'))

def post_alert_kr():
    with app.app_context():
        requests.post(url_for('alert', cntry='kr', usid='yepark'))

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

