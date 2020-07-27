#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re, time, pymongo
from utils import load
from utils.load import _lang, _text
import subprocess
from telegram.utils.request import Request as TGRequest
from telegram import Bot
from threading import Thread
from multiprocessing import Manager

myclient = pymongo.MongoClient(
    f"{load.cfg['database']['db_connect_method']}://{load.user}:{load.passwd}@{load.cfg['database']['db_addr']}",
    port=load.cfg["database"]["db_port"],
    connect=False,
)
mydb = myclient[load.cfg["database"]["db_name"]]
fav_col = mydb["fav_col"]

_cfg = load.cfg
purging_process = subprocess.Popen

request = TGRequest(con_pool_size=8)
bot = Bot(token=f"{_cfg['tg']['token']}", request=request)

def purge_run(command):
    global purging_process
    purging_process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        encoding="utf-8",
        errors="ignore",
        universal_newlines=True,
    )
    while True:
        line = purging_process.stdout.readline().rstrip()
        if not line:
            break
        yield line
    purging_process.communicate()

def purge_fav(ns, purge_chat_id, purge_message_id, fav_id, fav_name):
    cloner = _cfg["general"]["cloner"]
    option1 = "delete"
    option2 = "rmdir"
    remote = _cfg["general"]["remote"]
    src_id = fav_id
    src_block = remote + ":" + "{" + src_id + "}"
    checkers = "--checkers=" + f"{_cfg['general']['parallel_c']}"
    transfers = "--transfers=" + f"{_cfg['general']['parallel_t']}"
    rmdirs = "--rmdirs"
    flags = ["--drive-trashed-only", "--drive-use-trash=false", "-P"]
    sa_sleep = "--drive-pacer-min-sleep=" + f"{_cfg['general']['min_sleep']}"

    command1 = [cloner, option1, src_block, rmdirs, checkers, transfers, sa_sleep]
    command1 += flags

    command2 = [cloner, option2, src_block, checkers, transfers, sa_sleep]
    command2 += flags

    purge_process(ns, command1, command2, purge_chat_id, purge_message_id, fav_id, fav_name)

    ns.purge = 0

def purge_process(ns, command1, command2, purge_chat_id, purge_message_id, fav_id, fav_name):
    for output in purge_run(command=command1):
        if ns.purge == 1:
            purging_process.kill()

    for output in purge_run(command=command2):
        if ns.purge == 1:
            purging_process.kill()

    if ns.purge == 0:
        last_purge_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        fav_col.update_one(
            {"G_id": fav_id}, {"$set": {"last_purge_time": last_purge_time,}},
        )

        purged_msg = (
            "༺ ✪iCopy✪ ༻\n\n"
            + fav_name
            + "\n["
            + fav_id
            + "]\n\n"
            + _text[_lang]["purging_done"]
        )

        bot.edit_message_text(
            chat_id=purge_chat_id, message_id=purge_message_id, text=purged_msg,
        )

    if ns.purge == 1:
        bot.edit_message_text(
            chat_id=purge_chat_id,
            message_id=purge_message_id,
            text=_text[_lang]["is_killed_by_user"],
        )
