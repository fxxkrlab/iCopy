import os
from functools import wraps
from subprocess import Popen, PIPE
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
import settings
from threading import Timer

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


# Mission is finished Judged via Mission_Done and Mission_kill
Mission_Done = ""
Mission_kill = ""


# ############################## Global AUTH ##############################

# 全局权限约束
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


# ############################## sendMsg_BOX ##############################

# BOT界面信息滚动更新模块
def sendmsg(bot, chat_id, mid, context):
    bot.edit_message_text(chat_id=chat_id, message_id=mid, text=context),

# Cron task
def cron_task(sendmsg,bot,chat_id,mid,info,percent,prog,working):
    Timer(
        0,
        sendmsg,
        args=(
            bot,
            chat_id,
            mid,
            info.format(
                percent, prog, working,
            ),
        ),
    ).start()

# ############################## sendMsg_BOX.END ##############################


# 资源名获取
def folder_name(remote, lid, tid):
    f_name = (
        os.popen(
            """gclone lsf {}:{{{}}} --dump bodies -vv 2>&1 | grep '"{}","name"' | cut -d '"' -f 8"""
                .format(remote, lid, lid)
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
            Mission_Done = "finished"
            break
        yield line

def killmission():
    global Mission_kill
    global icopyprocess
    icopyprocess.kill()
    Mission_kill = "killed"



# ############################## Message ##############################
def start_message():
    return "Hi! {} 欢迎使用 iCopy\nFxxkr LAB 出品必属极品\n请选择 Google Drive 模式转存模式"


def help_message():
    return ("/start - 开始菜单 \n"
            "/help - 帮助菜单 \n"
            "/quick - 极速转存 \n"
            "/copy - 自定义转存 \n"
            "/cancel - 任务未开始前取消 \n"
            "/kill - 任务进行中取消 \n")


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
    return "▣▣▣▣▣▣▣正在执行转存▣▣▣▣▣▣▣ \n {} \n {} \n {} \n "


def cplt_message():
    return ("▣▣▣▣▣▣▣转存任务完成▣▣▣▣▣▣▣ \n {} \n {} \n{} \n "
            "本次转存任务已完成 \n"
            "跳转至开始(START)命令 \n")


def kill_message():
    return "✖✖✖✖✖✖任务已被取消✖✖✖✖✖✖ \n {} \n {} \n {} \n "

