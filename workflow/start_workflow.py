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

SET_FAV_MULTI, CHOOSE_MODE, GET_LINK, IS_COVER_QUICK = range(4)


@_r.restricted
def start(update, context):
    _first_name = update.effective_user.first_name
    update.effective_message.reply_text(
        _msg.start_msg(_lang, _first_name),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=_KB.start_keyboard(),
    )

    return CHOOSE_MODE
