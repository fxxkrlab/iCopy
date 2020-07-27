#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, re, json, requests
from utils import (
    load,
    messages as _msg,
    restricted as _r,
    get_set as _set,
    task_box as _box,
    task_payload as _payload,
    callback_stage as _stage,
)
from workflow import copy_workflow as _copy
from utils.load import _lang, _text
from telegram.ext import ConversationHandler
from drive.gdrive import GoogleDrive as _gd
from telegram import ParseMode
from threading import Thread
from utils.load import ns


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

regex1 = r"[-\w]{11,}"
regex2 = r"[-\w]"
judge_folder_len = [28, 33]
pick_quick = []
mode = ""

def cook_to_id(get_share_link):
    share_id_list = []
    unsupported_type = []
    share_id = ""

    share_link = get_share_link.strip().replace(" ", "").splitlines()
    for item in share_link:
        if "drive.google.com" in item:
            share_id = re.findall(regex1, item)
            if len(share_id) <= 33:
                share_id = "".join(share_id)

                share_id_list.append(share_id)
            else:
                unsupported_type.append({"type": "link", "value": item})

        else:
            if len(item) >= 11 and len(item) <= 33 and re.match(regex2, item):
                share_id_list.append(item)
            else:
                unsupported_type.append({"type": "id", "value": item})

    return share_id_list


def get_name_from_id(update, taget_id, list_name):
    cook_list = list(list_name)
    if len(taget_id) >= 11 and len(taget_id) < 28:
        cook_list.append(
            {"G_type": "G_drive", "G_id": taget_id, "G_name": load.all_drive[taget_id],}
        )
    elif len(taget_id) in judge_folder_len:
        cook_list.append(
            {
                "G_type": "G_Folder",
                "G_id": taget_id,
                "G_name": _gd().file_get_name(file_id=taget_id),
            }
        )
    else:
        update.effective_message.reply_text(_msg.get_fav_len_invaild(_lang, taget_id))

        return ConversationHandler.END

    return cook_list

def get_src_name_from_id(update, taget_id, list_name):
    cook_list = []
    cook_list = list(list_name)
    if len(taget_id) >= 11 and len(taget_id) < 28:
        target_info = _gd.drive_get(_gd(),drive_id=taget_id)
        cook_list.append(
            {"G_type": "G_drive", "G_id": taget_id, "G_name": target_info['name'],}
        )
    elif len(taget_id) in judge_folder_len:
        cook_list.append(
            {
                "G_type": "G_Folder",
                "G_id": taget_id,
                "G_name": _gd().file_get_name(file_id=taget_id),
            }
        )
    else:
        update.effective_message.reply_text(_msg.get_fav_len_invaild(_lang, taget_id))

        return ConversationHandler.END

    return cook_list


def insert_to_db_quick(pick_quick, update):
    is_quick = {"_id": "fav_quick"}
    is_quick_cur = load.fav_col.find(is_quick)
    if list(is_quick_cur) == []:
        for item in pick_quick:
            item["_id"] = "fav_quick"
            load.fav_col.insert_one(item)

        update.effective_message.reply_text(
            _text[_lang]["insert_quick_success"], parse_mode=ParseMode.MARKDOWN_V2
        )

        return ConversationHandler.END

    else:
        status = "is_cover"

        return status


def modify_quick_in_db(update, context):
    pick_quick = _set.pick_quick
    for item in pick_quick:
        load.fav_col.update({"_id": "fav_quick"}, item, upsert=True)

    update.effective_message.reply_text(
        _text[_lang]["modify_quick_success"], parse_mode=ParseMode.MARKDOWN_V2
    )

    return ConversationHandler.END


def delete_in_db_quick():
    load.fav_col.delete_one({"_id": "fav_quick"})

    return


def delete_in_db(delete_request):
    load.fav_col.delete_one(delete_request)

    return


def get_share_link(update, context):
    get_share_link = update.effective_message.text
    tmp_src_name_list = ""
    tmp_task_list = []
    src_name_list = []
    src_id_list = cook_to_id(get_share_link)
    is_quick = {"_id": "fav_quick"}
    is_quick_cur = load.fav_col.find(is_quick)
    is_dstinfo = _copy.current_dst_info

    if is_dstinfo != "":
        dstinfo = is_dstinfo.split("id+name")
        dst_id = dstinfo[0]
        dst_name = dstinfo[1]
    else:
        for doc in is_quick_cur:
            dst_id = doc["G_id"]
            dst_name = doc["G_name"]

    for item in src_id_list:
        src_name_list += get_src_name_from_id(update, item, list_name=tmp_src_name_list)
        tmp_src_name_list = ""

    for item in src_name_list:
        src_id = item["G_id"]
        src_name = item["G_name"]

        tmp_task_list.append(
            {
                "mode_type": mode,
                "src_id": src_id,
                "src_name": src_name,
                "dst_id": dst_id,
                "dst_name": dst_name,
                "chat_id": update.message.chat_id,
                "raw_message_id": update.message.message_id,
            }
        )

    Thread(target=_box.cook_task_to_db, args=(update, context, tmp_task_list)).start()
    _copy.current_dst_info = ""
    return ConversationHandler.END

def taskill(update, context):
    entry_cmd = update.effective_message.text
    if "/kill" == entry_cmd :
        ns.x = 1
    
    elif context.args[0] == "task":
        ns.x = 1

    elif context.args[0] == "size":
        ns.size = 1    

    elif context.args[0] == "purge":
        ns.purge = 1

    elif context.arg[0] == "dedupe":
        ns.dedupe = 1

    else:
        update.effective_message.reply_text(_text[_lang]["global_command_error"])
        
def check_restart(bot):
    check_restart = load.db_counters.find_one({"_id": "is_restart"})
    chat_id = check_restart["chat_id"]
    message_id = check_restart["message_id"]
    load.db_counters.update_one({"_id": "is_restart"}, {"$set": {"status": 0,}}, True)
    bot.edit_message_text(
        chat_id=chat_id, message_id=message_id, text=_text[_lang]["restart_success"]
    )

def _version(update, context):
    update.message.reply_text(
        "Welcome to use iCopy Telegram BOT\n\n"
        f"Current Version : {load._version}\n\n"
        f"Latest Version : {_get_ver()}"
    )

def _get_ver():
    _url = "https://api.github.com/repos/fxxkrlab/iCopy/releases"
    _r_ver = requests.get(_url).json()
    _latest_ver = _r_ver[0]["tag_name"]
    return _latest_ver

@_r.restricted
def cancel(update, context):
    user = update.effective_user.first_name
    logger.info("User %s canceled the conversation.", user)
    update.effective_message.reply_text(
        f"Bye! {update.effective_user.first_name} ," + _text[_lang]["cancel_msg"]
    )
    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
