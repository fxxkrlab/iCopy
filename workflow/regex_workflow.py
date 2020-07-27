#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils.load import _lang, _text, ns
from utils import (
    load,
    get_functions as _func,
    restricted as _r,
    keyboard as _KB,
    task_box as _box,
    size_payload as _s_payload,
    callback_stage as _stage,
)
from telegram.ext import CallbackQueryHandler, ConversationHandler
from threading import Thread
from multiprocessing import Process as _mp

ns.size = 0
ns.dedupe = 0
ns.purge = 0

src_name_list = []
src_id_list = []
regex_in_update = None
regex_in_context = None


@_r.restricted
def regex_entry(update, context):
    global src_id_list
    global src_name_list
    src_id_list = []
    src_name_list = []
    tmp_src_name_list = ""
    get_share_link = update.effective_message.text
    src_id_list = _func.cook_to_id(get_share_link)
    for item in src_id_list:
        src_name_list += _func.get_src_name_from_id(
            update, taget_id=item, list_name=tmp_src_name_list
        )
        tmp_src_name_list = ""

    update.effective_message.reply_text(
        _text[_lang]["menu_msg"], reply_markup=_KB.regex_in_keyboard(),
    )

    global regex_in_update
    global regex_in_context
    regex_in_update = update
    regex_in_context = context

    return _stage.REGEX_IN


def regex_callback(update, context):
    if "quick" == update.callback_query.data:
        load.bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text=_text[_lang]["mode_select_msg"].replace(
                "replace", _text[_lang]["quick_mode"]
            ),
            reply_markup=None,
        )

        regex_in_chat_id = regex_in_update.effective_message.chat_id
        regex_in_message_id = regex_in_update.effective_message.message_id
        tmp_task_list = []
        mode = "quick"
        is_quick = {"_id": "fav_quick"}
        is_quick_cur = load.fav_col.find(is_quick)

        if is_quick_cur is not None:
            for doc in is_quick_cur:
                dst_id = doc["G_id"]
                dst_name = doc["G_name"]

        for item in src_name_list:
            src_id = item["G_id"]
            src_name = item["G_name"]

            tmp_task_list.append(
                {
                    "mode_type": mode,
                    "src_id": src_id,
                    "src_name": src_name,
                    "dst_id": dst_id,
                    "dst_name": dst_name,
                    "chat_id": regex_in_chat_id,
                    "raw_message_id": regex_in_message_id,
                }
            )

        Thread(
            target=_box.cook_task_to_db,
            args=(regex_in_update, regex_in_context, tmp_task_list),
        ).start()
        tmp_task_list = []
        return ConversationHandler.END

    if "copy" == update.callback_query.data:
        update.callback_query.edit_message_text(
            _text[_lang]["mode_select_msg"].replace(
                "replace", _text[_lang]["copy_mode"]
            )
            + "\n"
            + _text[_lang]["request_dst_target"],
            reply_markup=_KB.dst_keyboard(update, context),
        )

        return _stage.REGEX_GET_DST

    if "size" == update.callback_query.data:

        for item in src_id_list:
            size_msg = load.bot.edit_message_text(
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id,
                text=_text[_lang]["ready_to_size"],
                reply_markup=None,
            )
            size_chat_id = size_msg.chat_id
            size_message_id = size_msg.message_id

            # to payload
            progress = _mp(
                target=_s_payload.simple_size,
                args=(
                    ns,
                    update,
                    context,
                    item,
                    size_chat_id,
                    size_message_id,
                    src_name_list,
                ),
            )
            progress.start()

            context.bot.edit_message_text(
                chat_id=size_chat_id,
                message_id=size_message_id,
                text=_text[_lang]["sizing"],
            )

        return ConversationHandler.END


def regex_copy_end(update, context):

    load.bot.edit_message_text(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        text=_text[_lang]["mode_select_msg"].replace(
            "replace", _text[_lang]["copy_mode"]
        ),
        reply_markup=None,
    )

    mode = "copy"
    regex_in_chat_id = regex_in_update.effective_message.chat_id
    regex_in_message_id = regex_in_update.effective_message.message_id
    tmp_task_list = []

    is_dstinfo = update.callback_query.data
    dstinfo = is_dstinfo.split("id+name")
    dst_id = dstinfo[0]
    dst_name = dstinfo[1]

    for item in src_name_list:
        src_id = item["G_id"]
        src_name = item["G_name"]

        tmp_task_list.append(
            {
                "mode_type": mode,
                "src_id": src_id,
                "src_name": src_name,
                "dst_id": dst_id,
                "dst_name": dst_name,
                "chat_id": regex_in_chat_id,
                "raw_message_id": regex_in_message_id,
            }
        )

    Thread(
        target=_box.cook_task_to_db,
        args=(regex_in_update, regex_in_context, tmp_task_list),
    ).start()
    dstinfo = ""
    return ConversationHandler.END

