import xlsxwriter
import os, re
import calendar
from app import app
from datetime import datetime, timedelta
from utils.datetime import datetime_to_str
from task.mfg.reproduce import target_field
from db.models import NodePairKr, PickedPairKr, SimulaReportKr
from db.models import NodePairUs, PickedPairUs, SimulaReportUs


SIMULA_PATH = app._static_folder + '/xls/simula'
SIMULA_NAME = 'Simula'

def reorganize_xls_picked_pair(cntry, date):
    if date.day != calendar.monthrange(date.year,date.month)[1]:
        return

    date1 = datetime(date.year, date.month, 1, 0, 0)
    date2 = date

    path = app._static_folder + f'/xls/{cntry}/pair'
    name = f'PickedPair_{cntry}'

    purge_month(path, name, date)
    save_xls_picked_pair(cntry, date1, date2)

def reorganize_xls_simula(cntry, date):
    # reorganize day
    date1 = datetime(date.year, date.month, date.day, 0, 0)
    date2 = date1

    purge_day(SIMULA_PATH, SIMULA_NAME, date)
    save_xls_simula_daily(cntry, date1, date2)

    # reorganize month
    if date.day != calendar.monthrange(date.year,date.month)[1]:
        return

    date1 = datetime(date.year, date.month, 1, 0, 0)
    date2 = date

    path = app._static_folder + f'/xls/{cntry}/simula'
    name = f'Simula.{cntry}'

    purge_month(path, name, date)
    save_xls_simula_daily(cntry, date1, date2)

def purge_month(path, name, date):
    year  = format(date.year, '04')
    month = format(date.month,'02')

    pattern = '%s_%s%s.*xlsx' % (name, year, month)
    for f in os.listdir(path):
        if re.search(pattern, f):
            os.remove(os.path.join(path, f))

def purge_day(path, name, date):
    year  = format(date.year, '04')
    month = format(date.month,'02')
    day   = format(date.day,  '02')

    pattern = '%s_%s%s%s.*xlsx' % (name, year, month, day)
    for f in os.listdir(path):
        if re.search(pattern, f):
            os.remove(os.path.join(path, f))

def write_sheet_simula(cursor, date):
    sheet = workbook.add_worksheet(datetime_to_str(date, '%Y%m%d'))

    row = 0
    sheet.write(row, 0, 'period:' + str(cursor.date1.date()) + '~' + str(cursor.date2.date()))

    row = 1
    sheet.write(row, 0, 'strainer')
    sheet.write(row, 1, str(cursor.strainer.to_dict))

    row = 3
    sheet.write(row, 0, '진입일자')
    sheet.write(row, 1, '포지션')
    sheet.write(row, 2, '진입가격(LONG)')
    sheet.write(row, 3, '진입수량(LONG)')
    sheet.write(row, 4, '진입금액(LONG)')
    sheet.write(row, 5, '진입가격(SHORT)')
    sheet.write(row, 6, '진입수량(SHORT)')
    sheet.write(row, 7, '진입금액(SHORT)')
    sheet.write(row, 8, '청산일자')
    sheet.write(row, 9, '청산가격(LONG)')
    sheet.write(row,10, '청산가격(SHORT)')
    sheet.write(row,11, '수익률')

    for entry in cursor.entries:
        row = row + 1
        entry_date = min(entry.Long.entry_date, entry.Short.entry_date)

        if not entry.Long.exit_date or not entry.Short.exit_date:
            exit_date = None
        else:
            exit_date = max(entry.Long.exit_date, entry.Short.exit_date)

        sheet.write(row, 0, datetime_to_str(entry_date, '%Y-%m-%d'))
        sheet.write(row, 1, entry.label)
        sheet.write(row, 2, entry.Long.entry_uv)
        sheet.write(row, 3, entry.Long.entry_qty)
        sheet.write(row, 4, entry.Long.entry_amt)
        sheet.write(row, 5, entry.Short.entry_uv)
        sheet.write(row, 6, entry.Short.entry_qty)
        sheet.write(row, 7, entry.Short.entry_amt)
        sheet.write(row, 8, datetime_to_str(exit_date, '%Y-%m-%d'))
        sheet.write(row, 9, entry.Long.exit_uv)
        sheet.write(row,10, entry.Short.exit_uv)
        sheet.write(row,11, entry.yld)

