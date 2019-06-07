# -*- coding: utf-8 -*-

import requests, re, sys

def find_multiple_matches(text, pattern):
    return re.findall(pattern, text, re.DOTALL)

def test_video_exists(page_url):
    response = requests.get(page_url)
    if response.status_code == 404:
        return False, config.get_localized_string(70449) % "RapidVideo"
    if not response.text or "urlopen error [Errno 1]" in str(response.status_code):
        if config.is_xbmc():
            return False, config.get_localized_string(70302) % "RapidVideo"
        elif config.get_platform() == "plex":
            return False, config.get_localized_string(70303) % "RapidVideo"
        elif config.get_platform() == "mediaserver":
            return False, config.get_localized_string(70304) % "RapidVideo"
    if "Object not found" in response.text:
        return False, config.get_localized_string(70449) % "RapidVideo"
    if response.status_code == 500:
        return False, config.get_localized_string(70524) % "RapidVideo"

    return True, ""


def get_video_url(page_url):
    video_urls = []
    if test_video_exists(page_url):
        data = requests.get(page_url).text
        post = "confirm.x=77&confirm.y=76&block=1"
        if "Please click on this button to open this video" in data:
            data = requests.get(page_url, post=post).text
        patron = 'https://www.rapidvideo.com/e/[^"]+'
        match = find_multiple_matches(data, patron)
        if match:
            for url1 in match:
                res = find_single_match(url1, '=(\w+)')
                data = requests.get(url1).text
                if "Please click on this button to open this video" in data:
                    data = requests.get(url1, post=post).text
                url = find_single_match(data, 'source src="([^"]+)')
                ext = get_filename_from_url(url)[-4:]
                video_urls.append(['%s %s [rapidvideo]' % (ext, res), url])
        else:
            patron = 'src="([^"]+)" type="video/([^"]+)" label="([^"]+)"'
            match = find_multiple_matches(data, patron)
            if match:
                for url, ext, res in match:
                    video_urls.append(['.%s %s [Rapidvideo]' % (ext, res), url])

    if len(video_urls) > 0:
        video_urls = video_urls[-1][1]

    return video_urls