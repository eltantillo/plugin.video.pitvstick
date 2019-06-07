# -*- coding: utf-8 -*-
import xbmcgui, xbmc
import urllib
import sys
from urllib2 import HTTPError

arg = sys.argv[1]
title, folder, video_url, icon_url, fanart_url = arg.decode('base64').split('|')
progress_bar = xbmcgui.DialogProgressBG()
progress_bar.create('Descargando...', title.decode('utf-8'))


def reporthook(block_number, block_size, total_size):
    if 0 == block_number & 511:
        percent = (block_number * block_size * 100) / total_size
        progress_bar.update(percent)

try:
	urllib.urlretrieve(video_url.decode('utf-8'), folder.decode('utf-8') + 'video.mp4', reporthook)
	urllib.urlretrieve(icon_url.decode('utf-8'), folder.decode('utf-8') + 'icon.png', reporthook)
	urllib.urlretrieve(fanart_url.decode('utf-8'), folder.decode('utf-8') + 'fanart.jpg', reporthook)
	progress_bar.close()
	xbmc.executebuiltin('Notification(PiTVStick, La descarga de {} ha terminado, 5000)'.format(title))
except HTTPError as error:
	progress_bar.close()
	xbmc.executebuiltin('Notification(PiTVStick, Falló la descarga de {}, 5000)'.format(title))
