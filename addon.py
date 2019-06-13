# -*- coding: utf-8 -*-
from resources.lib.media import *
from resources.lib.functions import *

if internet_access():
    params = get_params()
    id = None
    mode = None
    media_id = None
    page = 1
    adults = False

    if 'id' in params:
        id = params["id"]
    if 'mode' in params:
        mode = params["mode"]
    if 'media_id' in params:
        media_id = params["media_id"]
    if 'name' in params:
        name = params["name"]
    if 'page' in params:
        page = params["page"]
    if 'adults' in params:
        adults = params["adults"]

    if mode is None:
        main_menu()

    elif mode == 'settings':
        open_settings()

    elif mode == 'play':
        play_video(media_id)

    elif mode == 'download':
        download_video(
            media_id,
            name,
            params["icon"],
            params["fanart"],
            params["year"]
        )

    elif mode == 'delete':
        delete_download(name)

    elif mode == 'tvshows':
        if id == 'tv':
            tv_menu()
        elif id == 'openTv':
            get_tv_channels()
        elif id == 'cableTv':
            get_tv_channels(True)
        elif id == 'seasons':
            get_series_seasons(media_id)
        elif id == 'tvAdults':
            get_tv_channels(True, True)
        elif id == 'episodes':
            get_series_chapters(media_id)

    elif mode == 'movies':
        if id == 'movies':
            get_movies(page=page)
        elif id == 'searchMovies':
            search_movies(page=page, adults=adults)
        elif id == 'series':
            series_menu(page=page)
        elif id == 'searchSeries':
            search_series(page=page, adults=adults)
        elif id == 'anime':
            anime_menu()
        elif id == 'searchAnimeMovies':
            search_movies(anime=True, page=page, adults=adults)
        elif id == 'animeMovies':
            get_movies(anime=True, page=page)
        elif id == 'animeSeries':
            series_menu(anime=True, page=page)
        elif id == 'searchAnimeSeries':
            search_series(anime=True, page=page, adults=adults)

        # Adults section
        elif id == 'adults':
            adults_menu()
        elif id == 'animeAdults':
            adults_anime_menu()
        elif id == 'moviesAdults':
            get_movies(page=page, adults=True)
        elif id == 'animeMoviesAdults':
            get_movies(anime=True, page=page, adults=True)
        elif id == 'seriesAdults':
            series_menu(page=page, adults=True)
        elif id == 'animeSeriesAdults':
            series_menu(anime=True, page=page, adults=True)

        elif id == 'downloads':
            get_downloads()

    xbmcplugin.endOfDirectory(addon_handle)