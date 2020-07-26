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

def regex_in_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(_langtext['quick_mode'], callback_data="quick"),
            InlineKeyboardButton(_langtext['copy_mode'], callback_data="copy"),
            InlineKeyboardButton(_langtext['size_mode'], callback_data="size"),
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

def dedupe_mode_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("first", callback_data="first"),
        ],
        [
            InlineKeyboardButton("newest", callback_data="newest"),
            InlineKeyboardButton("oldest", callback_data="oldest"),
        ],
        [
            InlineKeyboardButton("largest", callback_data="largest"),
            InlineKeyboardButton("smallest", callback_data="smallest"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)

def dst_keyboard(update, context):
    favs = load.fav_col.find({"fav_type":"fav"})
    button_list = []

    for item in favs:
        button_list.append(InlineKeyboardButton(item['G_name'], callback_data=item['G_id']+"id+name"+item['G_name']))
    return InlineKeyboardMarkup(build_dst_keyboard(button_list,n_cols=2))
    
def build_dst_keyboard(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu