import os
import logging
import random
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

#boring boiler plate stuff
load_dotenv('key.env')
token = os.getenv('token')
updater = Updater(token = token, use_context = True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#end boring boiler plate stuff

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Paste the URL of a website you want to monitor")

def new_url(update, context):
    url = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


new_url_handler = MessageHandler(Filters.text & (~Filters.command), new_url)
start_handler = CommandHandler('start', start)

dispatcher.add_handler(new_url_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()