def write_workbook_simula_latest_kr(workbook, date1, date2):
    if date1 != date2:
        return
    
    cursor = SimulaReportKr.objects.raw({'create_date':{'$eq':date2}})
    report = cursor.order_by([('seq',-1)]).first()

    sheet_name = datetime_to_str(date2, '%Y%m%d') + '-%d' % report.seq
    sheet = workbook.add_worksheet(sheet_name)
    write_sheet_simula(report, sheet)

def write_workbook_simula_latest_us(workbook, date1, date2):
    if date1 != date2:
        return
    
    cursor = SimulaReportUs.objects.raw({'create_date':{'$eq':date2}})
    report = cursor.order_by([('seq',-1)]).first()

    sheet_name = datetime_to_str(date2, '%Y%m%d') + '-%d' % report.seq
    sheet = workbook.add_worksheet(sheet_name)
    write_sheet_simula(report, sheet)

def write_workbook_simula_daily_kr(workbook, date1, date2):
    delta = date2 - date1
    for i in range(delta.days + 1):
        date = date1 + timedelta(i)

        cursor = SimulaReportKr.objects.raw({'create_date':{'$eq':date}})
        reports= cursor.order_by([('seq',1)])

        if reports.count() == 0:
            continue

        for report in reports:
            sheet_name = datetime_to_str(date, '%Y%m%d') + '-%d' % report.seq
            sheet = workbook.add_worksheet(sheet_name)
            write_sheet_simula(report, sheet)

def write_workbook_simula_daily_us(workbook, date1, date2):
    delta = date2 - date1
    for i in range(delta.days + 1):
        date = date1 + timedelta(i)

        cursor = SimulaReportUs.objects.raw({'create_date':{'$eq':date}})
        reports= cursor.order_by([('seq',1)])

        if reports.count() == 0:
            continue

        for report in reports:
            sheet_name = datetime_to_str(date, '%Y%m%d') + '-%d' % report.seq
            sheet = workbook.add_worksheet(sheet_name)
            write_sheet_simula(report, sheet)

def write_sheet_node_pair(workbook, cursor, date):
    sheet = workbook.add_worksheet(datetime_to_str(date, '%Y%m%d'))

    date1 = cursor.limit(1).project({'date1':1}).get({}).date1
    date2 = cursor.limit(1).project({'date2':1}).get({}).date2

    row = 0
    sheet.write(row, 0, 'period:' + str(date1.date()) + '~' + str(date2.date()))

    row = 1
    sheet.write(row, 0, '종목코드1')
    sheet.write(row, 1, '종목명1')
    sheet.write(row, 2, '시장1')
    sheet.write(row, 3, '계열사1')
    sheet.write(row, 4, '업종1')
    sheet.write(row, 5, '추종1')
    sheet.write(row, 6, 'PER1')
    sheet.write(row, 7, '50일거래대금(백만)1')
    sheet.write(row, 8, '종목코드2')
    sheet.write(row, 9, '종목명2')
    sheet.write(row,10, '시장2')
    sheet.write(row,11, '계열사2')
    sheet.write(row,12, '업종2')
    sheet.write(row,13, '추종2')
    sheet.write(row,14, 'PER2')
    sheet.write(row,15, '50일거래대금(백만)2')
    sheet.write(row,16, 'Correlation')

    for node in cursor:
        if not target_field(node.stock1, node.stock2):
            continue
        row = row + 1
        sheet.write(row, 0, node.stock1.code)
        sheet.write(row, 1, node.stock1.name)
        sheet.write(row, 2, node.stock1.exchange)
        sheet.write(row, 3, node.stock1.parent)
        sheet.write(row, 4, node.stock1.industry)
        sheet.write(row, 5, node.stock1.aimed)
        sheet.write(row, 6, node.per1)
        sheet.write(row, 7, node.stock1.avg_v50)
        sheet.write(row, 8, node.stock2.code)
        sheet.write(row, 9, node.stock2.name)
        sheet.write(row,10, node.stock2.exchange)
        sheet.write(row,11, node.stock2.parent)
        sheet.write(row,12, node.stock2.industry)
        sheet.write(row,13, node.stock2.aimed)
        sheet.write(row,14, node.per2)
        sheet.write(row,15, node.stock2.avg_v50)
        sheet.write(row,16, node.corr)

