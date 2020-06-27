import os

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
# ############################## Program Description.END ##########################

# NOTICE :: iCopy设置中 < ' JSUSPLIT ' > 为一个识别度高的命令分隔符请不要删除
# NOTICE :: 基础设置只需要填写 Global Auth 与 Pre-Configuration 部分内容

# ############################## Global Auth ######################################

_token = "这里填写机器人Token"

_usr_id = "这里填写个人 id 应为全数字"

# ############################## Global Auth.END ##################################


# ############################## Pre-Configuration ################################

# rclone / gclone
Clone = "填写你使用的程序"

# e.g. "gc"
Remote = "填写配置名"

# Folder Id / Drive Id
Pre_Dst_id = "Quick 模式预定 Dst ID"

# 自定义 Transfers 数,default = "10",
Parallel_NUM = "10"

#Service Accounts 所在文件夹路径 尾部 "不" 需要 "/" 斜杠
sa_path = "Service Accounts 文件所在路径"

# ############################## Pre-Configuration.END #############################


# ################################## Load Settings #################################

TOKEN = os.environ.get("TELEGRAM_API_TOKEN", "{}").format(_token)

ENABLED_USERS = os.environ.get("ENABLED_USERS", '{}').format(_usr_id)
ENABLED_USERS = set(int(e.strip()) for e in ENABLED_USERS.split(','))

# Run_Mode 中 "-P" 为必须参数, 请不要删除
Run_Mode = "--drive-server-side-across-configs' JSUSPLIT '-P' JSUSPLIT '--ignore-existing"

TRANSFER = "--transfers' JSUSPLIT '{}".format(Parallel_NUM)

# ################################ Load Settings.END ###############################


# ################################ unused variable ###############################

# Shared Drive IDs for future verion
shared_drive = "Is not used in current version"

# Authorized from Account Credentials via OAuth2
cred_path = ""