# -*- coding: utf-8 -*-
from resources.lib.globals import *

params = get_params()
media_id = None
mode = None

if 'id' in params:
    media_id = urllib.unquote_plus(params["id"])
if 'mode' in params:
    mode = params["mode"]

if mode is None:
    main_menu()

elif mode == 'tvshows':
    if media_id == 'tv':
        tv_menu()
    elif media_id == 'series':
        series_menu()
    elif media_id == 'openTv':
        get_open_tv_channels()
    elif media_id == 'cableTv':
        get_cable_tv_channels()
    elif media_id == 'animeSeries':
        anime_series_menu()

elif mode == 'movies':
    if media_id == 'movies':
        get_movies()
    elif media_id == 'anime':
        anime_menu()
    elif media_id == 'adults':
        get_adults()
    elif media_id == 'animeMovies':
        get_anime_movies()

elif mode == 'episodes':
    get_series_chapters(media_id)

xbmcplugin.endOfDirectory(addon_handle)