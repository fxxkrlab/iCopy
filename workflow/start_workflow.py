#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, logging, re
from telegram import ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
)
from utils.load import _lang, _text
from utils import messages as _msg, restricted as _r, keyboard as _KB

SET_FAV_MULTI, CHOOSE_MODE, GET_LINK, IS_COVER_QUICK, GET_DST, COOK_ID, REGEX_IN, REGEX_GET_DST = range(8)

def start(update, context):
    _first_name = update.effective_user.first_name
    update.effective_message.reply_text(
        _text[_lang]["start"].replace("replace",_first_name)
        + "\n"
        + _text[_lang]["guide_to_menu"]
    )

@_r.restricted
def menu(update, context):
    update.effective_message.reply_text(
        _text[_lang]["menu_msg"],
        reply_markup=_KB.start_keyboard(),
    )

    return CHOOSE_MODE
