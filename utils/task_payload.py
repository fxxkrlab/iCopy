#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re, time, pymongo
from utils import load, process_bar as _bar, get_functions as _func
from multiprocessing import Process as _mp, Manager
from utils.load import _lang, _text
import subprocess
from threading import Timer
from drive.gdrive import GoogleDrive as _gd
from telegram import ParseMode
from telegram.utils.request import Request as TGRequest
from telegram import Bot

myclient = pymongo.MongoClient(
    f"{load.cfg['database']['db_connect_method']}://{load.user}:{load.passwd}@{load.cfg['database']['db_addr']}",
    port=load.cfg["database"]["db_port"],
    connect=False,
)
mydb = myclient[load.cfg["database"]["db_name"]]
task_list = mydb["task_list"]
db_counters = mydb["counters"]

_cfg = load.cfg

request = TGRequest(con_pool_size=8)
bot = Bot(token=f"{_cfg['tg']['token']}", request=request)

message_info = ""
prog_bar = ""
current_working_file = ""
old_working_file = ""
now_elapsed_time = ""
context_old = ""
icopyprocess = subprocess.Popen
interruption = 0
dst_id = ""
src_name = ""


def task_buffer(ns):
    global dst_id
    global src_name
    while True:
        wait_list = task_list.find({"status": 0})
        for task in wait_list:
            if _cfg["general"]["cloner"] == "fclone":
                flags = ["--drive-server-side-across-configs", "--check-first"]
            else:
                flags = ["--drive-server-side-across-configs"]
            command = []

            cloner = _cfg["general"]["cloner"]
            option = _cfg["general"]["option"]
            remote = _cfg["general"]["remote"]
            src_id = task["src_id"]
            src_name = task["src_name"]
            if "/" in src_name:
                src_name = src_name.replace("/", "|")
            if "'" in src_name:
                src_name = src_name.replace("'", "")
            if '"' in src_name:
                src_name = src_name.replace('"', "")

            dst_id = task["dst_id"]
            src_block = remote + ":" + "{" + src_id + "}"
            dst_block = remote + ":" + "{" + dst_id + "}" + "/" + src_name
            checkers = "--checkers=" + f"{_cfg['general']['parallel_c']}"
            transfers = "--transfers=" + f"{_cfg['general']['parallel_t']}"
            sa_sleep = "--drive-pacer-min-sleep=" + f"{_cfg['general']['min_sleep']}"

            flags += _cfg["general"]["run_args"]
            flags += [checkers, transfers, sa_sleep]

            command = [cloner, option, src_block, dst_block]

            command += flags

            chat_id = task["chat_id"]

            task_process(chat_id, command, task, ns)

            ns.x = 0

            flags = []

            global old_working_line
            global current_working_line
            old_working_line = 0
            current_working_line = 0
            time.sleep(3)

        time.sleep(5)


