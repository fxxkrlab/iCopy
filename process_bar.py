# -*- coding: utf-8
import os, re

# ############################## Program Description ##############################
# Latest Modified DateTime : 202006252000 ,
# Version = '0.1.5-beta.1',
# Author : 'FxxkrLab',
# Website: 'https://bbs.jsu.net/c/official-project/icopy/6',
# Code_URL : 'https://github.com/fxxkrlab/iCopy',
# Description= 'Copy GoogleDrive Resources via Telegram BOT',
# Programming Language : Python3',
# License : MIT License',
# Operating System : Linux',
# ############################## Program Description.END ###########################

#转存进程动画设定
#code from steve x
def status(val):
    if val == 0:
        ss = "│░░░░░░░░░░░░░░░░░░░░│"

    if 0 < val <= 35:
        if val < 5:
            ss = "│█░░░░░░░░░░░░░░░░░░░│"

        if 5 <= val <= 10:
            ss = "│██░░░░░░░░░░░░░░░░░░│"

        if 10 < val <= 15:
            ss = "│███░░░░░░░░░░░░░░░░░│"

        if 15 < val <= 20:
            ss = "│████░░░░░░░░░░░░░░░░│"

        if 20 < val <= 25:
            ss = "│█████░░░░░░░░░░░░░░░│"

        if 25 < val <= 30:
            ss = "│██████░░░░░░░░░░░░░░│"

        if 30 < val <= 35:
            ss = "│███████░░░░░░░░░░░░░│"

    if 35 < val <= 70:
        if 35 < val <= 40:
            ss = "│████████░░░░░░░░░░░░│"

        if 40 < val <= 45:
            ss = "│█████████░░░░░░░░░░░│"

        if 45 < val <= 50:
            ss = "│██████████░░░░░░░░░░│"

        if 50 < val <= 55:
            ss = "│███████████░░░░░░░░░│"

        if 55 < val <= 60:
            ss = "│████████████░░░░░░░░│"

        if 60 < val <= 65:
            ss = "│█████████████░░░░░░░│"

        if 65 < val <= 70:
            ss = "│██████████████░░░░░░│"

    if 70 < val <= 100:
        if 70 < val < 75:
            ss = "│███████████████░░░░░│"

        if 75 <= val <= 80:
            ss = "│████████████████░░░░│"

        if 80 < val <= 85:
            ss = "│█████████████████░░░│"

        if 85 < val <= 90:
            ss = "│██████████████████░░│"

        if 90 < val <= 95:
            ss = "│███████████████████░│"

        if 95 < val <= 100:
            ss = "│████████████████████│"

    return ss