import re, time, pymongo
from utils import load
from utils.load import _lang, _text
import subprocess
from telegram.utils.request import Request as TGRequest
from telegram import Bot

myclient = pymongo.MongoClient(
    f"{load.cfg['database']['db_connect_method']}://{load.user}:{load.passwd}@{load.cfg['database']['db_addr']}",
    port=load.cfg["database"]["db_port"],
    connect=False,
)
mydb = myclient[load.cfg["database"]["db_name"]]
fav_col = mydb["fav_col"]

_cfg = load.cfg

request = TGRequest(con_pool_size=8)
bot = Bot(token=f"{_cfg['tg']['token']}", request=request)

def purge_fav(purge_chat_id, purge_message_id, fav_id, fav_name):
    cloner = _cfg["general"]["cloner"]
    option1 = "delete"
    option2 = "rmdir"
    remote = _cfg["general"]["remote"]
    src_id = fav_id
    src_block = remote + ":" + "{" + src_id + "}"
    checkers = "--checkers=" + f"{_cfg['general']['parallel_c']}"
    transfers = "--transfers=" + f"{_cfg['general']['parallel_t']}"
    rmdirs = "--rmdirs"
    flags = ["--drive-trashed-only", "--drive-use-trash=false", "-q"]
    sa_sleep = "--drive-pacer-min-sleep=" + f"{_cfg['general']['min_sleep']}"

    command1 = [cloner, option1, src_block, rmdirs, checkers, transfers, sa_sleep]
    command1 += flags

    command2 = [cloner, option2, src_block, checkers, transfers, sa_sleep]
    command2 += flags

    purging_process1 = subprocess.Popen(
        command1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False,
    )
    purging_process1.communicate()

    purging_process2 = subprocess.Popen(
        command2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False,
    )
    purging_process2.communicate()

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
