import re, time, pymongo
from utils import load
from utils.load import _lang, _text
import subprocess
from telegram import ParseMode

myclient = pymongo.MongoClient(
    f"{load.cfg['database']['db_connect_method']}://{load.user}:{load.passwd}@{load.cfg['database']['db_addr']}",
    port=load.cfg["database"]["db_port"],
    connect=False,
)
mydb = myclient[load.cfg["database"]["db_name"]]
task_list = mydb["task_list"]

bot = load.bot
_cfg = load.cfg


def dedupe_task(
    dedu_mode,
    dedu_chat_id,
    dedu_message_id,
    dedu_task_id,
    dedu_link,
    dedu_id,
    dedu_name,
):
    cloner = _cfg["general"]["cloner"]
    option = "dedupe"
    mode_suffix = "--dedupe-mode"
    mode = dedu_mode
    remote = _cfg["general"]["remote"]
    src_id = dedu_id
    src_block = remote + ":" + "{" + src_id + "}"
    checkers = "--checkers=" + f"{_cfg['general']['parallel_c']}"
    transfers = "--transfers=" + f"{_cfg['general']['parallel_t']}"
    flags = ["-q"]
    sa_sleep_suffix = "--drive-pacer-min-sleep"
    sa_sleep = _cfg['general']['min_sleep']

    command = [cloner, option, mode_suffix, mode, src_block, checkers, transfers, sa_sleep_suffix, sa_sleep]
    command += flags

    print(command)

    deduping_process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False,
    )
    deduping_process.communicate()

    last_dedupe_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    task_list.update_one(
        {"_id": int(dedu_task_id)}, {"$set": {"last_dedupe_time": last_dedupe_time,}},
    )

    deduped_msg = (
        " ༺ ✪iCopy✪ ༻ | "
        + "🏳️"
        + _text[_lang]["current_task_id"]
        + str(dedu_task_id)
        + "\n\n"
        + '<a href="{}">{}</a>'.format(dedu_link, dedu_name)
        + "\n["
        + dedu_id
        + "]\n\n"
        + _text[_lang]["deduping_done"]
    )

    bot.edit_message_text(
        chat_id=dedu_chat_id,
        message_id=dedu_message_id,
        text=deduped_msg,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
