import logging
import time
import os
import re
from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, Message

import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

#开始列表
def start(update, context):
    menu_keyboard = [['极速转存', '自定义转存', '全盘备份']]
    menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True)
    update.message.reply_text('Hi! 欢迎使用 iCopy\n'
        'Fxxkr LAB 出品必属极品', reply_markup=menu_markup)

#按钮列表
def menu_list(update, context):
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton('极速转存', callback_data='quick'),
        InlineKeyboardButton('自定义转存', callback_data='customize'),
        InlineKeyboardButton('全盘备份', callback_data='backup')]])
    update.message.reply_text('请选择模式\n',reply_markup = reply_markup)

#按钮点击行为更换 if 下一行的内容
def select_menu(update, context):
    if update.callback_query.data == 'quick':
        update.callback_query.edit_message_text('极速转存')
    if update.callback_query.data == 'customize':
        update.callback_query.edit_message_text('自定义转存')
    if update.callback_query.data == 'backup':
        update.callback_query.edit_message_text('全盘备份')

#增加命令请在下方增加对应的 Handler "" 中为命令 ,后为 def 函数名
def main():
    updater = Updater(
        settings.TOKEN, use_context=True,
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menulist", menu_list))
    dp.add_handler(CallbackQueryHandler(select_menu))
    updater.start_polling()
    logger.info('Fxxkr LAB iCopy Start')
    updater.idle()


if __name__ == '__main__':
    main()