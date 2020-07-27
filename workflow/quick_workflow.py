#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils.load import _lang, _text
from telegram.ext import ConversationHandler
from utils import (
    restricted as _r, 
    get_functions as _func, 
    task_box as _box, 
    callback_stage as _stage,
)

@_r.restricted
@_r.restricted_quick
def quick(update, context):
    _func.mode = "quick"
    call_mode = update.effective_message.text

    if "/quick" == call_mode.strip()[:6]:
        update.effective_message.reply_text(
            _text[_lang]["mode_select_msg"].replace(
                "replace", _text[_lang]["quick_mode"]
            )
            + "\n"
            + _text[_lang]["request_share_link"]
        )

        return _stage.GET_LINK

    if update.callback_query.data == "quick":
        update.callback_query.edit_message_text(
            _text[_lang]["mode_select_msg"].replace(
                "replace", _text[_lang]["quick_mode"]
            )
            + "\n"
            + _text[_lang]["request_share_link"]
        )

        return _stage.GET_LINK
