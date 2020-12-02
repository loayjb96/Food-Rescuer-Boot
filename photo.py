from config import TOKEN
import requests
import urllib3
import urllib.request
import os


def save_photo_by_path(file_id, dir_path):
    url = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'
    res = requests.get(url)
    print(res, type(res), res.json())
    file_path = res.json()['result']['file_path']
    print("PATH", file_path)
    url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    print("URL", url)
    file_path = file_path.replace('/', '-')
    file_path = file_path.replace("\\", '-')
    full_path = dir_path + file_path
    print("PATH", full_path)
    urllib.request.urlretrieve(url, full_path)
    return full_path
