import re
from telegram import Bot
from utils import load
from utils.load import _lang, _text
from telegram.utils.request import Request as TGRequest
from threading import Thread
import subprocess

_cfg = load.cfg
size_object = ""
size_size = ""
size_info = ""

def simple_size(update, context, item, size_chat_id, size_message_id, share_name_list):
    request = TGRequest(con_pool_size=8)
    bot = Bot(token=f"{_cfg['tg']['token']}", request=request)

    cloner = _cfg["general"]["cloner"]
    option = "size"
    remote = _cfg["general"]["remote"]
    src_id = item
    src_block = remote + ":" + "{" + src_id + "}"
    checkers = "--checkers=" + f"{_cfg['general']['parallel_c']}"
    flags = ['--size-only']
    sa_sleep = "--drive-pacer-min-sleep=" + f"{_cfg['general']['min_sleep']}"

    command = [cloner, option, src_block, checkers, sa_sleep]
    command += flags

    simple_size_process(command, bot, size_chat_id, size_message_id, share_name_list)

def simple_size_process(command, bot, size_chat_id, size_message_id, share_name_list):
    for output in simpe_size_run(command):
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

    for item in share_name_list:
        item_type = item['G_type']
        item_id = item['G_id']
        item_name = item['G_name']

        global size_info
        size_info = (
            " ༺ ✪iCopy✪ ༻             ["
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

def simpe_size_run(command):
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