def write_sheet_picked_pair(workbook, cursor, date):
    sheet = workbook.add_worksheet(datetime_to_str(date, '%Y%m%d'))

    date1 = cursor.limit(1).project({'date1':1}).get({}).date1
    date2 = cursor.limit(1).project({'date2':1}).get({}).date2

    row = 0
    sheet.write(row, 0, 'period:' + str(date1.date()) + '~' + str(date2.date()))

    row = 1
    sheet.write(row, 0, '종목코드1')
    sheet.write(row, 1, '종목명1')
    sheet.write(row, 2, '시장1')
    sheet.write(row, 3, '계열사1')
    sheet.write(row, 4, '업종1')
    sheet.write(row, 5, '추종1')
    sheet.write(row, 6, 'PER1')
    sheet.write(row, 7, '50일거래대금(백만)1')
    sheet.write(row, 8, '종목코드2')
    sheet.write(row, 9, '종목명2')
    sheet.write(row,10, '시장2')
    sheet.write(row,11, '계열사2')
    sheet.write(row,12, '업종2')
    sheet.write(row,13, '추종2')
    sheet.write(row,14, 'PER2')
    sheet.write(row,15, '50일거래대금(백만)2')
    sheet.write(row,16, 'Correlation')
    sheet.write(row,17, 'Cointegration-계산값')
    sheet.write(row,18, 'ks pvalue')
    sheet.write(row,19, 'adf pvalue')
    sheet.write(row,20, 'coint pvalue')
    sheet.write(row,21, 'value')
    sheet.write(row,22, 'density')
    sheet.write(row,23, 'place')
    sheet.write(row,24, 'std of coint')

    sheet.write(row,25, '0 hits')
    sheet.write(row,26, 'cycle 10')
    sheet.write(row,27, 'cycle 20')
    sheet.write(row,28, 'cycle 30')
    sheet.write(row,29, 'cycle 40')
    sheet.write(row,30, 'cycle 50')
    sheet.write(row,31, 'cycle 60')
    sheet.write(row,32, 'cycle 70')
    sheet.write(row,33, 'cycle 80')
    sheet.write(row,34, 'cycle 90')

    sheet.write(row,35, 'cycle 10-20')
    sheet.write(row,36, 'cycle 10-30')
    sheet.write(row,37, 'cycle 10-40')
    sheet.write(row,38, 'cycle 10-50')
    sheet.write(row,39, 'cycle 10-60')
    sheet.write(row,40, 'cycle 10-70')
    sheet.write(row,41, 'cycle 10-80')
    sheet.write(row,42, 'cycle 10-90')

    sheet.write(row,43, 'cycle 20-30')
    sheet.write(row,44, 'cycle 20-40')
    sheet.write(row,45, 'cycle 20-50')
    sheet.write(row,46, 'cycle 20-60')
    sheet.write(row,47, 'cycle 20-70')
    sheet.write(row,48, 'cycle 20-80')
    sheet.write(row,49, 'cycle 20-90')

    sheet.write(row,50, 'cycle 30-40')
    sheet.write(row,51, 'cycle 30-50')
    sheet.write(row,52, 'cycle 30-60')
    sheet.write(row,53, 'cycle 30-70')
    sheet.write(row,54, 'cycle 30-80')
    sheet.write(row,55, 'cycle 30-90')

    sheet.write(row,56, 'cycle 40-50')
    sheet.write(row,57, 'cycle 40-60')
    sheet.write(row,58, 'cycle 40-70')
    sheet.write(row,59, 'cycle 40-80')
    sheet.write(row,60, 'cycle 40-90')

    sheet.write(row,61, 'cycle 50-60')
    sheet.write(row,62, 'cycle 50-70')
    sheet.write(row,63, 'cycle 50-80')
    sheet.write(row,64, 'cycle 50-90')

    sheet.write(row,65, 'cycle 60-70')
    sheet.write(row,66, 'cycle 60-80')
    sheet.write(row,67, 'cycle 60-90')

    sheet.write(row,68, 'cycle 70-80')
    sheet.write(row,69, 'cycle 70-90')

    sheet.write(row,70, 'cycle 80-90')

    for pair in cursor:
        if not target_field(pair.stock1, pair.stock2):
            continue
        ratio_of_place = pair.fig_str.place / pair.fig_str.place_cnt * 100

        row = row + 1
        sheet.write(row, 0, pair.stock1.code)
        sheet.write(row, 1, pair.stock1.name)
        sheet.write(row, 2, pair.stock1.exchange)
        sheet.write(row, 3, pair.stock1.parent)
        sheet.write(row, 4, pair.stock1.industry)
        sheet.write(row, 5, pair.stock1.aimed)
        sheet.write(row, 6, pair.per1)
        sheet.write(row, 7, pair.stock1.avg_v50)
        sheet.write(row, 8, pair.stock2.code)
        sheet.write(row, 9, pair.stock2.name)
        sheet.write(row,10, pair.stock2.exchange)
        sheet.write(row,11, pair.stock2.parent)
        sheet.write(row,12, pair.stock2.industry)
        sheet.write(row,13, pair.stock2.aimed)
        sheet.write(row,14, pair.per2)
        sheet.write(row,15, pair.stock2.avg_v50)
        sheet.write(row,16, pair.corr)
        sheet.write(row,17, pair.fig_str.coint_calc)
        sheet.write(row,18, pair.fig_str.ks_pvalue)
        sheet.write(row,19, pair.fig_str.adf_pvalue)
        sheet.write(row,20, pair.fig_str.coint_pvalue)
        sheet.write(row,21, pair.fig_str.value)
        sheet.write(row,22, pair.fig_str.density)
        sheet.write(row,23, '%d/%d(%.2f%%)' % (pair.fig_str.place,pair.fig_str.place_cnt,ratio_of_place))
        if pair.coint_std != -1:
            sheet.write(row,24, pair.coint_std)

        sheet.write(row,25, pair.fig_str.hit0_cnt)
        sheet.write(row,26, pair.fig_str.cy10_cnt)
        sheet.write(row,27, pair.fig_str.cy20_cnt)
        sheet.write(row,28, pair.fig_str.cy30_cnt)
        sheet.write(row,29, pair.fig_str.cy40_cnt)
        sheet.write(row,30, pair.fig_str.cy50_cnt)
        sheet.write(row,31, pair.fig_str.cy60_cnt)
        sheet.write(row,32, pair.fig_str.cy70_cnt)
        sheet.write(row,33, pair.fig_str.cy80_cnt)
        sheet.write(row,34, pair.fig_str.cy90_cnt)

        sheet.write(row,35, pair.fig_str.cy10_20_cnt)
        sheet.write(row,36, pair.fig_str.cy10_30_cnt)
        sheet.write(row,37, pair.fig_str.cy10_40_cnt)
        sheet.write(row,38, pair.fig_str.cy10_50_cnt)
        sheet.write(row,39, pair.fig_str.cy10_60_cnt)
        sheet.write(row,40, pair.fig_str.cy10_70_cnt)
        sheet.write(row,41, pair.fig_str.cy10_80_cnt)
        sheet.write(row,42, pair.fig_str.cy10_90_cnt)

        sheet.write(row,43, pair.fig_str.cy20_30_cnt)
        sheet.write(row,44, pair.fig_str.cy20_40_cnt)
        sheet.write(row,45, pair.fig_str.cy20_50_cnt)
        sheet.write(row,46, pair.fig_str.cy20_60_cnt)
        sheet.write(row,47, pair.fig_str.cy20_70_cnt)
        sheet.write(row,48, pair.fig_str.cy20_80_cnt)
        sheet.write(row,49, pair.fig_str.cy20_90_cnt)

        sheet.write(row,50, pair.fig_str.cy30_40_cnt)
        sheet.write(row,51, pair.fig_str.cy30_50_cnt)
        sheet.write(row,52, pair.fig_str.cy30_60_cnt)
        sheet.write(row,53, pair.fig_str.cy30_70_cnt)
        sheet.write(row,54, pair.fig_str.cy30_80_cnt)
        sheet.write(row,55, pair.fig_str.cy30_90_cnt)

        sheet.write(row,56, pair.fig_str.cy40_50_cnt)
        sheet.write(row,57, pair.fig_str.cy40_60_cnt)
        sheet.write(row,58, pair.fig_str.cy40_70_cnt)
        sheet.write(row,59, pair.fig_str.cy40_80_cnt)
        sheet.write(row,60, pair.fig_str.cy40_90_cnt)

        sheet.write(row,61, pair.fig_str.cy50_60_cnt)
        sheet.write(row,62, pair.fig_str.cy50_70_cnt)
        sheet.write(row,63, pair.fig_str.cy50_80_cnt)
        sheet.write(row,64, pair.fig_str.cy50_90_cnt)

        sheet.write(row,65, pair.fig_str.cy60_70_cnt)
        sheet.write(row,66, pair.fig_str.cy60_80_cnt)
        sheet.write(row,67, pair.fig_str.cy60_90_cnt)

        sheet.write(row,68, pair.fig_str.cy70_80_cnt)
        sheet.write(row,69, pair.fig_str.cy70_90_cnt)

        sheet.write(row,70, pair.fig_str.cy80_90_cnt)

