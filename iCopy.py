#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, logging
from utils import load
from telegram import Bot
from telegram.utils.request import Request as TGRequest
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
)
from utils import (
    messages as _msg,
    restricted as _r,
    get_set as _set,
    get_functions as _func,
    task_payload as _payload,
)

from workflow import start_workflow as _start, quick_workflow as _quick, copy_workflow as _copy
from multiprocessing import Process as _mp

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ############################### Main ####################################

def main():
    request = TGRequest(con_pool_size=8)
    bot = Bot(token=f"{load.cfg['tg']['token']}", request=request)
    updater = Updater(bot=bot, use_context=True)

    dp = updater.dispatcher

    # Entry Conversation
    conv_handler = ConversationHandler(
        entry_points=[
            # Entry Points
            CommandHandler("set", _set._setting),
            CommandHandler("start", _start.start),
            CommandHandler("quick", _quick.quick),
            # CommandHandler("copy", copy),
        ],
        states={
            _set.SET_FAV_MULTI: [
                # fav settings function
                MessageHandler(Filters.text, _set._multi_settings_recieved),
            ],
            _start.CHOOSE_MODE: [
                # call function  judged via callback pattern
                CallbackQueryHandler(_quick.quick, pattern="quick"),
                # CallbackQueryHandler(copy, pattern="copy"),
            ],
            _quick.GET_LINK: [
                # get Shared_Link states
                MessageHandler(Filters.text, _func.get_share_link),
            ],
            _set.IS_COVER_QUICK: [
                CallbackQueryHandler(_func.delete_in_db_quick, pattern="cover_quick"),
                CallbackQueryHandler(_func.cancel, pattern="not_cover_quick"),
                MessageHandler(Filters.text, _func.cancel),
            ],
        },
        fallbacks=[CommandHandler("cancel", _func.cancel)],
    )

    dp.add_handler(conv_handler, 2)

    dp.add_handler(CommandHandler("ver", _func._version))

    updater.start_polling()
    logger.info("Fxxkr LAB iCopy v0.2.0a1 Start")
    updater.idle()


if __name__ == "__main__":
    progress = _mp(target=_payload.task_buffer)
    progress.start()

    main()
