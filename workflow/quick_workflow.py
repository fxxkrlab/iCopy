#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils.load import _lang, _text
from telegram.ext import ConversationHandler
from utils import messages as _msg, restricted as _r, get_functions as _func, task_box as _box

SET_FAV_MULTI, CHOOSE_MODE, GET_LINK, IS_COVER_QUICK = range(4)

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

        return GET_LINK

    if update.callback_query.data == "quick":
        update.callback_query.edit_message_text(
            _text[_lang]["mode_select_msg"].replace(
                "replace", _text[_lang]["quick_mode"]
            )
            + "\n"
            + _text[_lang]["request_share_link"]
        )

        return GET_LINK
