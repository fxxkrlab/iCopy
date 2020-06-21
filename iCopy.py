import time, logging, re, chardet
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
)
from telegram.ext.dispatcher import run_async
import utils
from utils import (
    folder_name,
    sendmsg,
    restricted,
    menu_keyboard,
    run,
    start_message,
    help_message,
    mode_message,
    task_message,
    cplt_message,
    pros_message,
    cron_task,
    killmission,
    kill_message,
    Mission_Done,
    Mission_kill,
)
from drive import drive_get
from threading import Timer, Thread
import settings
from process_bar import status


# ############################## Program Description ##############################
# Latest Modified DateTime : 202006220250 ,
# Version = '0.1.3-beta.2',
# Author : 'FxxkrLab',
# Website: 'https://bbs.jsu.net/c/official-project/icopy/6',
# Code_URL : 'https://github.com/fxxkrlab/iCopy',
# Description= 'Copy GoogleDrive Resources via Telegram BOT',
# Programming Language : Python3',
# License : MIT License',
# Operating System : Linux',
# ############################## Program Description.END ###########################


# ############################## logging ##############################

# Logging.basicConfig()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ############################## Global ##############################

# Conversation Stats
CHOOSE_MODE, LINK_REPLY, TARGET_REPLY = range(3)

# Regex
regex = r"[-\w]{11,}"


# ############################## Command ##############################

# START INFO & InlineKeyboard with Callback_query.data
@restricted
def start(update, context):
    update.effective_message.reply_text(
        start_message().format(update.effective_user.first_name),
        reply_markup=menu_keyboard(),
    )

    return CHOOSE_MODE


# HELP 帮助命令提示引导
@restricted
def help(update, context):
    update.effective_message.reply_text(help_message())


# ############################## Run_Modes ##############################

# QUICK Mode ,set mode = quick
@restricted
def quick(update, context):
    global mode
    mode = "quick"
    call_mode = update.effective_message.text

    if "/quick" == call_mode.strip()[:6]:
        update.effective_message.reply_text(
            mode_message().format(update.effective_user.first_name, "┋极速转存┋")
        )

        return request_link(update, context)

    if update.callback_query.data == "quick":
        update.callback_query.edit_message_text(
            mode_message().format(update.effective_user.first_name, "┋极速转存┋")
        )

        return request_link(update, context)


# COPY Mode ,set mode = copy
@restricted
def copy(update, context):
    global mode
    mode = "copy"
    call_mode = update.effective_message.text

    if "/copy" == call_mode.strip()[:5]:
        update.effective_message.reply_text(
            mode_message().format(update.effective_user.first_name, "┋自定义目录┋")
        )

        return request_link(update, context)

    if update.callback_query.data == "copy":
        update.callback_query.edit_message_text(
            mode_message().format(update.effective_user.first_name, "┋自定义目录┋")
        )

        return request_link(update, context)


# ############################## Run_Modes.END ##############################


# Error module
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# cancel function


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! {} , 欢迎再次使用 iCopy".format(update.message.from_user.first_name)
    )
    return ConversationHandler.END


# kill function


def kill(update, context):
    Thread(target=killmission).start()
    return cancel(update, context)


# ################################ Service #################################

# Request GoogleDrive Shared_Link
def request_link(update, context):
    update.effective_message.reply_text("请输入 Google Drive 分享链接")

    return LINK_REPLY


# Get Shared_link & request Target_Link
def request_target(update, context):
    global mode
    global link
    link = update.effective_message.text
    if "/cancel" == link.strip()[:7]:
        return cancel(update, context)

    if "quick" == mode:

        return recived_mission(update, context)

    if "copy" == mode:
        update.effective_message.reply_text("请输入转入目标文件夹链接 ")

    return TARGET_REPLY


