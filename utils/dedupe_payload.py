#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re, time, pymongo
from utils import load
from utils.load import _lang, _text
import subprocess
from telegram import ParseMode
from telegram.utils.request import Request as TGRequest
from telegram import Bot
from multiprocessing import Manager

myclient = pymongo.MongoClient(
    f"{load.cfg['database']['db_connect_method']}://{load.user}:{load.passwd}@{load.cfg['database']['db_addr']}",
    port=load.cfg["database"]["db_port"],
    connect=False,
)
mydb = myclient[load.cfg["database"]["db_name"]]
task_list = mydb["task_list"]
fav_col = mydb["fav_col"]

_cfg = load.cfg
deduping_process = subprocess.Popen

request = TGRequest(con_pool_size=8)
bot = Bot(token=f"{_cfg['tg']['token']}", request=request)

def dedupe_run(command):
    global deduping_process
    deduping_process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        encoding="utf-8",
        errors="ignore",
        universal_newlines=True,
    )
    while True:
        line = deduping_process.stdout.readline().rstrip()
        if not line:
            break
        yield line
    deduping_process.communicate()

def dedupe_task(
    ns,
    dedu_mode,
    dedu_chat_id,
    dedu_message_id,
    dedu_task_id,
    dedu_link,
    dedu_id,
    dedu_name,
):
    cloner = _cfg["general"]["cloner"]
    option = "dedupe"
    mode_suffix = "--dedupe-mode"
    mode = dedu_mode
    remote = _cfg["general"]["remote"]
    src_id = dedu_id
    src_block = remote + ":" + "{" + src_id + "}"
    checkers = "--checkers=" + f"{_cfg['general']['parallel_c']}"
    transfers = "--transfers=" + f"{_cfg['general']['parallel_t']}"
    flags = ["-P"]
    sa_sleep_suffix = "--drive-pacer-min-sleep"
    sa_sleep = _cfg["general"]["min_sleep"]

    command = [
        cloner,
        option,
        mode_suffix,
        mode,
        src_block,
        checkers,
        transfers,
        sa_sleep_suffix,
        sa_sleep,
    ]
    command += flags

    dedupe_process(ns, command, dedu_mode, dedu_chat_id, dedu_message_id, dedu_task_id, dedu_link, dedu_id, dedu_name)

    ns.dedupe = 0

def dedupe_process(ns, command, dedu_mode, dedu_chat_id, dedu_message_id, dedu_task_id, dedu_link, dedu_id, dedu_name):
    for output in dedupe_run(command):
        if ns.dedupe == 1:
            deduping_process.kill()

    if ns.dedupe == 0:
        last_dedupe_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if dedu_task_id == 0:
            fav_col.update_one(
                {"G_id": dedu_id}, {"$set": {"last_dedupe_time": last_dedupe_time,}},
            )

            deduped_msg = (
                " ༺ ✪iCopy✪ ༻ | " 
                + "🏳️"
                + " FAVORITES"
                + "\n\n" 
                + '<a href="{}">{}</a>'.format(dedu_link, dedu_name) 
                + "\n[" 
                + dedu_id 
                + "]\n\n" 
                + _text[_lang]["deduping_done"]
            )

        else:
            task_list.update_one(
                {"_id": int(dedu_task_id)}, {"$set": {"last_dedupe_time": last_dedupe_time,}},
            )

            deduped_msg = (
                " ༺ ✪iCopy✪ ༻ | " 
                + "🏳️" + _text[_lang]["current_task_id"] 
                + str(dedu_task_id) 
                + "\n\n" 
                + '<a href="{}">{}</a>'.format(dedu_link, dedu_name) 
                + "\n[" 
                + dedu_id 
                + "]\n\n" 
                + _text[_lang]["deduping_done"]
            )

        bot.edit_message_text(
            chat_id=dedu_chat_id,
            message_id=dedu_message_id,
            text=deduped_msg,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
    elif ns.dedupe == 1:
        bot.edit_message_text(
            chat_id=dedu_chat_id,
            message_id=dedu_message_id,
            text=_text[_lang]["is_killed_by_user"],
        )

