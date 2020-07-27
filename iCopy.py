#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, logging
from telegram import Bot
from telegram.utils.request import Request as TGRequest
from utils import load
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
)
from utils import (
    get_set as _set,
    get_functions as _func,
    task_box as _box,
    task_payload as _payload,
    callback_stage as _stage,
)

from workflow import (
    start_workflow as _start,
    quick_workflow as _quick,
    copy_workflow as _copy,
    size_workflow as _size,
    regex_workflow as _regex,
    purge_workflow as _purge,
    dedupe_workflow as _dedupe,
)
from multiprocessing import Process as _mp, Manager
from threading import Thread
from utils.load import ns


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ############################### Main ####################################

def main():
    ### bot define
    request = TGRequest(con_pool_size=8)
    bot = Bot(token=f"{load.cfg['tg']['token']}", request=request)
    updater = Updater(bot=bot, use_context=True)

    ### judge is restart
    is_restart = load.db_counters.find_one({"_id": "is_restart"})
    if is_restart is not None:
        if is_restart["status"] == 0:
            pass
        else:
            _func.check_restart(bot)

    else:
        load.db_counters.update(
            {"_id": "is_restart"}, {"status": 0}, upsert=True,
        )

    dp = updater.dispatcher

    # Entry Conversation
    conv_handler = ConversationHandler(
        entry_points=[
            # Entry Points
            CommandHandler("set", _set._setting),
            CommandHandler("menu", _start.menu),
            CommandHandler("quick", _quick.quick),
            CommandHandler("copy", _copy.copy),
            CommandHandler("task", _box.taskinfo),
            CommandHandler("size", _size.size),
            CommandHandler("purge", _purge.purge),
            CommandHandler("dedupe", _dedupe.dedupe),
            MessageHandler(
                Filters.regex(pattern=load.regex_entry_pattern), _regex.regex_entry
            ),
        ],

        states={
            _stage.SET_FAV_MULTI: [
                # fav settings function
                MessageHandler(Filters.text, _set._multi_settings_recieved),
            ],
            _stage.CHOOSE_MODE: [
                # call function  judged via callback pattern
                CallbackQueryHandler(_quick.quick, pattern="quick"),
                CallbackQueryHandler(_copy.copy, pattern="copy"),
            ],
            _stage.GET_LINK: [
                # get Shared_Link states
                MessageHandler(Filters.text, _func.get_share_link),
            ],
            _stage.IS_COVER_QUICK: [
                # cover quick setting
                CallbackQueryHandler(_func.modify_quick_in_db, pattern="cover_quick"),
                CallbackQueryHandler(_func.cancel, pattern="not_cover_quick"),
                MessageHandler(Filters.text, _func.cancel),
            ],
            _stage.GET_DST: [
                # request DST
                CallbackQueryHandler(_copy.request_srcinfo),
            ],
            _stage.COOK_ID: [
                # request to COOK ID
                MessageHandler(Filters.text, _size.size_handle),
            ],
            _stage.REGEX_IN: [
                # regex in choose mode
                CallbackQueryHandler(_regex.regex_callback, pattern=r"quick|copy|size"),
            ],
            _stage.REGEX_GET_DST: [
                # regex copy end
                CallbackQueryHandler(_regex.regex_copy_end),
            ],
            _stage.COOK_FAV_TO_SIZE: [CallbackQueryHandler(_size.pre_cook_fav_to_size),],
            _stage.COOK_FAV_PURGE: [CallbackQueryHandler(_purge.pre_to_purge),],
            _stage.COOK_ID_DEDU: [CallbackQueryHandler(_dedupe.dedupe_mode),],
            _stage.COOK_FAV_DEDU: [CallbackQueryHandler(_dedupe.dedupe_fav_mode),],
            _stage.FAV_PRE_DEDU_INFO: [CallbackQueryHandler(_dedupe.pre_favdedu_info)],
        },
        fallbacks=[CommandHandler("cancel", _func.cancel)],
    )

    def stop_and_restart():
        progress.terminate()
        load.myclient.close()
        updater.stop()
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    def restart(update, context):
        restart_msg = update.message.reply_text(load._text[load._lang]["is_restarting"])
        restart_chat_id = restart_msg.chat_id
        restart_msg_id = restart_msg.message_id
        load.db_counters.update_one(
            {"_id": "is_restart"},
            {
                "$set": {
                    "status": 1,
                    "chat_id": restart_chat_id,
                    "message_id": restart_msg_id,
                }
            },
            True,
        )
        Thread(target=stop_and_restart).start()

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", _start.start))
    dp.add_handler(CommandHandler("reset", _box.task_reset))
    dp.add_handler(CommandHandler("kill", _func.taskill))
    dp.add_handler(CommandHandler("ver", _func._version))

    dp.add_handler(
        CommandHandler(
            "restart",
            restart,
            filters=Filters.user(user_id=int(load.cfg["tg"]["usr_id"])),
        )
    )

    dp.add_error_handler(_func.error)

    updater.start_polling()
    logger.info(f"Fxxkr LAB iCopy {load._version} Start")
    updater.idle()


if __name__ == "__main__":
    ns.x = 0
    progress = _mp(target=_payload.task_buffer, args=(ns,))
    progress.start()
    main()
