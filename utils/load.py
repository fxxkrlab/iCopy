#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, toml
import pymongo
from urllib import parse
from drive import gdrive
from multiprocessing import Manager
from telegram.utils.request import Request as TGRequest
from telegram import Bot


### local version
_version = "v0.2.0-beta.6.4"

_cfgFile_RAW = os.path.abspath(os.path.join("config", "conf.toml"))
cfg = toml.load(_cfgFile_RAW)
_textFile_RAW = os.path.abspath(os.path.join("config", "text.toml"))
_text = toml.load(_textFile_RAW)


### load language selector
_lang = cfg["general"]["language"]

### ENABLED_USERS
ENABLED_USERS = os.environ.get("ENABLED_USERS", f"{cfg['tg']['usr_id']}")

### Mongodb
user = parse.quote_plus(f"{cfg['database']['db_user']}")
passwd = parse.quote_plus(f"{cfg['database']['db_passwd']}")
myclient = pymongo.MongoClient(
    f"{cfg['database']['db_connect_method']}://{user}:{passwd}@{cfg['database']['db_addr']}",
    port=cfg["database"]["db_port"],
    connect=False,
)
mydb = myclient[cfg["database"]["db_name"]]

# main_col = mydb['main_col']
fav_col = mydb["fav_col"]
task_list = mydb["task_list"]
db_counters = mydb["counters"]

### drive().list
all_drive = gdrive.GoogleDrive().drive_list()

### ns
manager = Manager()
ns = manager.Namespace()

### Restore Unexpected Interrupted Task status 2 --> 0
task_list.update_one(
    {"status": 2}, {"$set": {"status": 0,}},
)

### regex entry pattern
regex_entry_pattern = r"https://drive\.google\.com/(?:drive/(?:u/[\d]+/)?(?:mobile/)?folders/([\w.\-_]+)(?:\?[\=\w]+)?|folderview\?id=([\w.\-_]+)(?:\&[=\w]+)?|open\?id=([\w.\-_]+)(?:\&[=\w]+)?|(?:a/[\w.\-_]+/)?file/d/([\w.\-_]+)|(?:a/[\w.\-_]+/)?uc\?id\=([\w.\-_]+)&?)"

### define bot
request = TGRequest(con_pool_size=8)
bot = Bot(token=f"{cfg['tg']['token']}", request=request)