import os
import sys
import time
from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TimedOut
from telegram.error import Unauthorized
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from pymongo import ASCENDING, DESCENDING
from pymongo.operations import IndexModel
from pymodm import MongoModel, EmbeddedMongoModel, fields, connect

connect('mongodb://localhost:27017/watchdog')

class User(MongoModel):
    chat_id   = fields.CharField()
    name      = fields.CharField()
    join_date = fields.CharField()
    send_date = fields.CharField()

    def __init__(self, chat_id=None, name=None, **kwargs):
        super().__init__(**kwargs)
        self.chat_id   = chat_id
        self.name      = name
        self.join_date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        self.send_date = '0000/00/00'

@run_async
def send_message(bot, chat_id, name, message):
    print('--- send', chat_id, name, message[:10])
    try:
        bot.send_message(chat_id=chat_id, text=message)
        user = User.objects.get({'chat_id':str(chat_id)})
        user.send_date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        user.save()

    except TimedOut as ex_to:
        print('@@@ error, ex_to', ex_to)
        try:
            bot.send_message(chat_id=chat_id, text=message, timeout=60)
        except Exception as ex1:
            print('@@@ error ex1', ex1)
    except Unauthorized as ex_ua:
        print('@@@ error, ex_ua', ex_ua, chat_id)
    except Exception as ex2:
        print('@@@ error, ex2', chat_id, ex2)

def callback_connect(bot, job):
    if 7 <= int(datetime.now().strftime('%H')) < 22:
        pass
    else:
        return

    ret = os.system('./connect_test.sh')
    if ret == 0:
        return

    users = User.objects.all()
    for user in users:
        send_message(bot, user.chat_id, user.name, 'pair 연결이 끊겼습니다.')

def get_message(bot, update, job_queue):
    chat_id = update.message.chat.id
    name = update.message.chat.last_name + update.message.chat.first_name
    text = update.message.text

    try:
        user = User.objects.get({'chat_id':str(chat_id)})
    except Exception as ex2:
        print('except 1', ex2)
        User(chat_id, name).save()
    print('get_message', chat_id, name, text)


if __name__ == "__main__":
    my_token = '1135014060:AAHbWAEjYjERztEJyS29oGPeJAkcLp9X9Ro'
    updater = Updater(my_token)

    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_message, pass_job_queue=True))

    j = updater.job_queue
    job_minute = j.run_repeating(callback_connect, interval=60 * 60, first=0)

    updater.start_polling()
    updater.idle()
