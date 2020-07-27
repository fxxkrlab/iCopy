#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from telegram.ext import ConversationHandler
from utils.load import _lang, _text, ns
from utils import (
    load,
    restricted as _r,
    get_functions as _func,
    task_box as _box,
    size_payload as _s_payload,
    keyboard as _KB,
    callback_stage as _stage,
)
from drive.gdrive import GoogleDrive as _gd
from multiprocessing import Process as _mp

bot = load.bot
ns.size = 0

@_r.restricted
def size(update, context):
    entry_cmd = update.effective_message.text
    match_cmd = re.search(r"^\/size ([1-9]\d*)$", entry_cmd, flags=re.I)
    if "/size" == entry_cmd:
        update.effective_message.reply_text(_text[_lang]["request_share_link"])

        return _stage.COOK_ID

    elif match_cmd:
        limit_query = load.db_counters.find_one({"_id": "task_list_id"})
        check_query = match_cmd.group(1)
        size_msg = update.effective_message.reply_text(_text[_lang]["ready_to_size"])
        size_chat_id = size_msg.chat_id
        size_message_id = size_msg.message_id

        if int(check_query) <= limit_query["future_id"]:

            check_task = load.task_list.find_one({"_id": int(check_query)})

            if check_task["status"] == 1:
                if "dst_endpoint_link" and "dst_endpoint_id" in check_task:
                    task_id = str(check_query)
                    task_link = check_task["dst_endpoint_link"]
                    endpoint_id = check_task["dst_endpoint_id"]
                    endpoint_name = check_task["src_name"]

                    progress = _mp(
                        target=_s_payload.owner_size,
                        args=(
                            ns,
                            size_chat_id,
                            size_message_id,
                            task_id,
                            task_link,
                            endpoint_id,
                            endpoint_name,
                        ),
                    )
                    progress.start()

                    context.bot.edit_message_text(
                        chat_id=size_chat_id,
                        message_id=size_message_id,
                        text=_text[_lang]["sizing"],
                    )

                    return ConversationHandler.END

                else:
                    dst_endpoint_id = _gd.get_dst_endpoint_id(
                        _gd(), check_task["dst_id"], check_task["src_name"]
                    )
                    if dst_endpoint_id:
                        dst_endpoint_link = r"https://drive.google.com/open?id={}".format(
                            dst_endpoint_id["id"]
                        )

                        load.task_list.update_one(
                            {"_id": int(check_query)},
                            {
                                "$set": {
                                    "dst_endpoint_id": dst_endpoint_id["id"],
                                    "dst_endpoint_link": dst_endpoint_link,
                                },
                            },
                        )

                        task_id = str(check_query)
                        task_link = dst_endpoint_link
                        endpoint_id = dst_endpoint_id["id"]
                        endpoint_name = check_task["src_name"]

                        progress = _mp(
                            target=_s_payload.owner_size,
                            args=(
                                ns,
                                size_chat_id,
                                size_message_id,
                                task_id,
                                task_link,
                                endpoint_id,
                                endpoint_name,
                            ),
                        )
                        progress.start()

                        context.bot.edit_message_text(
                            chat_id=size_chat_id,
                            message_id=size_message_id,
                            text=_text[_lang]["sizing"],
                        )

                        return ConversationHandler.END

                    else:
                        bot.edit_message_text(
                            chat_id=size_chat_id,
                            message_id=size_message_id,
                            text=_text[_lang]["support_error"],
                        )

                        return ConversationHandler.END

            elif check_task["status"] == 0:
                bot.edit_message_text(
                    chat_id=size_chat_id,
                    message_id=size_message_id,
                    text=_text[_lang]["task_is_in_queue"]
                    + "\n"
                    + _text[_lang]["finished_could_be_check"],
                )

                return ConversationHandler.END

            elif check_task["status"] == 2:
                bot.edit_message_text(
                    chat_id=size_chat_id,
                    message_id=size_message_id,
                    text=_text[_lang]["doing"]
                    + "\n"
                    + _text[_lang]["finished_could_be_check"],
                )

                return ConversationHandler.END

        else:
            bot.edit_message_text(
                chat_id=size_chat_id,
                message_id=size_message_id,
                text=_text[_lang]["over_limit_to_check"],
            )

            return ConversationHandler.END

    elif entry_cmd.split(" ")[1].strip() == "fav":
        update.effective_message.reply_text(
            _text[_lang]["request_target_folder"],
            reply_markup=_KB.dst_keyboard(update, context),
        )

        return _stage.COOK_FAV_TO_SIZE


def pre_cook_fav_to_size(update, context):
    get_callback = update.callback_query.data
    size_msg = bot.edit_message_text(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        text=_text[_lang]["ready_to_size"],
        reply_markup=None,
    )
    size_chat_id = size_msg.chat_id
    size_message_id = size_msg.message_id

    fav_info_list = get_callback.split("id+name")
    fav_id = fav_info_list[0]
    fav_name = fav_info_list[1]

    task_id = 0
    task_link = r"https://drive.google.com/open?id={}".format(fav_id)
    endpoint_id = fav_id
    endpoint_name = fav_name

    progress = _mp(
        target=_s_payload.owner_size,
        args=(
            ns,
            size_chat_id,
            size_message_id,
            task_id,
            task_link,
            endpoint_id,
            endpoint_name,
        ),
    )
    progress.start()

    context.bot.edit_message_text(
        chat_id=size_chat_id,
        message_id=size_message_id,
        text=_text[_lang]["sizing"],
    )

    return ConversationHandler.END


def size_handle(update, context):
    tmp_share_name_list = ""
    share_id_list = []
    share_name_list = []
    share_id = update.effective_message.text
    share_id_list = _func.cook_to_id(share_id)
    for item in share_id_list:
        size_msg = update.effective_message.reply_text(_text[_lang]["ready_to_size"])

        size_chat_id = size_msg.chat_id
        size_message_id = size_msg.message_id
        share_name_list += _func.get_src_name_from_id(
            update, item, list_name=tmp_share_name_list
        )
        tmp_share_name_list = ""
        progress = _mp(
            target=_s_payload.simple_size,
            args=(
                ns,
                update,
                context,
                item,
                size_chat_id,
                size_message_id,
                share_name_list,
            ),
        )
        progress.start()

        context.bot.edit_message_text(
            chat_id=size_chat_id,
            message_id=size_message_id,
            text=_text[_lang]["sizing"],
        )

    return ConversationHandler.END

