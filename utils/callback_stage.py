#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
    COOK_FAV_DEDU,
    FAV_PRE_DEDU_INFO,

) = range(13)