#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from telegram.ext import ConversationHandler
from utils.load import _lang, _text
from utils import load, restricted as _r, get_functions as _func, task_box as _box, size_payload as _s_payload
from drive.gdrive import GoogleDrive as _gd
from multiprocessing import Process as _mp

SET_FAV_MULTI, CHOOSE_MODE, GET_LINK, IS_COVER_QUICK, GET_DST, COOK_ID = range(6)

def size(update, context):
    entry_cmd = update.effective_message.text
    if "/size" == entry_cmd:
        update.effective_message.reply_text(
            _text[_lang]["request_share_link"]
        )

        return COOK_ID

def size_handle(update, context):
    share_id_list = []
    share_name_list = []
    share_id = update.effective_message.text
    share_id_list = _func.cook_to_id(share_id)
    for item in share_id_list:
        size_msg = update.effective_message.reply_text(_text[_lang]["ready_to_size"])

        size_chat_id = size_msg.chat_id
        size_message_id = size_msg.message_id
        share_name_list += _func.get_src_name_from_id(update, item, list_name=share_name_list)
        progress = _mp(target=_s_payload.simple_size, args=(update, context, item, size_chat_id, size_message_id, share_name_list))
        progress.start()

        context.bot.edit_message_text(
            chat_id=size_chat_id, message_id=size_message_id, text=_text[_lang]["sizing"]
        )

    return ConversationHandler.END