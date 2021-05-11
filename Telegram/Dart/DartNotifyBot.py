from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TimedOut
from telegram.error import Unauthorized
from datetime import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup
import os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
import requests
import sqlite3

DB_NAME = "dart.db"

HELP_STRING = "\
1) 검색어 등록 방법\n\r\
    1. 여러개의 검색어를 한번에 등록할 경우\n\r\
        /add 회사명1 또는 공시내용1, 회사명2 또는 공시내용2\n\r\
        예) /add 증자, 합병, 경영계획, 삼성전자\n\r\
    2. 특정기업의 특정공시만을 확인하고 싶을 경우\n\r\
        /add 회사명:공시내용\n\r\
        예) /add 삼성전자:증자\n\r\
    3. 활용\n\r\
        예) /add 삼성전자:배당, 현대차:합병, LG화학\n\r\
        -> 삼성전자의 배당공시나 현대차의 합병공시, LG화학 공시가 있는 경우 알림\n\r\
2) 등록한 검색어 리스트 확인 방법\n\r\
    /list\n\r\
3) 검색어 삭제 방법\n\r\
    1. /list\n\r\
    -> 등록한 검색어가 모두 나열되고 나열된 검색어 중 삭제하고 싶은 검색어가 있으면 클릭시 삭제가능\n\r\
    2. /delall\n\r\
    -> 등록한 모든 검색어 삭제\n\r"

"""
/add 합병
/add 삼성전자
/add 유상, 합병
/add 삼성전자 배당
/add 삼성전자 배당, 현대차 증자
/add 삼성전자 배당 합병, 현대차 증자 감자
"""

def init_db():
    con = sqlite3.connect(DB_NAME)

    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS USERS(chat_id TEXT NOT NULL, name TEXT, join_date DATE, PRIMARY KEY(chat_id))")

    cur.execute("CREATE TABLE IF NOT EXISTS DASHBOARD(reg_date DATE NOT NULL, title TEXT, code_name TEXT, market TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS KEYWORDS(chat_id TEXT NOT NULL, keyword NOT NULL, PRIMARY KEY(chat_id, keyword))")

def send_message(context, chat_id, name, text):
    print('--- send', chat_id, name, text[:10])
    try:
        context.bot.send_message(chat_id=chat_id, text=text)
    except TimedOut as ex_to:
        print('@@@ error, ex_to', ex_to)
        try:
            context.bot.send_message(chat_id=chat_id, text=text, timeout=60)
        except Exception as ex1:
            print('@@@ error ex1', ex1)
    except Unauthorized as ex_ua:
        print('@@@ error, ex_ua', ex_ua, chat_id)
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute("DELETE FROM USERS WHERE chat_id = '{}'".format(chat_id))
        con.commit()
        con.close()
    except Exception as ex2:
        print('@@@ error, ex2', chat_id, ex2)

def check_board(last_board, fetched):
    if last_board is None or last_board.__len__() == 0:
        return True

    if fetched['reg_date'] > last_board['reg_date']:
        return True

    if fetched['reg_date'] == last_board['reg_date'] and last_board['code_name'] != fetched['code_name']:
        return True

    return False

def get_user_keyword(keywords, chat_id):
    user_keywords = list()
    for keyword in keywords:
        if keyword['chat_id'] != chat_id:
            continue
        user_keywords.append({'chat_id':chat_id, 'keyword':keyword['keyword']})

    return user_keywords

def callback_dart(context):
    fetched_list = fetch_dart()

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute("SELECT * FROM KEYWORDS")
    columns = [column[0] for column in cur.description]
    rows = cur.fetchall()
    keywords = list()
    for row in rows:
        keywords.append(dict(zip(columns, row)))

    cur.execute("SELECT * FROM USERS")
    columns = [column[0] for column in cur.description]
    rows = cur.fetchall()
    users = list()
    for row in rows:
        users.append(dict(zip(columns, row)))

    cur.execute("SELECT * FROM DASHBOARD")
    columns = [column[0] for column in cur.description]
    rows = cur.fetchall()
    last_board = {}
    for row in rows:
        last_board = dict(zip(columns, row))

    if not fetched_list:
        return

    reg_date = fetched_list[0]['reg_date']
    title = fetched_list[0]['title']
    code_name = fetched_list[0]['code_name']
    market = fetched_list[0]['market']

    cur.execute("DELETE FROM DASHBOARD")
    cur.execute("INSERT OR REPLACE INTO DASHBOARD(reg_date, title, code_name, market) VALUES('{}','{}', '{}', '{}')".format(reg_date, title, code_name, market))
    con.commit()
    con.close()

    for fetched in fetched_list:
        if check_board(last_board, fetched) != True:
            break

        for user in users:
            message = '['+fetched['code_name']+']'+fetched['title'] + '\n' + fetched['link']

            user_keywords = get_user_keyword(keywords, user['chat_id'])

            if user_keywords is None or user_keywords.__len__() == 0:
                send_message(context, user['chat_id'], user['name'], message)
            else:
                for user_keyword in user_keywords:
                    keyword = [x for x in user_keyword['keyword'].split(':') if x]
                    if keyword.__len__() == 0:
                        break
                    if keyword.__len__() == 1:
                        if keyword[0] in fetched['title'] or keyword[0] in fetched['code_name']:
                            send_message(context, user['chat_id'], user['name'],message)
                            break

                    if keyword[0] in fetched['code_name']:
                        for i in range(1,keyword.__len__()):
                            if keyword[i] in fetched['title']:
                                send_message(context, user['chat_id'], user['name'],message)
                                break


