import re
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

from glob import glob

from settings import sa_path

# ############################## Program Description ##############################
# Latest Modified DateTime : 202006220250 ,
# Version = '0.1.3-beta.2',
# Author : 'FxxkrLab',
# Website: 'https://bbs.jsu.net/c/official-project/icopy/6',
# Code_URL : 'https://github.com/fxxkrlab/iCopy',
# Description= 'Copy GoogleDrive Resources via Telegram BOT',
# Programming Language : Python3',
# License : MIT License',
# Operating System : Linux',
# ############################## Program Description.END ###########################

def credentials_from_file():

    SCOPES = [
        'https://www.googleapis.com/auth/drive'
    ]

    SERVICE_ACCOUNT_FILE = glob(sa_path + '/*.json')[0]
    print(SERVICE_ACCOUNT_FILE)

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            
    return credentials

def drive_get(d_id):
    credentials = credentials_from_file()
    service = build('drive', 'v3', credentials=credentials)
    resp = service.drives().get(driveId="{}".format(d_id)).execute()
    result = str(resp)
    symbols = re.compile(r"[{}' ]",flags=re.UNICODE)
    result = symbols.sub("",result).rsplit(":", 3)[3]
    print(result)
    return result