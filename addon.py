# -*- coding: utf-8 -*-
from resources.lib.globals import *

params = get_params()
id = None
mode = None
media_id = None
page_id = 1

if 'id' in params:
    id = urllib.unquote_plus(params["id"])
if 'mode' in params:
    mode = params["mode"]
if 'media_id' in params:
    media_id = params["media_id"]
if 'page' in params:
    page = params["page"]

if mode is None:
    main_menu()

elif mode == 'tvshows':
    if id == 'tv':
        tv_menu()
    elif id == 'series':
        series_menu(page=page)
    elif id == 'searchSeries':
        search_series(page=page)
    elif id == 'openTv':
        get_tv_channels()
    elif id == 'cableTv':
        get_tv_channels(True)
    elif id == 'animeSeries':
        series_menu(anime=True, page=page)
    elif id == 'searchAnimeSeries':
        search_series(anime=True, page=page)
    elif id == 'seasons':
        get_series_seasons(media_id)

elif mode == 'movies':
    if id == 'movies':
        get_movies(page=page)
    elif id == 'searchMovies':
        search_movies(page=page)
    elif id == 'anime':
        anime_menu()
    elif id == 'searchAnimeMovies':
        search_movies(anime=True, page=page)
    elif id == 'adults':
        if get_pass():
            get_adults()
    elif id == 'animeMovies':
        get_movies(anime=True, page=page)

elif mode == 'episodes':
    get_series_chapters(media_id)

xbmcplugin.endOfDirectory(addon_handle)