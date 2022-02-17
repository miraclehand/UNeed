import sqlite3
import telegram
import datetime
import asyncio

DB_FOR_TELE= "../../Telegram/Dart/dart.db"
TOKEN_FOR_TELE = '676500333:AAEn9gLG67aLCRa_U8-n4HqVR_2Lv0zD140'

bot = telegram.Bot(token = TOKEN_FOR_TELE)

async def do_async(r):
    chat_id, name, text = r['chat_id'], r['name'], r['text']
    #print('do_async', chat_id, name, text[:20])
    idx = text.find('&dcmNo')
    text = text[:idx].replace('report/viewer', 'dsaf001/main')
    print('do_async', chat_id, name, text)
    loop = asyncio.get_event_loop() 
    loop.run_in_executor(None, bot.sendMessage, chat_id, text)

async def main_async(receivers):
    futures = [
        asyncio.ensure_future(do_async(receiver)) for receiver in receivers
    ]
    await asyncio.gather(*futures)

def send_telegram(new_discs):
    receivers = []
    con = sqlite3.connect(DB_FOR_TELE)
    cur = con.cursor()

    for disc in new_discs:
        corp_name, report_nm, url = disc.corp.corp_name, disc.report_nm,disc.url
        label = corp_name + report_nm
        text = f'[{corp_name}] {report_nm}\n{url}'

        cur.execute(f"SELECT A.CHAT_ID, A.NAME, SUBSTR(B.KEYWORD,1,INSTR(B.KEYWORD,':')-1) corp_name,  SUBSTR(B.KEYWORD,INSTR(B.KEYWORD,':')+1,LENGTH(B.KEYWORD)) keyword, '{text}' text FROM USERS A, KEYWORDS B WHERE A.CHAT_ID = B.CHAT_ID AND B.KEYWORD LIKE '%:%' AND SUBSTR(B.KEYWORD,1,INSTR(B.KEYWORD,':')-1) = '{corp_name}' ")
        columns = [column[0] for column in cur.description]
        results = cur.fetchall()
        results = list(dict(zip(columns, rows)) for rows in results)

        recv = []
        for index, r in enumerate(results):
            chat_id, name, keyword, text = r['chat_id'], r['name'], r['keyword'], r['text']
            if keyword in report_nm:
                recv.append({'chat_id':chat_id,'name':name,'text':text})

        if recv:
            #receivers.append({v['chat_id']+v['text']:v for v in recv}.values())
            receivers.extend(recv)

        cur.execute(f"SELECT A.CHAT_ID, A.NAME, B.KEYWORD, '{text}' text FROM USERS A, KEYWORDS B WHERE A.CHAT_ID = B.CHAT_ID AND INSTR(B.KEYWORD,':') = 0")
        columns = [column[0] for column in cur.description]
        results = cur.fetchall()
        results = list(dict(zip(columns, rows)) for rows in results)
        recv = []
        for index, r in enumerate(results):
            chat_id, name, keyword, text = r['chat_id'], r['name'], r['keyword'], r['text']

            if keyword in report_nm or keyword in corp_name:
                recv.append({'chat_id':chat_id,'name':name,'text':text})
        if recv:
            #receivers.append({v['chat_id']+v['text']:v for v in recv}.values())
            receivers.extend(recv)

    if receivers:
        receivers = {v['chat_id']+v['text']:v for v in receivers}.values()
        asyncio.run(main_async(receivers))

def send_telegram_bak(new_discs):
    receivers = []
    con = sqlite3.connect(DB_FOR_TELE)
    cur = con.cursor()

    for disc in new_discs:
        corp_name, report_nm, url = disc.corp.corp_name, disc.report_nm,disc.url
        label = corp_name + report_nm
        text = f'[{corp_name}] {report_nm}\n{url}'

        cur.execute(f"SELECT A.CHAT_ID, A.NAME, B.KEYWORD, '{text}' text FROM USERS A, KEYWORDS B WHERE A.CHAT_ID = B.CHAT_ID AND ('{corp_name}' LIKE '%'||B.KEYWORD||'%' OR '{report_nm}' LIKE '%'||B.KEYWORD||'%'")
        columns = [column[0] for column in cur.description]
        results = cur.fetchall()
        data = list(dict(zip(columns, rows)) for rows in results)

        for index, d in enumerate(data):
            if ':' in d['keyword']:
                code, key = d['keyword'].split(':')
                if corp_name != code:
                    data.delete(index)

        receivers.extend(data)

    asyncio.run(main_async(receivers))

