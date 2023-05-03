# <!-- MADE BY JSMSJ#5252 -->

from google.oauth2 import service_account
# from googleapiclient import discovery
from googleapiclient.discovery import build
# import httplib2
# import google_auth_httplib2
from googleapiclient.errors import HttpError
import config
import re
import urllib.parse as urlparse

from urllib.parse import parse_qs


from tenacity import *

def humanbytes(size: int) -> str:
    if not size:
        return ""
    power = 2 ** 10
    number = 0
    dict_power_n = {
        0: " ",
        1: "K",
        2: "M",
        3: "G",
        4: "T",
        5: "P"
    }
    while size > power:
        size /= power
        number += 1
    return str(round(size, 3)) + " " + dict_power_n[number] + 'B'

def getIdFromUrl(link: str):
    if "folders" in link or "file" in link:
        
            regex = r"https://drive\.google\.com/(drive)?/?u?/?\d?/?(mobile)?/?(file)?(folders)?/?d?/([-\w]+)[?+]?/?(w+)?"
            res = re.search(regex,link)
            if res is None:
                    raise IndexError("GDrive ID not found.")
            return res.group(5)
    parsed = urlparse.urlparse(link)
    return parse_qs(parsed.query)['id'][0]

sa = {
        "client_email":config.client_email,
        "token_uri":config.token_uri,
        "private_key":config.private_key
    }

creds = service_account.Credentials.from_service_account_info(sa,scopes=['https://www.googleapis.com/auth/drive'])

service = build('drive', 'v3', credentials=creds, cache_discovery=False)

class DriveHelp:
    def __init__(self,service) -> None:
        self.service = service

    def get_file(self,file_id):
        drive_file = self.service.files().get(fileId=file_id, fields="id,mimeType,size,name",
                                                supportsTeamDrives=True).execute()
        return drive_file
    
    def list_drive_dir(self, file_id: str) -> list:
        query = f"'{file_id}' in parents and (name contains '*') and trashed=false"
        fields = 'nextPageToken, files(id, mimeType, size,name,modifiedTime)'
        page_token = None
        page_size = 1000
        files = []
        while True:
            response = self.service.files().list(supportsTeamDrives=True,
                                                  includeTeamDriveItems=True,
                                                  q=query, spaces='drive',
                                                  fields=fields, pageToken=page_token,
                                                  pageSize=page_size, corpora='allDrives',
                                                  orderBy='folder, name').execute()
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return files
    

    @retry(wait=wait_exponential(multiplier=2, min=3, max=6), stop=stop_after_attempt(5),
    retry=retry_if_exception_type(HttpError))
    def get_master_parents(self,file_id):
        # print('GETTING PARENTS')
        end=False
        path = []
        parent=file_id
        while not end:
            bef_parent = parent
            parent,fname = self.get_parents(parent)
            # print(parent)
            # print(fname)
            if not parent:
                try:
                    drive = self.service.drives().get(driveId=bef_parent,fields='name,id').execute()
                    fname = drive.get('name')
                    fname = f"[{str(fname)}]"
                except Exception:
                    return None
                end=True
            path.append((fname,str(bef_parent)))
        path.reverse()
        return path
    

    @retry(wait=wait_exponential(multiplier=2, min=3, max=6), stop=stop_after_attempt(5),
    retry=retry_if_exception_type(HttpError))
    def get_parents(self,file_id):
        try:
            # print(11)
            file = self.service.files().get(supportsAllDrives=True, fileId=file_id, fields="name,parents,id").execute()
            # print(1)
            # print(file.get('parents'))
            parents = file.get('parents')
            parent = parents[0]
            name = file.get('name')
            return parent,str(name)
        except Exception as e:
            # print(e)
            return None,'None'
        

    def search_files(self,name,drive_id) -> list:
        query = f" (name contains '{name}') and trashed=false" #'{drive_id}' in parents and
        fields = 'nextPageToken, files(id, mimeType, size,name,modifiedTime)'
        page_token = None
        page_size = 1000
        files = []
        while True:
            response = self.service.files().list(supportsTeamDrives=True,
                                                  includeTeamDriveItems=True,
                                                  q=query, spaces='drive',
                                                  fields=fields, pageToken=page_token,
                                                  pageSize=page_size, corpora='allDrives',
                                                  orderBy='folder, name').execute()
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return files