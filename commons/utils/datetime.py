from datetime import datetime
from dateutil.relativedelta import relativedelta

def datetime_to_str(date, formatter):
    if not date:
        return ''
    return date.strftime(formatter)

def str_to_datetime(date, formatter):
    if not date:
        return ''
    if date == '-':
        return date
    return datetime.strptime(date, formatter)

def to_yyyymmdd(date):
    return datetime(year=date.year, month=date.month, day=date.day)

#22시30분이 아니라면 하루전일자로 일자를 바꿔야 한다.
def cvrt_date_us(date):
    if date.hour != 22 or date.minute != 30:
        date = date - relativedelta(days = 1)
    return to_yyyymmdd(date)

def add_year(date, year):
    try:
        date = datetime(year=date.year+year,month=date.month,day=date.day)
    except:
        date = datetime(year=date.year+year,month=date.month,day=date.day-1)
    return date

def date_to_datetime(date):
    return datetime(year=date.year,month=date.month,day=date.day)

def extract(symbol, data, covt, default):
    return covt(data[symbol]) if symbol in data else default

