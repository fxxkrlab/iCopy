#!/usr/bin/python3
# -*- coding: utf-8 -*-

from functools import wraps
from utils.load import _lang, _text
from utils import messages as _msg, load
from telegram import ParseMode

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        _user_id = str(update.effective_user.id)
        _first_name = update.effective_user.first_name
        if _user_id not in load.ENABLED_USERS:
            print(f"Unauthorized access denied for {_user_id}.")
            update.effective_message.reply_text(_msg.restricted_msg(_lang,_first_name,_user_id))
            return
        return func(update, context, *args, **kwargs)

    return wrapped

def restricted_quick(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        is_quick = {"_id": "fav_quick"}
        is_quick_cur = load.fav_col.find(is_quick)
        if list(is_quick_cur) == []:
            print("fav quick directory is not set.")
            update.effective_message.reply_text(
                _text[_lang]["null_fav_quick"],
            )
            return
        return func(update, context, *args, **kwargs)
    return wrapped

def restricted_copy(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        is_fav = {"fav_type": "fav"}
        is_fav_cur = load.fav_col.find(is_fav)
        if list(is_fav_cur) == []:
            print("fav directory is not set.")
            update.effective_message.reply_text(
                _text[_lang]["null_fav"],
            )
            return
        return func(update, context, *args, **kwargs)
    return wrapped