#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, toml
#json
import pymongo
from urllib import parse
from drive import gdrive
from multiprocessing import Manager

### local version
_version = 'v0.2.0-alpha.15'

_cfgFile_RAW = os.path.abspath(os.path.join('config','conf.toml'))
cfg = toml.load(_cfgFile_RAW)
_textFile_RAW = os.path.abspath(os.path.join('config','text.toml'))
_text = toml.load(_textFile_RAW)


### load language selector
_lang = cfg['general']['language']

### ENABLED_USERS
ENABLED_USERS = os.environ.get("ENABLED_USERS", f"{cfg['tg']['usr_id']}")

### Mongodb
user = parse.quote_plus(f"{cfg['database']['db_user']}")
passwd = parse.quote_plus(f"{cfg['database']['db_passwd']}")
myclient = pymongo.MongoClient(f"{cfg['database']['db_connect_method']}://{user}:{passwd}@{cfg['database']['db_addr']}",port=cfg['database']['db_port'],connect=False)
mydb = myclient[cfg['database']['db_name']]

#main_col = mydb['main_col']
fav_col = mydb['fav_col']
task_list = mydb['task_list']
db_counters = mydb['counters']

### drive().list
all_drive = gdrive.GoogleDrive().drive_list()

### ns
manager = Manager()
ns = manager.Namespace()

### Restore Unexpected Interrupted Task status 2 --> 0
task_list.update_one({"status": 2},{"$set": {"status": 0,}},)
