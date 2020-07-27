#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils.load import _lang, _text
from telegram.ext import ConversationHandler
from utils import (
    messages as _msg,
    restricted as _r,
    get_functions as _func,
    task_box as _box,
    keyboard as _KB,
    callback_stage as _stage,
)

current_dst_info = ""


@_r.restricted
@_r.restricted_copy
def copy(update, context):
    _func.mode = "copy"
    call_mode = update.effective_message.text

    if "/copy" == call_mode.strip()[:5]:
        update.effective_message.reply_text(
            _text[_lang]["mode_select_msg"].replace(
                "replace", _text[_lang]["copy_mode"]
            )
            + "\n"
            + _text[_lang]["request_dst_target"],
            reply_markup=_KB.dst_keyboard(update, context),
        )

        return _stage.GET_DST

    if update.callback_query.data == "copy":
        update.callback_query.edit_message_text(
            _text[_lang]["mode_select_msg"].replace(
                "replace", _text[_lang]["copy_mode"]
            )
            + "\n"
            + _text[_lang]["request_dst_target"],
            reply_markup=_KB.dst_keyboard(update, context),
        )

        return _stage.GET_DST


def request_srcinfo(update, context):
    global current_dst_info
    current_dst_info = update.callback_query.data
    update.callback_query.edit_message_text(_text[_lang]["request_share_link"])

    return _stage.GET_LINK

