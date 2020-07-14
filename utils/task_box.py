#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, pymongo
from utils import load,task_payload as _payload

future = load.db_counters.find_one({"_id": "task_list_id"})
future_id = 0

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
