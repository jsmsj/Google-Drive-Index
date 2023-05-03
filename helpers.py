from datetime import datetime
from gdrive import humanbytes


def fix_time(time_str):
    return datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%d-%b-%Y %H:%M")



def parse_files_list(files:list[dict]):
    cleaned = {}
    for i in files:
        cleaned.update({i['name']:{
            'last modified': fix_time(i.get('modifiedTime','2023-01-01T00:00:00.000Z')),
            'id':i.get('id'),
            'size_b':i.get('size',0),
            'size_h': humanbytes(int(i.get('size',0))),
            'mime type':i.get('mimeType')
        }})

    return cleaned
