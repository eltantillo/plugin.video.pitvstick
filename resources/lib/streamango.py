# -*- coding: utf-8 -*-

import requests, re, xbmc


def find_multiple_matches(text, pattern):
    return re.findall(pattern, text, re.DOTALL)

def decode(encoded, code):
    _0x59b81a = ""
    k = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    k = k[::-1]

    count = 0

    for index in range(0, len(encoded) - 1):
        while count <= len(encoded) - 1:
            _0x4a2f3a = k.index(encoded[count])
            count += 1
            _0x29d5bf = k.index(encoded[count])
            count += 1
            _0x3b6833 = k.index(encoded[count])
            count += 1
            _0x426d70 = k.index(encoded[count])
            count += 1

            _0x2e4782 = ((_0x4a2f3a << 2) | (_0x29d5bf >> 4))
            _0x2c0540 = (((_0x29d5bf & 15) << 4) | (_0x3b6833 >> 2))
            _0x5a46ef = ((_0x3b6833 & 3) << 6) | _0x426d70
            _0x2e4782 = _0x2e4782 ^ code

            _0x59b81a = str(_0x59b81a) + chr(_0x2e4782)

            if _0x3b6833 != 64:
                _0x59b81a = str(_0x59b81a) + chr(_0x2c0540)
            if _0x3b6833 != 64:
                _0x59b81a = str(_0x59b81a) + chr(_0x5a46ef)

    return _0x59b81a

def test_video_exists(page_url):
    data = requests.get(page_url).text
    if "We are unable to find the video" in data:
        return False, config.get_localized_string(70449) % "Streamango"

    return True, ""


def get_video_url(page_url):
    video_urls = []
    if test_video_exists(page_url):
        data = requests.get(page_url).text
        matches = find_multiple_matches(data, "type:\"video/([^\"]+)\",src:d\('([^']+)',(.*?)\).+?height:(\d+)")

        for ext, encoded, code, quality in matches:

            media_url = decode(encoded, int(code))
            media_url = media_url.replace("@","")
            if not media_url.startswith("http"):
                media_url = "http:" + media_url
            video_urls.append([".%s %sp [streamango]" % (ext, quality), media_url])

        video_urls.reverse()

    if len(video_urls) > 0:
        video_urls = video_urls[-1][1]

    return video_urls