# Get Target_Link(also include Shared_link) & run command judged from mode
def recived_mission(update, context):
    global mode
    global link
    global target
    target = update.effective_message.text
    if "/cancel" == target.strip()[:7]:
        return cancel(update, context)

    # extract lid,tid from Link(shared & Target)
    lid = "".join(re.findall(regex, link))
    tid = "".join(re.findall(regex, target))

    # extract Shared_Link folderName
    if len(lid) == 28 or len(lid) == 33:
        foldername = folder_name(settings.Remote, lid, lid)
    elif len(lid) != 28 and len(lid) != 33:
        d_id = lid
        foldername = drive_get(d_id)

    # get Target_folderName under quick mode
    if "quick" == mode:
        # tid = Pre_Dst_id under quick mode
        tid = settings.Pre_Dst_id
        if len(tid) == 28 or len(tid) == 33:
            target_folder = folder_name(settings.Remote, tid, tid)
        elif len(tid) != 28 and len(tid) != 33:
            d_id = tid
            target_folder = drive_get(d_id)

    # get Target_folderName under copy mode
    elif "copy" == mode:
        if len(tid) == 28 or len(tid) == 33:
            target_folder = folder_name(settings.Remote, tid, tid)
        elif len(tid) != 28 and len(tid) != 33:
            d_id = tid
            target_folder = drive_get(d_id)

    # sendmsg Mission.INFO
    update.effective_message.reply_text(
        task_message().format(foldername, lid, target_folder, foldername)
    )

    # Build Mission Command
    global command
    commandstr = """gclonejsusplitcopyjsusplit{}:{{{}}}jsusplit{}:{{{}}}/{}jsusplit{}jsusplit{}""".format(
        settings.Remote,
        lid,
        settings.Remote,
        tid,
        foldername,
        settings.Run_Mode,
        settings.TRANSFER,
    )

    command = commandstr.split("jsusplit")
    print(command)

    return ConversationHandler.END, copyprocess(update, context, command)


# 任务信息读取处理，并通过异步进程发送 BOT 界面滚动更新信息
@run_async
def copyprocess(update, context, command):
    bot = context.bot
    message = update.effective_message.reply_text("转存任务准备中...")
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
                cron_task(
                    sendmsg,
                    bot,
                    message.chat_id,
                    mid,
                    pros_message(),
                    percent,
                    prog,
                    working,
                )
                percent1 = percent
                working1 = working
                xtime = time.time()

    # Fix Mission INFO
    if utils.Mission_Done == "finished":
        if utils.Mission_kill != "killed":
            percent = "100%"
            prog = status(100)
            cron_task(
                sendmsg, bot, message.chat_id, mid, cplt_message(), percent, prog, ""
            )
            utils.Mission_Done = ""

            return help(update, context)

        elif utils.Mission_kill == "killed":
            percent = "0%"
            prog = status(0)
            working = "本次转存任务已取消"
            cron_task(
                sendmsg,
                bot,
                message.chat_id,
                mid,
                kill_message(),
                percent,
                prog,
                working,
            )
            utils.Mission_Done = ""
            utils.Mission_kill = ""

            return help(update, context)


# ############################### Main ####################################


def main():
    updater = Updater(settings.TOKEN, use_context=True,)

    dp = updater.dispatcher

    # Entry Conversation
    conv_handler = ConversationHandler(
        entry_points=[
            # Entry Points
            CommandHandler("start", start),
            CommandHandler("quick", quick),
            CommandHandler("copy", copy),
        ],
        states={
            CHOOSE_MODE: [
                # call function which judged via pattern
                CallbackQueryHandler(quick, pattern="quick"),
                CallbackQueryHandler(copy, pattern="copy"),
            ],
            LINK_REPLY: [
                # get Shared_Link states
                CallbackQueryHandler(request_target),
                MessageHandler(Filters.text, request_target),
            ],
            TARGET_REPLY: [
                # get Target_Link states
                CallbackQueryHandler(recived_mission),
                MessageHandler(Filters.text, recived_mission),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel),],
    )

    dp.add_handler(CommandHandler("kill", kill), 1)

    dp.add_handler(conv_handler, 2)

    dp.add_handler(CommandHandler("help", help))

    dp.add_error_handler(error)

    updater.start_polling()
    logger.info("Fxxkr LAB iCopy Start")
    updater.idle()


if __name__ == "__main__":
    main()
