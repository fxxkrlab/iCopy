import logging
import time
import os
import re
import chardet
from datetime import date
from subprocess import Popen, PIPE 
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
def list(update, context):
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton('极速转存', callback_data='quick'),
        InlineKeyboardButton('自定义转存', callback_data='customize'),
        InlineKeyboardButton('全盘备份', callback_data='backup')]])
    update.message.reply_text('请选择 Google Drive 模式转存模式\n',reply_markup = reply_markup)

#按钮点击行为更换 if 下一行的内容
def select_menu(update, context):
    if update.callback_query.data == 'quick':
        update.callback_query.edit_message_text('您选择了极速转存模式')
    if update.callback_query.data == 'customize':
        update.callback_query.edit_message_text('自定义转存')
    if update.callback_query.data == 'backup':
        update.callback_query.edit_message_text('全盘备份')

def quick(update, context):
    update.message.reply_text('示例运行 gclone lsf')
    txt = "gclone copy gc:{15y-hKqsOvoh3eqUuVlbLsWUXbIweKr__} gc:{1vPsJutJHthzHqbpTzARRCSzA1IxjlZA1} --drive-server-side-across-configs -vvP --ignore-existing --transfers 40 --tpslimit 40"
    command = "".join(txt)
    process(update, context, command)


def process(update, context, command):
    bot = context.bot
    message=update.message.reply_text("STATUS")
    mid=message.message_id
    percent=""
    percent1=""
    working=""
    working1=""
    prog=""
    for toutput in run(command):
        print(toutput)
        y= re.findall("^Transferred:", toutput)
        z= re.findall("^ * ", toutput)
        if (y):
            val=str(toutput)
            val=val.split(",")
            percent=str(val[1])
            statu=val[1].replace("%","")
            if statu != " -":
                statu=int(statu)
                prog=status(statu)

        if (z):
            working=str(toutput)

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
    process=Popen(command,stdout=PIPE,shell=True)
    while True:
        line=process.stdout.readline().rstrip()
        if not line:
            break
        yield line

#增加命令请在下方增加对应的 Handler "" 中为命令 ,后为 def 函数名
def main():
    updater = Updater(
        settings.TOKEN, use_context=True,
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("list", list))
    dp.add_handler(CommandHandler("quick", quick))
    dp.add_handler(CallbackQueryHandler(select_menu))
    updater.start_polling()
    logger.info('Fxxkr LAB iCopy Start')
    updater.idle()


if __name__ == '__main__':
    main()