import re, json, random
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from telegram.ext.dispatcher import run_async
from glob import glob

from settings import sa_path

# ############################## Program Description ##############################
# Author : 'FxxkrLab',
# Website: 'https://bbs.jsu.net/c/official-project/icopy/6',
# Code_URL : 'https://github.com/fxxkrlab/iCopy',
# Description= 'Copy GoogleDrive Resources via Telegram BOT',
# Programming Language : Python3',
# License : MIT License',
# Operating System : Linux',
# ############################## Program Description.END ###########################

d_callback = {}

def credentials_from_file():

    SCOPES = [
        'https://www.googleapis.com/auth/drive'
    ]

    #_sas = glob(sa_path + '/*.json')

    SERVICE_ACCOUNT_FILE = random.choice(glob(sa_path + '/*.json'))

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            
    return credentials


def drive_get(d_id):
    global d_callback
    credentials = credentials_from_file()
    service = build('drive', 'v3', credentials=credentials)
    resp = service.drives().get(driveId="{}".format(d_id)).execute()
    result = str(resp).replace("'", '"')
    result = json.loads(result)
    d_callback[result['id']] = result
    return result
