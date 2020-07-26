from utils.load import _lang, _text
from utils import load, restricted as _r, keyboard as _KB, purge_payload as _p_payload
from multiprocessing import Process as _mp
from telegram.ext import ConversationHandler

(
    SET_FAV_MULTI,
    CHOOSE_MODE,
    GET_LINK,
    IS_COVER_QUICK,
    GET_DST,
    COOK_ID,
    REGEX_IN,
    REGEX_GET_DST,
    COOK_FAV_TO_SIZE,
    COOK_FAV_PURGE,
    COOK_ID_DEDU,
) = range(11)

bot = load.bot

def purge(update, context):
    update.effective_message.reply_text(
        _text[_lang]["mode_select_msg"].replace(
            "replace", _text[_lang]["purge_mode"]
        )
        + "\n"
        + _text[_lang]["request_target_folder"],
        reply_markup=_KB.dst_keyboard(update, context),
    )

    return COOK_FAV_PURGE

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

    progress = _mp(
        target=_p_payload.purge_fav,
        args=(
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