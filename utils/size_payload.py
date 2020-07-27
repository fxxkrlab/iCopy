#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re, pymongo
from utils import load
from utils.load import _lang, _text
from threading import Thread
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

request = TGRequest(con_pool_size=8)
bot = Bot(token=f"{_cfg['tg']['token']}", request=request)

simple_sizing = subprocess.Popen
size_object = ""
size_size = ""
size_info = ""

def simpe_size_run(command):
    global simple_sizing
    simple_sizing = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        encoding="utf-8",
        errors="ignore",
        universal_newlines=True,
    )
    while True:
        line = simple_sizing.stdout.readline().rstrip()
        if not line:
            break
        yield line
    simple_sizing.communicate()

def simple_size(ns, update, context, item, size_chat_id, size_message_id, share_name_list):
    cloner = _cfg["general"]["cloner"]
    option = "size"
    remote = _cfg["general"]["remote"]
    src_id = item
    src_block = remote + ":" + "{" + src_id + "}"
    checkers = "--checkers=" + f"{_cfg['general']['parallel_c']}"
    flags = ["--size-only"]
    sa_sleep = "--drive-pacer-min-sleep=" + f"{_cfg['general']['min_sleep']}"

    command = [cloner, option, src_block, checkers, sa_sleep]
    command += flags

    simple_size_process(ns,command, size_chat_id, size_message_id, share_name_list)

    ns.size = 0


def simple_size_process(ns,command, size_chat_id, size_message_id, share_name_list):
    for output in simpe_size_run(command):
        if ns.size == 1:
            simple_sizing.kill()

        regex_total_object = r"^Total objects:"
        regex_total_size = r"Total size:"
        if output:
            size_total_object = re.findall(regex_total_object, output)
            size_total_size = re.findall(regex_total_size, output)

            global size_object
            global size_size

            if size_total_object:
                size_object = output[15:]
            if size_total_size:
                size_size_all = output[12:]
                size_size = size_size_all.split("(")

    if ns.size == 0:
        for item in share_name_list:
            item_type = item["G_type"]
            item_id = item["G_id"]
            item_name = item["G_name"]

            global size_info
            size_info = (
                " ༺ ✪iCopy✪ ༻                 ["
                + _text[_lang]["sizing_done"]
                + "]\n\n"
                + item_type
                + " : "
                + item_name
                + "\n"
                + item_id
                + "\n"
                + "--------------------\n"
                + _text[_lang]["total_file_num"]
                + str(size_object)
                + "\n"
                + _text[_lang]["total_file_size"]
                + str(size_size[0])
                + "\n("
                + str(size_size[1])
            )

        bot.edit_message_text(
            chat_id=size_chat_id, message_id=size_message_id, text=size_info
        )

    if ns.size == 1:
        bot.edit_message_text(
            chat_id=size_chat_id,
            message_id=size_message_id,
            text=_text[_lang]["is_killed_by_user"],
        )

def owner_size(
    ns, size_chat_id, size_message_id, task_id, task_link, endpoint_id, endpoint_name
):
    cloner = _cfg["general"]["cloner"]
    option = "size"
    remote = _cfg["general"]["remote"]
    src_id = endpoint_id
    src_block = remote + ":" + "{" + src_id + "}"
    checkers = "--checkers=" + f"{_cfg['general']['parallel_c']}"
    flags = ["--size-only"]
    sa_sleep = "--drive-pacer-min-sleep=" + f"{_cfg['general']['min_sleep']}"

    command = [cloner, option, src_block, checkers, sa_sleep]
    command += flags

    owner_size_process(
        ns,
        command,
        size_chat_id,
        size_message_id,
        task_id,
        task_link,
        endpoint_id,
        endpoint_name,
    )

    ns.size = 0


def owner_size_process(
    ns,
    command,
    size_chat_id,
    size_message_id,
    task_id,
    task_link,
    endpoint_id,
    endpoint_name,
):
    for output in simpe_size_run(command):
        if ns.size == 1:
            simple_sizing.kill()
            
        regex_total_object = r"^Total objects:"
        regex_total_size = r"Total size:"
        if output:
            size_total_object = re.findall(regex_total_object, output)
            size_total_size = re.findall(regex_total_size, output)

            global size_object
            global size_size

            if size_total_object:
                size_object = output[15:]
            if size_total_size:
                size_size_all = output[12:]
                size_size = size_size_all.split("(")

    if ns.size == 0:
        size_size_re = r"([\d.]+[\s]?)([kMGTP]?Bytes)"
        get_size_size = re.search(size_size_re, str(size_size[0]))
        if get_size_size:
            size_size_num = get_size_size.group(1).strip()
            size_size_tail = get_size_size.group(2).strip()

        if task_id == 0:
            size_info = (
                " ༺ ✪iCopy✪ ༻ | favorites | ["
                + _text[_lang]["sizing_done"]
                + "]\n\n"
                + '<a href="{}">{}</a>'.format(task_link, endpoint_name)
                + "\n"
                + "--------------------\n"
                + _text[_lang]["total_file_num"]
                + str(size_object)
                + "\n"
                + _text[_lang]["total_file_size"]
                + str(size_size[0])
                + "\n("
                + str(size_size[1])
            )

            fav_col.update_one(
                {"G_id": endpoint_id},
                {
                    "$set": {
                        "fav_object": int(size_object),
                        "fav_size": float(size_size_num),
                        "fav_size_tail": size_size_tail,
                    },
                },
                upsert=True,
            )

        else:
            size_info = (
                " ༺ ✪iCopy✪ ༻ | "
                + "🏳️"
                + _text[_lang]["current_task_id"]
                + str(task_id)
                + " | ["
                + _text[_lang]["sizing_done"]
                + "]\n\n"
                + '<a href="{}">{}</a>'.format(task_link, endpoint_name)
                + "\n"
                + "--------------------\n"
                + _text[_lang]["total_file_num"]
                + str(size_object)
                + "\n"
                + _text[_lang]["total_file_size"]
                + str(size_size[0])
                + "\n("
                + str(size_size[1])
            )

            task_list.update_one(
                {"_id": int(task_id)},
                {
                    "$set": {
                        "task_current_prog_num": int(size_object),
                        "task_total_prog_num": int(size_object),
                        "task_current_prog_size": float(size_size_num),
                        "task_total_prog_size": float(size_size_num),
                        "task_current_prog_size_tail": size_size_tail[:1],
                        "task_total_prog_size_tail": size_size_tail,
                    }
                },
            )

        bot.edit_message_text(
            chat_id=size_chat_id,
            message_id=size_message_id,
            text=size_info,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )

    elif ns.size == 1:
        bot.edit_message_text(
            chat_id=size_chat_id,
            message_id=size_message_id,
            text=_text[_lang]["is_killed_by_user"],
        )
