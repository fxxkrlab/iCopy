import os, requests, json, logging
from functools import wraps
from subprocess import Popen, PIPE
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
import settings
from threading import Timer

# ############################## Program Description ##############################
# Author : 'FxxkrLab',
# Website: 'https://bbs.jsu.net/c/official-project/icopy/6',
# Code_URL : 'https://github.com/fxxkrlab/iCopy',
# Description= 'Copy GoogleDrive Resources via Telegram BOT',
# Programming Language : Python3',
# License : MIT License',
# Operating System : Linux',
# ############################## Program Description.END ###########################

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Mission is finished Judged via Mission_Done and Mission_kill
Mission_Done = ""
Mission_kill = ""


# ############################## Global AUTH ##############################

# 全局权限约束
def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = str(update.effective_user.id)
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


# ############################## sendMsg_BOX ##############################

# BOT界面信息滚动更新模块
def sendmsg(bot, chat_id, mid, context):
    bot.edit_message_text(chat_id=chat_id, message_id=mid, text=context),

# Cron task
def cron_task(sendmsg,bot,chat_id,mid,info,percent,fps,prog,working):
    Timer(
        0,
        sendmsg,
        args=(
            bot,
            chat_id,
            mid,
            info.format(
                percent, fps, prog, working,
            ),
        ),
    ).start()

# ############################## sendMsg_BOX.END ##############################


# 资源名获取
def folder_name(remote, lid, tid):
    f_name = (
        os.popen(
            """{} lsf {}:{{{}}} --dump bodies -vv 2>&1 | grep '"{}","name"' | cut -d '"' -f 8"""
                .format(settings.Clone, remote, lid, lid)
        ).read().rstrip()
    )
    return f_name


# InlineKeyBoard
def menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("极速转存", callback_data="quick"),
            InlineKeyboardButton("自定义模式", callback_data="copy"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# run(command) subprocess.popen --> line --> stdout
def run(command):
    global Mission_Done
    global icopyprocess
    icopyprocess = Popen(command, stdout=PIPE, shell=False)
    while True:
        line = icopyprocess.stdout.readline().rstrip()
        if not line:
            if icopyprocess.poll() == 0 or icopyprocess.poll() == -9:
                Mission_Done = "finished"
            break
        yield line

def killmission():
    global Mission_kill
    global icopyprocess
    icopyprocess.kill()
    Mission_kill = "killed"

def _get_ver():
    _url = "https://api.github.com/repos/fxxkrlab/iCopy/releases"
    _r_ver = requests.get(_url).json()
    _latest_ver = _r_ver[0]["tag_name"]
    return _latest_ver

# ############################## Message ##############################
def start_message():
    return "Hi! {} 欢迎使用 iCopy\nFxxkr LAB 出品必属极品\n请选择 Google Drive 模式转存模式"


def help_message():
    return ("/start - 开始菜单 \n"
            "/help - 帮助菜单 \n"
            "/quick - 极速转存 \n"
            "/copy - 自定义转存 \n"
            "/cancel - 任务未开始前取消 \n"
            "/kill - 任务进行中取消 \n"
            "/ver - 查询版本号 \n")


def mode_message():
    return "您好 {} , 本次转存任务您选择了\n{}模式 "


def task_message():
    return ("▣▣▣▣▣▣▣▣任务信息▣▣▣▣▣▣▣▣\n"
            "┋资源名称┋:\n"
            "┋•{} \n"
            "┋资源地址┋:\n"
            "┋•{} \n"
            "┋转入位置┋:\n"
            "┋•{}/{}")


def pros_message():
    return "▣▣▣▣▣▣▣正在执行转存▣▣▣▣▣▣▣ \n {} {}\n {} \n {} \n "


def cplt_message():
    return ("▣▣▣▣▣▣▣转存任务完成▣▣▣▣▣▣▣ \n {} {}\n {} \n{} \n "
            "本次转存任务已完成 \n"
            "跳转至帮助(HELP)命令 \n")

def kill_message():
    return "✖✖✖✖✖任务已被取消✖✖✖✖✖\n{} \n {} \n {} \n "

def kill_message_info():
    return ("\n"
            "•  本次转存任务已取消\n")

def drive_select_message():
    return "请选择目标团队盘 \n"

