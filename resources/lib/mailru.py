# -*- coding: utf-8 -*-

import requests, re, xbmc, json


session = requests.Session()

def test_video_exists(page_url):
    data = session.get(page_url).text
    if '"error":"video_not_found"' in data or '"error":"Can\'t find VideoInstance"' in data:
        return False, "[Mail.ru] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    link = ''
    if test_video_exists(page_url):
        cookies = session.cookies.get_dict()
        data = session.get(page_url, cookies=cookies).text
        pos = data.find('"videos":[{"url":"') + 18
        pos2 = pos + data[pos:].find('"')
        link = data[pos:pos2]#.replace('//', 'http://').replace('embed', 'check')

    return link