def task_process(chat_id, command, task, ns):
    # mark is in processing in db
    task_list.update_one({"_id": task["_id"]}, {"$set": {"status": 2,}})
    db_counters.update({"_id": "last_task"}, {"task_id": task["_id"]}, upsert=True)
    chat_id = chat_id
    message = bot.send_message(chat_id=chat_id, text=_text[_lang]["ready_to_task"])
    message_id = message.message_id

    interval = 0.1
    timeout = 60
    xtime = 0
    old_working_line = 0
    current_working_line = 0
    task_current_prog_num = 0
    task_total_prog_num = 0
    task_percent = 0
    task_current_prog_size = "0"
    task_total_prog_size = "0 Bytes"
    task_in_size_speed = "-"
    task_in_file_speed = "-"
    task_eta_in_file = "-"
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for toutput in run(command):
        if ns.x == 1:
            global icopyprocess
            icopyprocess.kill()

        regex_working_file = r"^ * "
        regex_elapsed_time = r"^Elapsed time:"
        regex_total_files = (
            r"Transferred:\s+(\d+) / (\d+), (\d+)%(?:,\s*([\d.]+\sFiles/s))?"
        )
        regex_total_size = (
            r"Transferred:[\s]+([\d.]+\s*)([kMGTP]?) / ([\d.]+[\s]?)([kMGTP]?Bytes),"
            r"\s*(?:\-|(\d+)\%),\s*([\d.]+\s*[kMGTP]?Bytes/s),\s*ETA\s*([\-0-9hmsdwy]+)"
        )

        output = toutput

        if output:
            task_total_files = re.search(regex_total_files, output)
            task_total_size = re.search(regex_total_size, output)
            task_elapsed_time = re.findall(regex_elapsed_time, output)
            task_working_file = re.findall(regex_working_file, output)

            if task_total_files:
                task_current_prog_num = task_total_files.group(1)
                task_total_prog_num = task_total_files.group(2)
                task_percent = int(task_total_files.group(3))
                task_in_file_speed = task_total_files.group(4)

            if task_total_size:
                task_current_prog_size = task_total_size.group(1).strip()
                task_current_prog_size_tail = task_total_size.group(2)
                task_total_prog_size = task_total_size.group(3).strip()
                task_total_prog_size_tail = task_total_size.group(4)
                task_in_size_speed = task_total_size.group(6)
                task_eta_in_file = task_total_size.group(7)

            if task_elapsed_time:
                global now_elapsed_time
                now_elapsed_time = output.replace(" ", "").split(":")[1]

            if task_working_file:
                global current_working_file
                current_working_line += 1
                current_working_file = (
                    output.lstrip("*  ").rsplit(":")[0].rstrip("Transferred")
                )

        global prog_bar
        prog_bar = _bar.status(0)
        if task_percent != 0:
            prog_bar = _bar.status(task_percent)

        global message_info
        message_info = (
            _text[_lang]["task_src_info"]
            + "\n"
            + "📃"
            + task["src_name"]
            + "\n"
            + "----------------------------------------"
            + "\n"
            + _text[_lang]["task_dst_info"]
            + "\n"
            + "📁"
            + task["dst_name"]
            + ":"
            + "\n"
            + "    ┕─📃"
            + task["src_name"]
            + "\n"
            + "----------------------------------------"
            + "\n\n"
            + _text[_lang]["task_start_time"]
            + start_time
            + "\n\n"
            + _text[_lang]["task_files_size"]
            + str(task_current_prog_size)
            + task_current_prog_size_tail
            + "/"
            + str(task_total_prog_size)
            + task_total_prog_size_tail
            + "\n"
            + _text[_lang]["task_files_num"]
            + str(task_current_prog_num)
            + "/"
            + str(task_total_prog_num)
            + "\n"
            + _text[_lang]["task_status"]
            + "\n\n"
            + str(task_in_size_speed)
            + "  |  "
            + str(task_in_file_speed)
            + "\n\n"
            + str(task_percent)
            + "%"
            + str(prog_bar)
        )

        if (
            int(time.time()) - xtime > interval
            and old_working_line != current_working_line
        ):
            Timer(
                0,
                task_message_box,
                args=(
                    bot,
                    chat_id,
                    message_id,
                    " ༺ ✪iCopy✪ ༻ \n"
                    + _text[_lang]["doing"]
                    + " | "
                    + "🏳️"
                    + _text[_lang]["current_task_id"]
                    + str(task["_id"])
                    + "\n\n"
                    + message_info
                    + "\n\n"
                    + current_working_file[:30]
                    + "\n"
                    + "ETA : "
                    + str(task_eta_in_file),
                ),
            ).start()
            old_working_line = current_working_line
            global old_working_file
            old_working_file = current_working_file
            time.sleep(3.5)
            xtime = time.time()

        if (
            int(time.time()) - xtime > timeout
            and current_working_file == old_working_file
            and task_percent > 5
        ):
            global interruption
            interruption = 1
            break

    old_working_file = ""
    finished_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    dst_endpoint_id = _gd.get_dst_endpoint_id(_gd(), dst_id, src_name)
    if dst_endpoint_id:
        dst_endpoint_link = r"https://drive.google.com/open?id={}".format(
            dst_endpoint_id["id"]
        )

    if ns.x == 0:
        time.sleep(5)
        prog_bar = _bar.status(100)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=" ༺ ✪iCopy✪ ༻ \n"
            + _text[_lang]["done"]
            + " | "
            + "🏳️"
            + _text[_lang]["current_task_id"]
            + str(task["_id"])
            + "\n\n"
            + message_info.replace(
                "    ┕─📃" + task["src_name"],
                "    ┕─📃"
                + '<a href="{}">{}</a>'.format(dst_endpoint_link, task["src_name"]),
            )
            + "\n"
            + _text[_lang]["task_finished_time"]
            + finished_time
            + "\n"
            + _text[_lang]["elapsed_time"]
            + str(now_elapsed_time),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
        check_is_reset = task_list.find_one({"_id": task["_id"]})
        if check_is_reset['is_reset'] == 0:
            task_list.update_one(
                {"_id": task["_id"]},
                {
                    "$set": {
                        "status": 1,
                        "start_time": start_time,
                        "finished_time": finished_time,
                        "task_current_prog_num": int(task_current_prog_num),
                        "task_total_prog_num": int(task_total_prog_num),
                        "task_current_prog_size": float(task_current_prog_size),
                        "task_total_prog_size": float(task_total_prog_size),
                        "task_current_prog_size_tail": task_current_prog_size_tail,
                        "task_total_prog_size_tail": task_total_prog_size_tail,
                        "dst_endpoint_link": dst_endpoint_link,
                        "dst_endpoint_id": dst_endpoint_id["id"],
                    }
                },
            )

        if check_is_reset['is_reset'] == 1:
            task_list.update_one(
                {"_id": task["_id"]},
                {
                    "$set": {
                        "status": 1,
                        "start_time": start_time,
                        "finished_time": finished_time,
                        "task_current_prog_num": int(task_current_prog_num) + check_is_reset['task_current_prog_num'],
                        "task_total_prog_num": int(task_total_prog_num) + check_is_reset['task_total_prog_num'],
                        "task_current_prog_size": 0,
                        "task_total_prog_size": 0,
                        "task_current_prog_size_tail": "",
                        "task_total_prog_size_tail": "",
                        "dst_endpoint_link": dst_endpoint_link,
                        "dst_endpoint_id": dst_endpoint_id["id"],
                    }
                },
            )

    if ns.x == 1:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=" ༺ ✪iCopy✪ ༻ \n"
            + _text[_lang]["killed"]
            + " | "
            + "🏳️"
            + _text[_lang]["current_task_id"]
            + str(task["_id"])
            + "\n\n"
            + message_info.replace(
                "\n\n" + _text[_lang]["task_start_time"] + start_time, ""
            ).replace(
                "\n"
                + _text[_lang]["task_status"]
                + "\n\n"
                + str(task_in_size_speed)
                + "  |  "
                + str(task_in_file_speed),
                "",
            )
            + "\n"
            + _text[_lang]["is_killed_by_user"],
        )

        task_list.update_one(
            {"_id": task["_id"]},
            {
                "$set": {
                    "status": 1,
                    "error": 9,
                    "start_time": start_time,
                    "finished_time": finished_time,
                }
            },
        )

    if interruption == 1:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=" ༺ ✪iCopy✪ ༻ \n"
            + _text[_lang]["interrupted"]
            + " | "
            + "🏳️"
            + _text[_lang]["current_task_id"]
            + str(task["_id"])
            + "\n\n"
            + message_info.replace(
                "\n\n" + _text[_lang]["task_start_time"] + start_time, ""
            ).replace(
                "\n"
                + _text[_lang]["task_status"]
                + "\n\n"
                + str(task_in_size_speed)
                + "  |  "
                + str(task_in_file_speed),
                "",
            )
            + "\n"
            + _text[_lang]["is_interrupted_error"],
        )

        task_list.update_one(
            {"_id": task["_id"]},
            {
                "$set": {
                    "status": 1,
                    "error": 1,
                    "start_time": start_time,
                    "finished_time": finished_time,
                }
            },
        )

    prog_bar = _bar.status(0)


def task_message_box(bot, chat_id, message_id, context):
    global context_old
    context_old = "iCopy"
    if context_old != context:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=context)
        context_old = context


def run(command):
    global icopyprocess
    icopyprocess = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        encoding="utf-8",
        errors="ignore",
        universal_newlines=True,
    )
    while True:
        line = icopyprocess.stdout.readline().rstrip()
        if not line:
            break
        yield line
    icopyprocess.communicate()

