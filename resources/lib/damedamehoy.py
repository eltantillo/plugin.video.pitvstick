# -*- coding: utf-8 -*-

import requests, re, xbmc, urllib


def get_video_url(page_url):
    file = page_url.split("#")[1]
    page = requests.get('https://damedamehoy.xyz/details.php?v={}'.format(file)).text

    pos  = page.find('"file":"') + 8
    pos2 = pos + page[pos:].find('"')
    url  = page[pos:pos2].replace("\\", "")

    return url
