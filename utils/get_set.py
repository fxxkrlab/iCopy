#!/usr/bin/python3
# -*- coding: utf-8 -*-

from utils import load, get_functions as _func, messages as _msg, restricted as _r, keyboard as _KB
from telegram.ext import ConversationHandler
from telegram import ParseMode
from utils.load import _lang, _text
from drive.gdrive import GoogleDrive as _gd

SET_FAV_MULTI, CHOOSE_MODE, GET_LINK, IS_COVER_QUICK, GET_DST = range(5)

pick_quick = []
pick_fav = []
unpick_fav = []
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
    elif "quick" or "fav" in entry_cmd:
        ### single quick (drive or folder)
        if len(entry_cmd.splitlines()) == 1:
            each = entry_cmd[4:]
            if " " in entry_cmd:
                each = entry_cmd.replace(" ", "")[4:]
            if "quick" == each[:5]:
                if "quick+" == each[:6]:
                    global pick_quick
                    pick_quick = _func.get_name_from_id(update, each[6:], list_name=pick_quick)
                    insert_fav_quick = _func.insert_to_db_quick(pick_quick, update)
                    if insert_fav_quick == "is_cover":
                        update.effective_message.reply_text(
                            _text[_lang]["is_cover_quick_msg"],
                            parse_mode=ParseMode.MARKDOWN_V2,
                            reply_markup=_KB.is_cover_keyboard(),
                        )

                        return IS_COVER_QUICK

            elif "quick-" == each[:6]:
                _func.delete_in_db_quick
                update.effective_message.reply_text(
                    _text[_lang]["delete_quick_success"]
                )

            ### set fav folder(fav folder could be a drive or folder of GDrive)

            elif "fav" == each[:3]:
                fav_count = load.db_counters.find_one({"_id": "fav_count_list"})
                fav_sum = 0

                if fav_count != None:
                    fav_sum = fav_count['fav_sum']
        
                if "+" == each[3]:
                    global pick_fav
                    pick_fav = _func.get_name_from_id(update, each[4:], list_name=pick_fav)
                    for item in pick_fav:
                        item['fav_type'] = "fav"
                        try:
                            load.fav_col.insert_one(item)
                        except:
                            update.effective_message.reply_text(
                                _text[_lang]["is_set_err"],
                            )
                        else:
                            fav_sum += 1
                            load.db_counters.update({"_id": "fav_count_list"},{"fav_sum":fav_sum},upsert=True)

                    update.effective_message.reply_text(
                        _text[_lang]["set_fav_success"]
                    )

                    pick_fav = []


                if "-" == each[3]:
                    global unpick_fav
                    unpick_fav = _func.get_name_from_id(update, each[4:], list_name=unpick_fav)
                    for item in unpick_fav:
                        delete_request = {"G_ID":item['G_id']}
                        _func.delete_in_db(delete_request)
                    
                    update.effective_message.reply_text(
                        _text[_lang]["delete_fav_success"]
                    )

                    unpick_fav = []


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
        return ConversationHandler.END



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
            _func.delete_in_db_quick
            update.effective_message.reply_text(
                _text[_lang]["delete_quick_success"]
            )


        ### set fav folder(fav folder could be a drive or folder of GDrive)

        elif "fav" == each[:3]:
            fav_count = load.db_counters.find_one({"_id": "fav_count_list"})
            fav_sum = 0

            if fav_count != None:
                fav_sum = fav_count['fav_sum']
    
            if "+" == each[3]:
                global pick_fav
                pick_fav = _func.get_name_from_id(update, each[4:], list_name=pick_fav)
                for item in pick_fav:
                    item['fav_type'] = "fav"
                    try:
                        load.fav_col.insert_one(item)
                    except:
                        update.effective_message.reply_text(
                            _text[_lang]["is_set_err"],
                        )
                    else:
                        fav_sum += 1
                        load.db_counters.update({"_id": "fav_count_list"},{"fav_sum":fav_sum},upsert=True)

                update.effective_message.reply_text(
                    _text[_lang]["set_fav_success"]
                )
                pick_fav = []

            if "-" == each[3]:
                global unpick_fav
                unpick_fav = _func.get_name_from_id(update, each[4:], list_name=unpick_fav)
                for item in unpick_fav:
                    delete_request = {"G_ID":item['G_id']}
                    _func.delete_in_db(delete_request)
                
                update.effective_message.reply_text(
                    _text[_lang]["delete_fav_success"]
                )

                unpick_fav = []

        else:
            if "/cancel" == update.effective_message.text:

                return _func.cancel(update, context)
            else:
                update.effective_message.reply_text(_text[_lang]["get_multi_fav_error"])

            return ConversationHandler.END
