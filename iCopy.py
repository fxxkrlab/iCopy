import os, re, time
import logging, chardet
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
from process_bar import status

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

LINK_REPLY, TARGET_REPLY = range(2)
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
        "/copy 自定义目录转存 \n"
        "/pre1 预设转存目录1(未制作) \n"
        "/pre2 预设转存目录2(未制作) \n"
        "/backup 预设备份目录1(未制作) \n"
        "/dir 获取预设目录文件(未制作) \n"
    )


@restricted
def quick(update, context):
    update.message.reply_text(
       "您好 {} , 本次转存任务您选择了\n极速模式 ".format(update.message.from_user.first_name)
    )
    global mode
    mode = update.message.text.strip('/')

    return request_link(update, context)


@restricted
def copy(update, context):
    update.message.reply_text(
        "您好 {} , 本次转存任务您选择了\n自定义模式 ".format(update.message.from_user.first_name)
    )
    global mode
    mode = update.message.text.strip('/')

    return request_link(update, context)


def request_link(update, context):
    update.message.reply_text(
        "您好 {} , 请输入 Google Drive 分享链接 ".format(update.message.from_user.first_name)
    )

    return LINK_REPLY


def request_target(update, context):
    global mode
    global link
    link = update.message.text

    if "quick" == mode:
        return recived_mission(update, context)

    if "copy" == mode:
        update.message.reply_text(
            "您好 {} , 请输入任务目标文件夹链接 ".format(update.message.from_user.first_name)
        )

    return TARGET_REPLY


def recived_mission(update, context):
    global mode
    global link
    global target
    target = update.message.text
    
    lid = "".join(re.findall(regex, link))
    tid = "".join(re.findall(regex, target))
    foldername = (
        os.popen(
             """gclone lsf {}:{{{}}} --dump bodies -vv 2>&1 | grep '"{}","name"' | cut -d '"' -f 8""".format(
                settings.Remote, lid, lid
            )
        )
        .read()
        .rstrip()
    )

    if "quick" == mode:
        target_folder = (
            os.popen(
                """gclone lsf {}:{{{}}} --dump bodies -vv 2>&1 | grep '"{}","name"' | cut -d '"' -f 8""".format(
                    settings.Remote, settings.Pre_Dst_id, settings.Pre_Dst_id
                )
            )
            .read()
            .rstrip()
        )
        tid = settings.Pre_Dst_id
    elif "copy" == mode:
        target_folder = (
            os.popen(
                """gclone lsf {}:{{{}}} --dump bodies -vv 2>&1 | grep '"{}","name"' | cut -d '"' -f 8""".format(
                    settings.Remote, tid, tid
                )
            )
            .read()
            .rstrip()
        )

    update.message.reply_text(
        "┋资源名称┋:{} \n"
        "┋资源地址┋:{} \n"
        "┋转入位置┋:{}/{}"
        .format(foldername, lid, target_folder, foldername)
    )

    command = """gclone copy {}:{{{}}} {}:{{{}}}/"{}" {} {}""".format(
        settings.Remote,
        lid,
        settings.Remote,
        tid,
        foldername,
        settings.Run_Mode,
        settings.TRANSFER,
    )
    print(command)
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
        print(toutput.decode("utf-8", "ignore"))
        y = re.findall("^Transferred:", toutput.decode("utf-8", "ignore"))
        z = re.findall("^ * ", toutput.decode("utf-8", "ignore"))
        if y:
            val = str(toutput.decode("utf-8", "ignore"))
            val = val.split(",")
            percent = str(val[1])
            statu = val[1].replace("%", "")
            if statu != " -":
                statu = int(statu)
                prog = status(statu)

        if z:
            working = str(
                toutput.decode("utf-8", "ignore").lstrip("*  ").rsplit(":", 2)[0]
            )

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


def run(command):
    process = Popen(command, stdout=PIPE, shell=True)
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
        entry_points=[CommandHandler("quick", quick), CommandHandler("copy", copy)],
        states={
            LINK_REPLY: [MessageHandler(Filters.text, request_target),],
            TARGET_REPLY: [MessageHandler(Filters.text, recived_mission),],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler("help", help))

    dp.add_error_handler(error)

    updater.start_polling()
    logger.info("Fxxkr LAB iCopy Start")
    updater.idle()


if __name__ == "__main__":
    main()
