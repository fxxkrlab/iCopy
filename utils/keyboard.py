#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils import load
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

_langtext = load._text[load._lang]

# start InlineKeyBoard
def start_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(_langtext['quick_mode'], callback_data="quick"),
            InlineKeyboardButton(_langtext['copy_mode'], callback_data="copy"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)

def is_cover_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(_langtext['is_cover'], callback_data="cover_quick"),
            InlineKeyboardButton(_langtext['not_cover'], callback_data="not_cover_quick"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)