def make_filename(path, name, seq, date1, date2):
    if date1 == date2:
        name = name + '_' + datetime_to_str(date1, '%Y%m%d')
    else:
        name = name + '_' + datetime_to_str(date1, '%Y%m')

    if seq:
        name = name + '_' + '%03d' % seq

    name = name + '.xlsx'

    return os.path.join(path, name)

def save_xls(filename, write_workbook, date1, date2):
    workbook = xlsxwriter.Workbook(filename, {'constant_memory':True})
    sheets = write_workbook(workbook, date1, date2)
    if sheets > 0: workbook.close() # save xls
    else:          workbook = None  # skip

def write_node_pair_kr(workbook, date1, date2):
    cursor = NodePairKr.objects.raw({'date2':{'$eq':date2}})
    if cursor.count() == 0:
        return 0

    write_sheet_node_pair(workbook, cursor, date2)
    return 1

def write_node_pair_us(workbook, date1, date2):
    cursor = NodePairUs.objects.raw({'date2':{'$eq':date2}})
    if cursor.count() == 0: return 0

    write_sheet_node_pair(workbook, cursor, date2)
    return 1

def write_picked_pair_kr(workbook, date1, date2):
    cnt = 0
    delta = date2 - date1
    for i in range(delta.days + 1):
        date = date1 + timedelta(i)

        cursor = PickedPairKr.objects.raw({'date2':{'$eq':date}})
        if cursor.count() == 0: continue

        write_sheet_picked_pair(workbook, cursor, date)
        cnt = cnt + 1
    return cnt

