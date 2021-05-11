import requests
from flask import url_for
from app import app

def post_stock_kr():
    with app.app_context():
        requests.post(url_for('stock', cntry='kr'))

def put_stock_kr():
    with app.app_context():
        requests.put(url_for('stock', cntry='kr'))

def post_candle_kr():
    with app.app_context():
        requests.post(url_for('candle', cntry='kr'))

def put_candle_kr():
    with app.app_context():
        requests.put(url_for('candle', cntry='kr'))

def post_stock_us():
    with app.app_context():
        requests.post(url_for('stock', cntry='us'))

def put_stock_us():
    with app.app_context():
        requests.put(url_for('stock', cntry='us'))

def post_candle_us():
    with app.app_context():
        requests.post(url_for('candle', cntry='us'))

def put_candle_us():
    with app.app_context():
        requests.put(url_for('candle', cntry='us'))

if __name__ == '__main__':
    pass
