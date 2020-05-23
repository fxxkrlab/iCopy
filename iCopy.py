import logging
import time
import os
import re
from functools import wraps
import chardet
from datetime import date
from subprocess import Popen, PIPE 
from datetime import date
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

#用户限制
def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in settings.ENABLED_USERS:
            print(f"Unauthorized access denied for {user_id}.")
            update.message.reply_text('您的账号未经授权 请联系管理员')
            return
        return func(update, context, *args, **kwargs)
    return wrapped

#开始列表
@restricted
def start(update, context):
    menu_keyboard = [['极速转存', '自定义转存', '全盘备份']]
    menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True)
    update.message.reply_text('Hi! 欢迎使用 iCopy\n'
        'Fxxkr LAB 出品必属极品', reply_markup=menu_markup)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


@restricted
def list(update, context):
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton('极速转存', callback_data='quick'),
        InlineKeyboardButton('自定义转存', callback_data='customize'),
        InlineKeyboardButton('全盘备份', callback_data='backup')]])
    update.message.reply_text('请选择 Google Drive 模式转存模式\n',reply_markup = reply_markup)

@restricted
def select_menu(update, context):
    if update.callback_query.data == 'quick':
        update.callback_query.edit_message_text('您选择了极速转存模式')
    if update.callback_query.data == 'customize':
        update.callback_query.edit_message_text('自定义转存')
    if update.callback_query.data == 'backup':
        update.callback_query.edit_message_text('全盘备份')
@restricted
def quick(update, context):
    update.message.reply_text('示例运行 gclone')
    txt="这里输入 gclone copy 命令"
    command = "".join(txt)
    copyprocess(update, context, command)

def copyprocess(update, context, command):
    bot = context.bot
    message=update.message.reply_text("STATUS")
    mid=message.message_id
    percent=""
    percent1=""
    working=""
    working1=""
    prog=""
    for toutput in run(command):
        print(toutput.decode("utf-8", "ignore"))
        y= re.findall("^Transferred:", toutput.decode("utf-8", "ignore"))
        z= re.findall("^ * ", toutput.decode("utf-8", "ignore"))
        if (y):
            val=str(toutput.decode("utf-8", "ignore"))
            val=val.split(",")
            percent=str(val[1])
            statu=val[1].replace("%","")
            if statu != " -":
                statu=int(statu)
                prog=status(statu)

        if (z):
            working=str(toutput.decode("utf-8", "ignore"))

        if working1 != working or percent1 != percent :
            bot.edit_message_text(chat_id=message.chat_id,message_id=mid,text="{} \n {} \n {}".format(percent,prog,working))
            percent1=percent
            working1=working

def status(val):
    if val<10 :
        ss= "[                         ]"

    if val>=10 and val<=19:
        ss= "[#                      ]"

    if val>=20 and val<=29:
        ss= "[##                    ]"

    if val>=30 and val<=39:
        ss= "[###                 ]"

    if val>=40 and val<=49:
        ss= "[####               ]"
        
    if val>=50 and val<=59:
        ss= "[#####            ]"

    if val>=60 and val<=69:
        ss= "[######          ]"

    if val>=70 and val<=79:
        ss= "[#######       ]"

    if val>=80 and val<=89:
        ss= "[########     ]"
        
    if val>=90 and val<=99:
        ss= "[#########  ]"
        
    if val==100:
        ss= "[##########]"
    return ss
    
def run(command):
    process = Popen(command,stdout=PIPE,shell=True)
    while True:
        line=process.stdout.readline().rstrip()
        if not line:
            break
        yield line

def main():
    updater = Updater(
        settings.TOKEN, use_context=True,
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("list", list))
    dp.add_handler(CommandHandler("quick", quick))
    dp.add_handler(CallbackQueryHandler(select_menu))

    dp.add_error_handler(error)
    updater.start_polling()
    logger.info('Fxxkr LAB iCopy Start')
    updater.idle()


if __name__ == '__main__':
    main()