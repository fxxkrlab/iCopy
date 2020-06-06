import os, re, time
import logging
from functools import wraps
from datetime import date
from subprocess import Popen, PIPE
from telegram import Message
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
)
from threading import Timer

import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TYPING_REPLY = range(1)
regex = r"[-\w]{11,}"


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in settings.ENABLED_USERS:
            print(f"Unauthorized access denied for {user_id}.")
            update.message.reply_text(
                "Hi {} 您好".format(update.message.from_user.first_name)
            )
            update.message.reply_text(
                "您的用户ID:{} 未经授权\n请联系管理员".format(update.message.from_user.id)
            )
            return
        return func(update, context, *args, **kwargs)

    return wrapped


@restricted
def start(update, context):
    update.message.reply_text(
        "Hi! {} 欢迎使用 iCopy\n".format(update.message.from_user.first_name)
    )
    update.message.reply_text("Fxxkr LAB 出品必属极品\n" "请输入 /help 查询使用命令")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


@restricted
def help(update, context):
    update.message.reply_text(
        "/help - 查询使用命令 \n"
        "/quick Google Drive 极速转存 \n"
        "/copy 自定义目录转存(未制作) \n"
        "/pre1 预设转存目录1(未制作) \n"
        "/pre2 预设转存目录2(未制作) \n"
        "/backup 预设备份目录1(未制作) \n"
        "/dir 获取预设目录文件(未制作) \n"
    )


@restricted
def quick(update, context):
    update.message.reply_text(
        "您好 {} , 请输入 Google Drive 分享链接 ".format(update.message.from_user.first_name)
    )

    return TYPING_REPLY


def recived_link(update, context):
    link = update.message.text
    if "drive.google.com" in link:
        lid = "".join(re.findall(regex, link))
        foldername = (
            os.popen(
                """gclone lsf gc:{{{}}} --dump bodies -vv 2>&1 | grep '"{}","name"' | cut -d '"' -f 8""".format(
                    lid, lid
                )
            )
            .read()
            .rstrip()
        )
    pre_foldername = (
        os.popen(
            """gclone lsf gc:{{{}}} --dump bodies -vv 2>&1 | grep '"{}","name"' | cut -d '"' -f 8""".format(
                settings.Pre_Dst_id, settings.Pre_Dst_id
            )
        )
        .read()
        .rstrip()
    )
    update.message.reply_text(
        "分享文件夹为 : {} \n"
        "Folder id 为 : {} \n"
        "分享内容转存至 \n"
        "{} 预设目录中的 {} 文件夹内".format(foldername, lid, pre_foldername, foldername)
    )
    command = """gclone copy {}:{{{}}} {}:{{{}}}/"{}" {} {}""".format(
        settings.Remote,
        lid,
        settings.Remote,
        settings.Pre_Dst_id,
        foldername,
        settings.Run_Mode,
        settings.TRANSFER,
    )
    copyprocess(update, context, command)

    return ConversationHandler.END


def sendmsg(bot, chat_id, mid, context):

    bot.edit_message_text(chat_id=chat_id, message_id=mid, text=context)


def copyprocess(update, context, command):
    bot = context.bot
    message = update.message.reply_text("开始转存文件")
    mid = message.message_id
    percent = ""
    percent1 = ""
    working = ""
    working1 = ""
    prog = ""
    timeout = 0.1
    xtime = 0
    for toutput in run(command):
        print(toutput)
        y = re.findall("^Transferred:", toutput)
        z = re.findall("^ * ", toutput)
        if y:
            val = str(toutput)
            val = val.split(",")
            percent = str(val[1])
            statu = val[1].replace("%", "")
            if statu != " -":
                statu = int(statu)
                prog = status(statu)

        if z:
            working = str(toutput.lstrip("*  ").rsplit(":", 2)[0])

        if working1 != working or percent1 != percent:
            if int(time.time()) - xtime > timeout:
                Timer(
                    0,
                    sendmsg,
                    args=(
                        bot,
                        message.chat_id,
                        mid,
                        "正在执行转存 \n {} \n {} \n {} \n ".format(percent, prog, working),
                    ),
                ).start()
                percent1 = percent
                working1 = working
                xtime = time.time()


def status(val):
    if val < 10:
        ss = "[                         ]"

    if val >= 10 and val <= 19:
        ss = "[▇                      ]"

    if val >= 20 and val <= 29:
        ss = "[▇▇                    ]"

    if val >= 30 and val <= 39:
        ss = "[▇▇▇                 ]"

    if val >= 40 and val <= 49:
        ss = "[▇▇▇▇               ]"

    if val >= 50 and val <= 59:
        ss = "[▇▇▇▇▇            ]"

    if val >= 60 and val <= 69:
        ss = "[▇▇▇▇▇▇          ]"

    if val >= 70 and val <= 79:
        ss = "[▇▇▇▇▇▇▇      ]"

    if val >= 80 and val <= 89:
        ss = "[▇▇▇▇▇▇▇▇     ]"

    if val >= 90 and val <= 99:
        ss = "[▇▇▇▇▇▇▇▇▇  ]"

    if val == 100:
        ss = "[▇▇▇▇▇▇▇▇▇▇]"
    return ss


def run(command):
    process = Popen(
        command, stdout=PIPE, shell=True, bufsize=1, universal_newlines=True
    )
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! {} , 欢迎再次使用 iCopy".format(update.message.from_user.first_name)
    )

    return ConversationHandler.END


def main():
    updater = Updater(settings.TOKEN, use_context=True,)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("quick", quick)],
        states={TYPING_REPLY: [MessageHandler(Filters.text, recived_link),],},
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler("help", help))

    dp.add_error_handler(error)

    updater.start_polling()
    logger.info("Fxxkr LAB iCopy Start")
    updater.idle()


if __name__ == "__main__":
    main()
