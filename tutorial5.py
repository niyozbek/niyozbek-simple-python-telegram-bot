# python wrapper to work with official telegram bot api
#references
#https://github.com/python-telegram-bot/python-telegram-bot
#https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import os

load_dotenv()
updater = Updater(token=os.environ.get('YOURAPIKEY'), use_context=True)

dispatcher = updater.dispatcher
#not needed
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please talk to me, do not stop me!")

stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)

def echo(update, context):
    if(update.message.text == 'Hi'):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi {update.effective_chat.first_name}!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
#updater.stop()