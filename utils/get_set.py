#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils import load, get_functions as _func, messages as _msg, restricted as _r, keyboard as _KB
from telegram.ext import ConversationHandler
from telegram import ParseMode
from utils.load import _lang, _text
from drive.gdrive import GoogleDrive as _gd

SET_FAV_MULTI, CHOOSE_MODE, GET_LINK, IS_COVER_QUICK = range(4)

pick_quick = []
unpick_quick = []
pick_drive = []
unpick_drive = []
pick_folder = []
unpick_folder = []
judge_folder_len = [28, 33]


@_r.restricted
def _setting(update, context):
    entry_cmd = update.effective_message.text
    if "/set" == entry_cmd.strip():
        update.effective_message.reply_text(
            _msg.set_multi_fav_guide(_lang), parse_mode=ParseMode.MARKDOWN_V2
        )

        return SET_FAV_MULTI

    ### set single DST ID ###
    elif "quick" or "drive" or "folder" in entry_cmd:
        ### single quick (drive or folder)
        if len(entry_cmd.splitlines()) == 1:
            each = entry_cmd.replace(" ", "")[4:]
            if "quick" == each[:5]:
                if "quick+" == each[:6]:
                    global pick_quick
                    pick_quick = _func.get_name_from_id(update, each[6:], list_name=pick_quick)
                    insert_fav_quick = _func.insert_to_db_quick(pick_quick, update)
                    if insert_fav_quick == "error":
                        update.effective_message.reply_text(
                            _text[_lang]["is_cover_quick_msg"],
                            parse_mode=ParseMode.MARKDOWN_V2,
                            reply_markup=_KB.is_cover_keyboard(),
                        )

                        return IS_COVER_QUICK

            elif "quick-" == each[:6]:
                unpick_quick.append(each[6:])

            ### single drive
            elif "drive" == each[:5]:
                if "drive+" == each[:6]:
                    pick_drive.append(
                        {"id": each[6:], "name": load.all_drive[each[6:]]}
                    )
                elif "drive-" == each[:6]:
                    unpick_drive.append(each[6:])

            ### single folder
            elif "folder" == each[:6]:
                if "folder+" == each[:7]:
                    pick_folder.append(
                        {"id": each[7:], "name": _gd().file_get_name(file_id=each[7:])}
                    )
                if "folder-" == each[:7]:
                    unpick_folder.append(each[7:])

            ### single rule
            elif "rule" == entry_cmd.replace(" ", "")[4:8]:
                update.effective_message.reply_text(
                    _msg.set_single_fav_guide(_lang), parse_mode=ParseMode.MARKDOWN_V2
                )

                return ConversationHandler.END
            else:
                update.effective_message.reply_text(
                    _text[_lang]["get_single_fav_error"], parse_mode=ParseMode.MARKDOWN_V2
                )

                return ConversationHandler.END
        else:
            update.effective_message.reply_text(
                _text[_lang]["get_multi_in_single"], parse_mode=ParseMode.MARKDOWN_V2
            )

            return ConversationHandler.END

    else:
        update.effective_message.reply_text(
            _msg.set_help(_lang), parse_mode=ParseMode.MARKDOWN_V2
        )




### set multi DST ID ###
def _multi_settings_recieved(update, context):
    _tmp_quick_counter = 0
    fav_msg = update.effective_message.text
    print(fav_msg)
    fav_msg = fav_msg.strip().replace(" ", "").splitlines()
    global pick_quick
    for each in fav_msg:
        print(each)
        ### modify quick DST
        if "quick+" == each[:6]:
            _tmp_quick_counter += 1
            if _tmp_quick_counter == 1:
                global pick_quick
                pick_quick = _func.get_name_from_id(update, each[6:], list_name=pick_quick)
                insert_fav_quick = _func.insert_to_db_quick(pick_quick, update)
                if insert_fav_quick == "error":
                    update.effective_message.reply_text(
                        _text[_lang]["is_cover_quick_msg"],
                        parse_mode=ParseMode.MARKDOWN_V2,
                        reply_markup=_KB.is_cover_keyboard(),
                    )

                    return IS_COVER_QUICK

            elif _tmp_quick_counter < 1:
                pass
            elif _tmp_quick_counter > 1:
                print("error!")
                update.effective_message.reply_text(_text[_lang]["get_quick_count_invaild"])
        elif "quick-" == each[:6]:
            unpick_quick.append(each[6:])

        ### modify drive DST
        elif "drive" == each[:5]:
            if "drive+" == each[:6]:
                pick_drive.append({"id": each[6:], "name": load.all_drive[each[6:]]})
            elif "drive-" == each[:6]:
                unpick_drive.append(each[6:])

        ### modify folder DST
        elif "folder" == each[:6]:
            if "folder+" == each[:7]:
                pick_folder.append(
                    {"id": each[7:], "name": _gd().file_get_name(file_id=each[7:])}
                )
            if "folder-" == each[:7]:
                unpick_folder.append(each[7:])
        else:
            if "/cancel" == update.effective_message.text:

                return _func.cancel(update, context)
            else:
                update.effective_message.reply_text(_text[_lang]["get_multi_fav_error"])

            return ConversationHandler.END
