# -*- coding: utf-8 -*-

import requests, re, xbmc, urllib


def get_video_url(page_url):
    referer = page_url
    post = {'r': page_url, 'd': 'www.pelisplus.net'}
    post = urllib.urlencode(post)
    video_url = page_url.replace('/v/', '/api/source/')

    url_data = requests.post(video_url, data=post, headers={'Referer': referer}).text
    patron = '"file":"([^"]+)","label":"([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(url_data)

    url = matches[-1][0].replace('\/', '/')
    #r = requests.get(url, timeout=5)
    #link = r.url

    xbmc.log("LINKKKKKKKKKKKKKKKKKKKK: " + url)
    #https://www.pelisplus.net/v/dworr84-pog

    return url
