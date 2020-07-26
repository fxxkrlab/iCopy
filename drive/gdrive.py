#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, logging, random

from glob import glob
from googleapiclient import discovery
from google.oauth2 import service_account
from googleapiclient import errors
from google.auth.transport.requests import Request

from utils import load
logger = logging.getLogger(__name__)
class GoogleDrive:
    def __init__(self):
        service_account_file = random.choice(glob(load.cfg['general']['sa_path'] + '/*.json'))

        credentials = None
        scopes = ['https://www.googleapis.com/auth/drive']

        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=scopes)

        self.service = discovery.build('drive', 'v3', credentials=credentials)

    def drive_list(self):
        result = []
        raw_drives = {}
        page_token = None

        while True:
            try:
                param = {
                    'pageSize': 100,
                }
                if page_token:
                    param['pageToken'] = page_token
                drives = self.service.drives().list(**param).execute()

                result.extend(drives['drives'])
                logger.debug('Received {} drives'.format(len(drives['drives'])))
                page_token = drives.get('nextPageToken')
                if not page_token:
                    break
            except:
                break

        for item in result:
            raw_drives[item['id']] = item['name']
        return raw_drives

    def file_get_name(self, file_id):
        param = {
            'fileId': file_id,
            'supportsAllDrives': True,
            'fields': 'name, driveId',
        }
        raw_file_info = self.service.files().get(**param).execute()
        file_name = raw_file_info['name']

        return file_name

    def drive_get(self, drive_id):
        param = {
            'driveId': drive_id,
        }
        drive_info = self.service.drives().get(**param).execute()
        
        return drive_info

    def get_dst_endpoint_id(self, dst_id, src_name):
        page_token = None
        result = []
        while True:
            try:
                param = {
                    'q': r"name = '{}' and "
                         r"mimeType = 'application/vnd.google-apps.folder' and "
                         r"'{}' in parents and trashed = false".format(src_name, dst_id),
                    'includeItemsFromAllDrives': True,
                    'supportsAllDrives': True,
                    'fields': 'nextPageToken, files(id, name)',
                    'pageSize': 1000,
                }
                if page_token:
                    param['pageToken'] = page_token

                all_files = self.service.files().list(**param).execute()
                result = all_files['files'][0]
                page_token = all_files.get('nextPageToken')

                if not page_token:
                    break
            except:
                break
        return result