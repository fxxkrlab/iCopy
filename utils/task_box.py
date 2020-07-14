#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, pymongo
from utils import load,task_payload as _payload
from multiprocessing import Process as _mp

myclient = pymongo.MongoClient(f"mongodb+srv://{load.user}:{load.passwd}@{load.cfg['database']['db_addr']}",port=load.cfg['database']['db_port'],connect=False)
mydb = myclient[load.cfg['database']['db_name']]
#task_col = mydb['task_col']
task_list = mydb['task_list']
db_counters = mydb['counters']
future = task_list.find_one({"_id": "task_list_id"})
future_id = 0

if future != None:
    future_id = future['future_id']


def cook_task_to_db(update, context, tmp_task_list):
    global future_id
    for item in tmp_task_list:
        future_id += 1
        item["_id"] = future_id
        item["status"] = 0
        item["error"] = 0
        item["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["finished_time"] = ""

    global task_list
    insert_callback = task_list.insert_many(tmp_task_list)
    if insert_callback.inserted_ids:
        db_counters.update({"_id": "task_list_id"},{"future_id":future_id},upsert=True)
