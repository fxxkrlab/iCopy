#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, logging
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

from workflow import start_workflow as _start, quick_workflow as _quick,copy_workflow as _copy
from multiprocessing import Process as _mp
from threading import Thread

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
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
            CommandHandler("copy", _copy.copy),
        ],
        states={
            _set.SET_FAV_MULTI: [
                # fav settings function
                MessageHandler(Filters.text, _set._multi_settings_recieved),
            ],
            _start.CHOOSE_MODE: [
                # call function  judged via callback pattern
                CallbackQueryHandler(_quick.quick, pattern="quick"),
                CallbackQueryHandler(_copy.copy, pattern="copy"),
            ],
            _quick.GET_LINK: [
                # get Shared_Link states
                MessageHandler(Filters.text, _func.get_share_link),
            ],
            _set.IS_COVER_QUICK: [
                CallbackQueryHandler(_func.modify_quick_in_db, pattern="cover_quick"),
                CallbackQueryHandler(_func.cancel, pattern="not_cover_quick"),
                MessageHandler(Filters.text, _func.cancel),
            ],
            _copy.GET_DST: [
                # request DST
                CallbackQueryHandler(_copy.request_srcinfo),
            ]
        },
        fallbacks=[CommandHandler("cancel", _func.cancel)],
    )
    
    def stop_and_restart():
        progress.terminate()
        load.myclient.close()
        updater.stop()
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    def restart(update, context):
        update.message.reply_text(load._text[load._lang]['is_restarting'])
        Thread(target=stop_and_restart).start()

    dp.add_handler(conv_handler, 2)

    dp.add_handler(CommandHandler("ver", _func._version))

    dp.add_handler(CommandHandler('restart', restart,filters=Filters.user(user_id=int(load.cfg['tg']['usr_id']))))

    updater.start_polling()
    logger.info(f"Fxxkr LAB iCopy {load._version} Start")
    updater.idle()


if __name__ == "__main__":
    progress = _mp(target=_payload.task_buffer)
    progress.start()
    main()
