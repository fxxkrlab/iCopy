import logging
import time
import os
import re
from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup

import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    menu_keyboard = [['极速转存'], ['自定义转存']]
    menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True)
    update.message.reply_text('Hi! 欢迎使用 iCopy\n'
        'Fxxkr LAB 出品必属极品', reply_markup=menu_markup)
    
def main():
    updater = Updater(
        settings.TOKEN, use_context=True,
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    logger.info('Fxxkr LAB iCopy Start')
    updater.idle()


if __name__ == '__main__':
    main()