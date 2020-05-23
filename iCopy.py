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
            update.message.reply_text('Hi {} 您好'.format(update.message.from_user.first_name))
            update.message.reply_text('您的用户ID:{} 未经授权\n请联系管理员'.format(update.message.from_user.id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped

#start
@restricted
def start(update, context):
    update.message.reply_text('Hi! {} 欢迎使用 iCopy\n'.format(update.message.from_user.first_name))
    update.message.reply_text('Fxxkr LAB 出品必属极品\n'
        '请输入 /help 查询使用命令')

#error handler
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

@restricted
def help(update, context):
	update.message.reply_text('/help - 查询使用命令 \n'
	'/quick Google Drive 极速转存 \n'
	'/copy 自定义目录转存 \n'
	'/pre1 预设转存目录1 \n'
	'/pre2 预设转存目录2 \n'
	'/backup 预设备份目录1 \n'
	'/dir 获取预设目录文件 \n')

'''
#ReplyKB + 开始列表
@restricted
def start(update, context):
    menu_keyboard = [['极速转存', '自定义转存', '全盘备份']]
    menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True)
    update.message.reply_text('Hi! 欢迎使用 iCopy\n'
        'Fxxkr LAB 出品必属极品', reply_markup=menu_markup)

#InlineKB + 开始列表
@restricted
def start(update, context):
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton('极速转存', callback_data='quick'),
        InlineKeyboardButton('自定义转存', callback_data='customize'),
        InlineKeyboardButton('全盘备份', callback_data='backup')]])
    update.message.reply_text('Hi! 欢迎使用 iCopy\n'
        'Fxxkr LAB 出品必属极品\n'
        '请选择 Google Drive 模式转存模式',reply_markup = reply_markup)

def select_menu(update, context):
    if update.callback_query.data == 'quick':
        update.callback_query.edit_message_text('您选择了极速转存模式')
    if update.callback_query.data == 'customize':
        update.callback_query.edit_message_text('自定义转存')
    if update.callback_query.data == 'backup':
        update.callback_query.edit_message_text('全盘备份')


def button_callback(update, context):
    if update.callback_query.data == 'quick':
        quick(update, context)
'''

@restricted
def quick(update, context):
    update.message.reply_text('示例运行 gclone')
    command = "".join(settings.QUICK_SET)
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
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("quick", quick))
    #dp.add_handler(CallbackQueryHandler(button_callback))

    dp.add_error_handler(error)
    updater.start_polling()
    logger.info('Fxxkr LAB iCopy Start')
    updater.idle()


if __name__ == '__main__':
    main()