#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, pymongo
from utils import load,task_payload as _payload
from telegram.ext import ConversationHandler
from utils.load import _lang, _text

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

    insert_callback = load.task_list.insert_many(tmp_task_list)
    if insert_callback.inserted_ids:
        load.db_counters.update({"_id": "task_list_id"},{"future_id":future_id},upsert=True)


def taskinfo(update, context):
    entry_cmd = update.effective_message.text
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
        if list(task_list) != []:
            wait_num = len(list(task_list))
            for item in task_list:
                waititem = (
                    _text[_lang]["current_task_id"]
                    + str(item['_id'])
                    + _text[_lang]["current_task_src_name"]
                    + item['src_name']
                    + "\n--------------------\n"
                )
                waitlist.append(waititem)

            waitlist = "".join(waitlist)

            update.effective_message.reply_text(
                str(wait_num)
                +_text[_lang]["show_wait_list"] 
                + "\n\n" 
                + waitlist
            )
            waitlist = []

            return ConversationHandler.END

        else:
            update.effective_message.reply_text(
                _text[_lang]["show_wait_list_null"]
            )

            return ConversationHandler.END
    else:
        return ConversationHandler.END
