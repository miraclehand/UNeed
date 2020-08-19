from datetime import datetime

def write_log(*logs):
    fileName = 'log/%s.log' % (datetime.today().strftime('%Y%m%d'))
    f = open(fileName, 'a+')
    f.write('[%s]' % (datetime.today().strftime('%H:%M:%S')))
    for log in logs:
        f.write(str(log) + ' ')
    f.write('\n')
    f.close()
