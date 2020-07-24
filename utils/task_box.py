#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, pymongo, re
from utils import load,task_payload as _payload
from telegram.ext import ConversationHandler
from utils.load import _lang, _text
from telegram import ParseMode

future = load.db_counters.find_one({"_id": "task_list_id"})
future_id = 0
waititem = ""
waitlist = []

if future != None:
    future_id = future['future_id']

def cook_task_to_db(update, context, tmp_task_list):

    for item in tmp_task_list:
        global future_id
        future_id += 1
        item["_id"] = future_id
        item["status"] = 0
        item["error"] = 0
        item["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["finished_time"] = ""
        item["start_time"] = ""
        item["task_current_prog_num"] = 0
        item["task_total_prog_num"] = 0
        item["task_current_prog_size"] = 0
        item["task_total_prog_size"] = 0
        item["task_current_prog_size_tail"] = ""
        item["task_total_prog_size_tail"] = ""
        item["dst_endpoint_link"] = ""
        item["dst_endpoint_id"] = ""
        item["is_reset"] = 0

    insert_callback = load.task_list.insert_many(tmp_task_list)
    if insert_callback.inserted_ids:
        load.db_counters.update({"_id": "task_list_id"},{"future_id":future_id},upsert=True)
        update.effective_message.reply_text(
            _text[_lang]["add_task_successful"]
        )


def taskinfo(update, context):
    entry_cmd = update.effective_message.text
    match_cmd = re.search(r'^\/task ([1-9]\d*)$', entry_cmd, flags=re.I)
    if " " in entry_cmd:
        entry_cmd = entry_cmd.replace(" ","")

    if entry_cmd == "/task":
        current_task = load.task_list.find_one({"status":2})
        if current_task is not None:
            current_task_id = current_task['_id']
            current_task_src_name = current_task['src_name']
            current_task_dst_name = current_task['dst_name']
            update.effective_message.reply_text(
                _text[_lang]["is_current_task"]
                + _text[_lang]["current_task_id"]
                + str(current_task_id)
                + "\n"
                + _text[_lang]["current_task_src_name"]
                + current_task_src_name
                + "\n"
                + _text[_lang]["current_task_dst_name"]
                + current_task_dst_name
            )

            return ConversationHandler.END

        else:
            update.effective_message.reply_text(
                _text[_lang]['is_not_current_task']
            )

            return ConversationHandler.END

    elif entry_cmd[5:] == "list":
        global waititem
        global waitlist
        task_list = load.task_list.find({"status":0}).limit(10)

        if task_list != []:
            for doc in task_list:
                waititem = _text[_lang]["current_task_id"] + str(doc['_id']) + _text[_lang]["current_task_src_name"] + doc['src_name'] + "\n--------------------\n"
                waitlist.append(waititem)

            task_wait_num = len(waitlist)
            waitlist = "".join(waitlist)

            update.effective_message.reply_text(str(task_wait_num) +_text[_lang]["show_wait_list"] + waitlist)

            waitlist = []

            return ConversationHandler.END

        else:
            update.effective_message.reply_text(
                _text[_lang]["show_wait_list_null"]
            )

            return ConversationHandler.END

    elif match_cmd:
        limit_query = load.db_counters.find_one({"_id":"task_list_id"})
        check_query = match_cmd.group(1)

        if int(check_query) <= limit_query['future_id']:

            check_task = load.task_list.find_one({"_id": int(check_query)})

            if check_task["status"] == 1:
                if "task_current_prog_num" and "task_current_prog_size_tail" in check_task:
                    if check_task["error"] == 0:
                        task_status_now = _text[_lang]["done"]
                    elif check_task["error"] == 1:
                        task_status_now == _text[_lang]["is_interrupted_error"]
                    elif check_task["error"] == 9:
                        task_status_now == _text[_lang]["is_killed_by_user"]

                    check_msg = (
                        _text[_lang]["current_task_id"]
                        + str(check_query)
                        + "\n"
                        + '<a href="{}">{}</a>'.format(check_task["dst_endpoint_link"], check_task["src_name"])
                        + "\n"
                        + _text[_lang]["task_status"]
                        + task_status_now
                        + "\n"
                        + _text[_lang]["total_file_num"]
                        + str(check_task["task_current_prog_num"])
                        + "/"
                        + str(check_task["task_total_prog_num"])
                        + "\n"
                        + _text[_lang]["total_file_size"]
                        + str(check_task["task_current_prog_size"])
                        + check_task["task_current_prog_size_tail"]
                        + "/"
                        + str(check_task["task_total_prog_size"])
                        + check_task["task_total_prog_size_tail"]
                    )

                else:
                    check_msg = _text[_lang]["support_error"]

            elif check_task["status"] == 0:
                check_msg = _text[_lang]["task_is_in_queue"] + "\n" + _text[_lang]["finished_could_be_check"]

            elif check_task["status"] == 2:
                check_msg = _text[_lang]["doing"] + "\n" + _text[_lang]["finished_could_be_check"]

            update.effective_message.reply_text(check_msg,parse_mode=ParseMode.HTML,disable_web_page_preview=True)

        else:
            update.effective_message.reply_text(_text[_lang]["over_limit_to_check"])


    else:
        return ConversationHandler.END

def task_reset(update, context):
    entry_cmd = update.effective_message.text
    match_cmd = re.search(r'^\/RESET ([1-9]\d*)$', entry_cmd, flags=re.I)

    if "/reset" == entry_cmd:
        check_query = load.db_counters.find_one({"_id": "last_task"})
        load.task_list.update_one({"_id": check_query['task_id']}, {"$set": {"status": 0,"is_reset": 1}})
        update.effective_message.reply_text(
            _text[_lang]["reset_successful"].replace("replace",str(check_query['task_id']))
        )

    elif match_cmd:
        limit_query = load.db_counters.find_one({"_id":"task_list_id"})
        check_query = match_cmd.group(1)

        if int(check_query) <= limit_query['future_id']:

            load.task_list.update_one({"_id": int(check_query)}, {"$set": {"status": 0,"is_reset": 1}})
            update.effective_message.reply_text(
                _text[_lang]["reset_successful"].replace("replace",check_query)
            )
        
        else:
            update.effective_message.reply_text(
                _text[_lang]["over_limit_error"]
            )

    else:
        update.effective_message.reply_text(
            _text[_lang]["global_command_error"]
        )