def exec_sql(sql):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute(sql)

    con.commit()
    con.close()

def fetch_sql(sql):
    row_list = list()
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute(sql)
    columns = [column[0] for column in cur.description]
    rows = cur.fetchall()
    for row in rows:
        row_list.append(dict(zip(columns,row)))
    con.close()

    return row_list

def auth(chat_id):
    # 박용은
    if chat_id == 442047336:
        return True
    # 박민규
    if chat_id == 40487101:
        return True
    return False

def users_command(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_chat.last_name + update.effective_chat.first_name

    if auth(chat_id) != True:
        return

    rows = fetch_sql("SELECT * FROM USERS ORDER BY JOIN_DATE")
    message = ''
    for row in rows:
        message += row['name'] + '\n\r'
    message += '* 총 {}명'.format(rows.__len__())
    send_message(context, name=name, chat_id=chat_id, text=message)

def keywords_command(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_chat.last_name + update.effective_chat.first_name

    if auth(chat_id) != True:
        return

    rows = fetch_sql("SELECT A.NAME, B.KEYWORD FROM USERS A, KEYWORDS B WHERE A.CHAT_ID = B.CHAT_ID ORDER BY A.JOIN_DATE, A.NAME")
    message = ''
    for row in rows:
        message += row['name'] + ' ' + row['keyword'] + '\n\r'
    send_message(context, name=name, chat_id=chat_id, text=message)

def help_command(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_chat.last_name + update.effective_chat.first_name

    send_message(context, name=name, chat_id=chat_id, text=HELP_STRING)

def start_command(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_chat.last_name + update.effective_chat.first_name

    print('start', name)

    exec_sql("INSERT OR REPLACE INTO USERS(chat_id, name, join_date) VALUES('{}','{}', datetime('now'))".format(chat_id, name))
    send_message(context, name=name, chat_id=chat_id, text=HELP_STRING)

def delall_command(update, context):
    chat_id = update.effective_chat.id
    exec_sql("DELETE FROM KEYWORDS WHERE chat_id = '{}'".format(chat_id))

def add_command(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text

    keywords = [x.strip() for x in text[5:].split(',') if x]

    for keyword in keywords:
        exec_sql("INSERT OR REPLACE INTO KEYWORDS(chat_id, keyword) VALUES('{}','{}')".format(chat_id, keyword))


def list_command(update, context):
    chat_id = update.effective_chat.id
    rows = fetch_sql("SELECT * FROM KEYWORDS WHERE chat_id = '{}'".format(chat_id))

    keyboard = list()
    for row in rows:
        keyboard.append([InlineKeyboardButton(row['keyword'], callback_data=row['keyword'])])
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=chat_id,
                             text='Please choose a item to delete',
                             reply_markup=reply_markup)

def get_message(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_chat.last_name + update.effective_chat.first_name
    text = update.message.text

    print('get_message', chat_id, name, text)

def fetch_dart():
    print('fetch_dart', datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    fetched_list = list()

    url = 'http://dart.fss.or.kr/dsac001/mainAll.do?selectDate=&sort=&series=&mdayCnt=0'
    source_code = requests.get(url)
    plain_text = source_code.text

    bs = BeautifulSoup(plain_text, 'lxml')
    table_list = bs.find('div', {'class' : 'table_list'})

    if table_list is None:
        return

    for tr_data in table_list.find_all('tr'):
        tds = tr_data.find_all('td')
        if tds is None or tds.__len__() < 5:
            continue
        hhmm = tds[0].text.strip()      #시간
        yymmdd = tds[4].text.strip()    #일자
        title = tds[2].text.strip() #보고서명
        code_name = tds[1].find('a').text.strip()   #종목명
        market = tds[1].find('img')["alt"]  #시장구분
        link = "http://dart.fss.or.kr" + tds[2].a.get('href')

        reg_date = yymmdd + ' ' + hhmm
        title = title.replace('\t', '').replace('\r','').replace('\n','')

        fetched_list.append({'reg_date':reg_date, 'title':title, 'code_name':code_name, 'market':market, 'link':link})

    return fetched_list

def callback_del_keyword(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id

    exec_sql("DELETE FROM KEYWORDS WHERE chat_id = '{}' AND keyword = '{}'".format(chat_id, query.data.strip()))

    context.bot.edit_message_text(text='Deleted keyword: {}'.format(query.data),
                        chat_id = chat_id,
                        message_id=query.message.message_id)

if __name__ == '__main__':
    init_db()

    my_token = '676500333:AAEn9gLG67aLCRa_U8-n4HqVR_2Lv0zD140'
    updater = Updater(my_token)

    #updater.dispatcher.add_handler(MessageHandler(Filters.text, get_message, pass_job_queue=True))
    updater.dispatcher.add_handler(CommandHandler('start',   start_command))
    updater.dispatcher.add_handler(CommandHandler('help',    help_command))
    updater.dispatcher.add_handler(CommandHandler('list',    list_command))
    updater.dispatcher.add_handler(CommandHandler('add',     add_command))
    updater.dispatcher.add_handler(CommandHandler('users',   users_command))
    updater.dispatcher.add_handler(CommandHandler('keywords',keywords_command))
    updater.dispatcher.add_handler(CommandHandler('delall',  delall_command))

    updater.dispatcher.add_handler(CallbackQueryHandler(callback_del_keyword))

    j = updater.job_queue
    job_minute = j.run_repeating(callback_dart, interval=60 * 5, first=0)

    updater.start_polling()
    updater.idle()

