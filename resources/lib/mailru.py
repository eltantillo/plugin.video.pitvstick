# -*- coding: utf-8 -*-

import requests, re, xbmc, json


session = requests.Session()

def test_video_exists(page_url):
    data = session.get(page_url).text
    if '"error":"video_not_found"' in data or '"error":"Can\'t find VideoInstance"' in data:
        return False, "[Mail.ru] El archivo no existe o ha sido borrado"

    return True, ""

def get_video_url(page_url):
    link = ''
    meta_url = page_url.replace('video/embed', '+/video/meta')
    if test_video_exists(meta_url):
        cookies = session.cookies.get_dict()
        data = session.get(meta_url).text
        pos = data.find('"videos":[{"url":"') + 18
        pos2 = pos + data[pos:].find('"')
        link = data[pos:pos2].replace('//', 'http://') + '|Referer=https://my1.imgsmail.ru/r/video2/uvpv3.swf?75&Cookie=video_key=' + cookies['video_key']

    return link
