from time import time
from urllib.request import Request, urlopen
import asyncio

import telegram
chat_id = '442047336'
TOKEN_FOR_TELE = '676500333:AAEn9gLG67aLCRa_U8-n4HqVR_2Lv0zD140'
DB_FOR_TELE= "../../Telegram/Dart/dart.db"
bot = telegram.Bot(token = TOKEN_FOR_TELE)


""" 
urls = ['https://www.google.co.kr/search?q=' + i
    for i in ['apple', 'pear', 'grape', 'pineapple', 'orange', 'strawberry']]
 
async def fetch(url):
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})    # UA가 없으면 403 에러 발생
    response = await loop.run_in_executor(None, urlopen, request)    # run_in_executor 사용
    page = await loop.run_in_executor(None, response.read)           # run in executor 사용
    return len(page)
 
async def main():
    futures = [asyncio.ensure_future(fetch(url)) for url in urls]
                                                           # 태스크(퓨처) 객체를 리스트로 만듦
    result = await asyncio.gather(*futures)                # 결과를 한꺼번에 가져옴
    print(result)
 
begin = time()
loop = asyncio.get_event_loop()          # 이벤트 루프를 얻음
loop.run_until_complete(main())          # main이 끝날 때까지 기다림
loop.close()                             # 이벤트 루프를 닫음
end = time()
print('실행 시간: {0:.3f}초'.format(end - begin))



def ss(i):
    bot.sendMessage(chat_id=chat_id, text=f'text async {i}')

async def do_async(i):
    print('do_async', i)
    loop.run_in_executor(None, ss, i)
    print('send 완료', i)
    return i

async def main2():
    futures = [asyncio.ensure_future(do_async(i)) for i in range(1,5)]
    result = await asyncio.gather(*futures) 

begin = time()
loop = asyncio.get_event_loop()          # 이벤트 루프를 얻음
loop.run_until_complete(main2())          # main이 끝날 때까지 기다림
#loop.close()                             # 이벤트 루프를 닫음
end = time()
print('실행 시간: {0:.3f}초'.format(end - begin))


"""
async def do_async(l):
    print('do_async')
    chat_id = l['CHAT_ID']
    text  = l['TEXT']
    loop.run_in_executor(None, bot.sendMessage, chat_id, text)
    print('send 완료')

async def main2(ll):
    futures = [asyncio.ensure_future(do_async(l)) for l in ll]
    result = await asyncio.gather(*futures)



ll = [{'CHAT_ID':chat_id, 'TEXT':f'TEXT {i}'} for i in range(1,10)]

loop = asyncio.get_event_loop()          # 이벤트 루프를 얻음
loop.run_until_complete(main2(ll))
"""


import asyncio

async def factorial(name, number):
    f = 1
   for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f

async def main():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
            [do_async({'chat_id':chat_id, 'text':f'TEXT {i}'}) in range(1,10)]
        )
    print(L)

asyncio.run(main())




con = sqlite3.connect(DB_FOR_TELE)
cur = con.cursor()

corp_name = '삼성전자'
report_nm = '배당'
url = 'uuu'
label = corp_name + report_nm
text = f'[{corp_name}] {report_nm}\n{url}'

cur.execute(f"SELECT A.CHAT_ID, A.NAME, B.KEYWORD, '{text}' text FROM USERS A, KEYWORDS B WHERE A.CHAT_ID = B.CHAT_ID AND ('{corp_name}' LIKE '%'||B.KEYWORD||'%' OR '{report_nm}' LIKE '%'||B.KEYWORD||'%')")

columns = [column[0] for column in cur.description]
results = cur.fetchall()
data = list(dict(zip(columns, rows)) for rows in results)



for index, d in enumerate(data):
    keyword = d['keyword']
    if ':' in keyword:
        code, key = keyword.split(':')
        if corp_name != code:
            data.delete(index)
    else:
        i corp_name in:


