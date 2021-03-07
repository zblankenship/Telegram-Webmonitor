import os
import logging
import random
import pymongo
import datetime
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

#boring boiler plate stuff
add_dict = {}
load_dotenv('key.env')
token = os.getenv('token')
mongo = os.getenv('mongo')
myclient = os.getenv('myclient')
updater = Updater(token = token, use_context = True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#end boring boiler plate stuff

myclient = pymongo.MongoClient(mongo)
mydb = myclient["webmonitor"]
mycol = mydb["websites"]

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Paste the URL of a website you want to monitor")

def new_url(update, context):
    url = update.message.text
    mycol = mydb[url]
    chat_id=update.effective_chat.id
    username = update.message.chat.username
    add_to_db(url,chat_id,username)
    add_to_head_collection(url)

    #context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def add_to_db(url,chat_id,username):
    mycol = mydb[url]
    date = datetime.datetime.now()
    date = date.strftime("%x")
    time = datetime.datetime.now()
    time = time.strftime("%X")
    add_dict = { "url": url, "chats_id_to_notify": chat_id, "username": username, "date_added": date, "time_added": time}
    x = mycol.insert_one(add_dict)

def add_to_head_collection(url):
    headcol = mydb["websites"]
    date = datetime.datetime.now()
    date = date.strftime("%x")
    time = datetime.datetime.now()
    time = time.strftime("%X")
    head_dict = { "url": url, "time": "", "date_added": date, "time_added": time, "time_last_checked": datetime.datetime.now()}
    x = headcol.insert_one(head_dict)    



new_url_handler = MessageHandler(Filters.text & (~Filters.command), new_url)
start_handler = CommandHandler('start', start)

dispatcher.add_handler(new_url_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()