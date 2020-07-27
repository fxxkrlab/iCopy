#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils.load import _lang, _text, ns
from utils import (
    load, 
    restricted as _r, 
    keyboard as _KB, 
    purge_payload as _p_payload, 
    callback_stage as _stage,
)
from multiprocessing import Process as _mp
from telegram.ext import ConversationHandler

bot = load.bot
ns.purge = 0

@_r.restricted
def purge(update, context):
    update.effective_message.reply_text(
        _text[_lang]["mode_select_msg"].replace(
            "replace", _text[_lang]["purge_mode"]
        )
        + "\n"
        + _text[_lang]["request_target_folder"],
        reply_markup=_KB.dst_keyboard(update, context),
    )

    return _stage.COOK_FAV_PURGE

def pre_to_purge(update, context):
    get_callback = update.callback_query.data
    purge_msg = bot.edit_message_text(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        text=_text[_lang]["ready_to_purge"],
        reply_markup=None,
    )

    purge_chat_id = purge_msg.chat_id
    purge_message_id = purge_msg.message_id

    fav_info_list = get_callback.split("id+name")
    fav_id = fav_info_list[0]
    fav_name = fav_info_list[1]

    if len(fav_id) < 28:
        progress = _mp(
            target=_p_payload.purge_fav,
            args=(
                ns,
                purge_chat_id,
                purge_message_id,
                fav_id,
                fav_name,
            ),
        )

        progress.start()

        bot.edit_message_text(
            chat_id=purge_chat_id,
            message_id=purge_message_id,
            text=_text[_lang]["purging"],
        )

        return ConversationHandler.END
    
    else:
        bot.edit_message_text(
            chat_id=purge_chat_id,
            message_id=purge_message_id,
            text=_text[_lang]["is_folder_not_drive"],
        )

        return ConversationHandler.END