def write_picked_pair_us(workbook, date1, date2):
    cnt = 0
    delta = date2 - date1
    for i in range(delta.days + 1):
        date = date1 + timedelta(i)

        cursor = PickedPairUs.objects.raw({'date2':{'$eq':date}})
        if cursor.count() == 0: continue

        write_sheet_picked_pair(workbook, cursor, date)
        cnt = cnt + 1
    return cnt

def save_xls_node_pair(cntry, date):
    if cntry == 'kr': write_workbook = write_node_pair_kr
    if cntry == 'us': write_workbook = write_node_pair_us

    path = app._static_folder + f'/xls/{cntry}/node'
    name = f'NodePair.{cntry}'

    filename = make_filename(path, name, None, date, date)
    save_xls(filename, write_workbook, date, date)

def save_xls_picked_pair(cntry, date1, date2):
    if cntry == 'kr': write_workbook = write_picked_pair_kr
    if cntry == 'us': write_workbook = write_picked_pair_us

    path = app._static_folder + f'/xls/{cntry}/pair'
    name = f'PickedPair_{cntry}'

    filename = make_filename(path, name, None, date1, date2)
    save_xls(filename, write_workbook, date1, date2)

#save latest simula
def save_xls_simula_latest(date):
    if cntry == 'kr': SimulaReport, write_workbook = write_simula_latest_kr, SimulaReportKr
    if cntry == 'us': SimulaReport, write_workbook = write_simula_latest_us, SimulaReportUs

    path = app._static_folder + '/xls/{cntry}/simula'
    name = f'Simula.{cntry}'

    cursor = SimulaReport.objects.raw({'create_date':{'$eq':date}})
    seq = cursor.order_by([('seq',-1)]).first().seq

    filename = make_filename(path, name, seq, date, date)
    save_xls(filename, write_workbook, date, date)

#save daily simula
def save_xls_simula_daily(cntry, date1, date2):
    if cntry == 'kr': write_workbook = write_simula_daily_kr
    if cntry == 'us': write_workbook = write_simula_daily_us

    path = app._static_folder + '/xls/{cntry}/simula'
    name = f'Simula.{cntry}'

    filename = make_filename(path, name, None, date1, date2)
    save_xls(filename, write_workbook, date1, date2)

if __name__ == '__main__':
    date1 = datetime(year=2018,month=2,day=1)
    date2 = datetime(year=2018,month=2,day=28)
    cntry = 'kr'
    save_xls_picked_pair(cntry, date1, date2)

    from datetime import datetime
    from task.xls import save_xls_simula_latest
    date1 = datetime(year=2019,month=10,day=12)
    date2 = date1
    save_xls_simula_latest(cntry, date1, date2)

