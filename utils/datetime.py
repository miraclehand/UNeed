from datetime import datetime

def datetime_to_str(date, formatter):
    if not date:
        return ''
    return date.strftime(formatter)

def str_to_datetime(date, formatter):
    if not date:
        return ''
    return datetime.strptime(date, formatter)

def to_yyyymmdd(date):
    return datetime(year=date.year, month=date.month, day=date.day)

def add_year(date, year):
    try:
        date = datetime(year=date.year+year,month=date.month,day=date.day)
    except:
        date = datetime(year=date.year+year,month=date.month,day=date.day-1)
    return date

def extract(symbol, data, covt, default):
    return covt(data[symbol]) if symbol in data else default

