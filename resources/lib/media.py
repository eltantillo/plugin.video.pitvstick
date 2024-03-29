# -*- coding: utf-8 -*-
import os
import urllib
import xbmcplugin

from functions import *

def main_menu():
    #add_dir('Televisión', 'tvshows', 'tv', TV, FANART)
    add_dir('Películas', 'movies', 'movies', MOVIES, FANART)
    add_dir('Series', 'movies', 'series', SERIES, FANART)
    add_dir('Anime', 'movies', 'anime', ANIME, FANART)
    if parental_pass != '':
        add_dir('Adultos', 'movies', 'adults', ADULTS, FANART)
    add_dir('Descargas', 'movies', 'downloads', DOWNLOADS, FANART)
    
    add_action('Ajustes', 'settings', SETTINGS, FANART)

def tv_menu():
    add_dir('Televisión abierta', 'tvshows', 'openTv', TV, FANART)
    add_dir('Televisión de paga', 'tvshows', 'cableTv', PAIDTV, FANART)

def anime_menu():
    add_dir('Películas de Anime', 'movies', 'animeMovies', MOVIES, FANART)
    add_dir('Series de Anime', 'movies', 'animeSeries', SERIES, FANART)

def adults_menu():
    if get_pass():
        #add_dir('Televisión Adultos', 'tvshows', 'tvAdults', PAIDTV, FANART)
        add_dir('Películas Adultos', 'movies', 'moviesAdults', MOVIES, FANART)
        add_dir('Series Adultos', 'movies', 'seriesAdults', SERIES, FANART)
        add_dir('Anime Adultos', 'movies', 'animeAdults', ANIME, FANART)

def adults_anime_menu():
    add_dir('Películas de Anime Adultos', 'movies', 'animeMoviesAdults', MOVIES, FANART)
    add_dir('Series de Anime Adultos', 'movies', 'animeSeriesAdults', SERIES, FANART)

def get_tv_channels(cable=False, adults=False):
    tv_url = 'tv.php?'
    if cable:
        tv_url += 'cable&'

    tv_url += 'class=' + get_classifications()
    if adults:
        tv_url += '&adults'

    response = urllib.urlopen(URL + tv_url)
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")
        info = {'originaltitle':data[0],
                'plot':data[4],
                #'mpaa':data[5],
                }

        add_stream(data[0],data[1],'tvshows',data[2],data[3],info)

def get_movies(anime=False, search=None, page=1, adults=False):
    anime_str = ''
    movie_str = 'movies'
    if anime:
        anime_str = 'Anime'
        movie_str = 'animeMovies'
    if adults:
        movie_str += 'Adults'
    add_dir('Buscar películas...', 'movies', 'search{}Movies'.format(anime_str), SEARCH, FANART, adults=adults)

    movies_url = 'movies.php?page={}'.format(page)
    if anime:
        movies_url += '&anime'
    if search != None:
        movies_url += '&search=' + urllib.pathname2url(search)

    movies_url += '&class=' + get_classifications()
    movies_url += '&genre=' + get_genres()
    if adults:
        movies_url += '&adults'

    response = urllib.urlopen(URL + movies_url)
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")
        info = {'title':data[0],
                'originaltitle':data[1],
                'plot':data[5],
                'genre':data[6],
                'year':data[7],
                'duration':data[8],
                #'mpaa':movie['Rating'],
                }

        add_stream(data[0],data[2],'movies', data[3], data[4], info)

    if len(lines) == 25:
        add_dir('Cargar más...', 'movies', movie_str, NEXT, page=int(page)+1)

def search_movies(anime=False, page=1, adults=False):
    search = get_string('Buscar Películas...')
    get_movies(anime, search, page, adults)

def series_menu(anime=False, search=None, page=1, adults=False):
    anime_str = ''
    serie_str = 'series'
    if anime:
        anime_str = 'Anime'
        serie_str = 'animeSeries'
    if adults:
        serie_str += 'Adults'
    add_dir('Buscar series...', 'movies', 'search{}Series'.format(anime_str), SEARCH, FANART, adults=adults)

    series_url = 'series.php?page={}'.format(page)
    if anime:
        series_url += '&anime'
    if search != None:
        series_url += '&search=' + urllib.pathname2url(search)

    series_url += '&class=' + get_classifications()
    series_url += '&genre=' + get_genres()
    if adults:
        series_url += '&adults'

    response = urllib.urlopen(URL + series_url)
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")
        info = {'title':data[1],
                'originaltitle':data[2],
                'plot':data[5],
                'genre':data[6],
                #'year':data[5],
                #'duration':data[6],
                #'mpaa':data[7],
                }
        add_dir(data[1], 'tvshows', 'seasons', data[3], data[4], info, data[0])

    if len(lines) == 25:
        add_dir('Cargar más...', 'movies', serie_str, NEXT, page=int(page)+1)

    xbmcplugin.setContent(addon_handle, 'movies')

def search_series(anime=False, page=1, adults=False):
    search = get_string('Buscar Series...')
    series_menu(anime, search, page, adults)

def get_series_seasons(serie):
    seasons_url = 'seasons.php?id={}'.format(serie)
    response = urllib.urlopen(URL + seasons_url)
    lines = response.readlines()

    if len(lines) == 1:
        data = lines[0].split(" | ")
        get_series_chapters(data[0])
    else:
        for line in lines:
            data = line.split(" | ")
            season_id = data[0]
            season_name = data[1]
            season_logo = data[2]
            season_fanart = data[3]
            season_number = data[4]
            add_dir('{} - Temporada {}'.format(season_name, season_number), 'tvshows', 'episodes', season_logo, season_fanart, {}, season_id)

def get_series_chapters(season):
    chapters_url = 'chapters.php?id={}'.format(season)
    response = urllib.urlopen(URL + chapters_url)
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")

        name = data[0]
        link = data[1]
        logo = data[2]
        fanart = data[3]
        plot = data[4]
        year = data[5]
        duration = data[6]

        info = {'title':name,
                'plot':plot,
                #'genre':data[4],
                'year':year,
                'duration':duration,
                #'mpaa':movie['Rating'],
                }

        add_stream(name,link,'episodes',logo,fanart,info)

def get_downloads():
    directories = next(os.walk(videos_dir))[1]
    for directory in directories:
        name = directory
        directory = videos_dir + directory + '/'
        if os.path.exists(directory + 'movie_data.txt'):
            video  = directory + 'video.mp4'
            icon   = directory + 'icon.png'
            fanart = directory + 'fanart.jpg'

            f = open(directory + "movie_data.txt", "r")
            year = f.readline()
            f.close()

            info = {'title':name,
                    'year':year,
                    }
            add_stream(name, video, 'movies', icon, fanart, info, True)

def get_classifications():
    classsifications = ()
    if xbmcplugin.getSetting(addon_handle, 'class_aa') == 'true':
        classsifications += ('AA',)
    if xbmcplugin.getSetting(addon_handle, 'class_a') == 'true':
        classsifications += ('A',)
    if xbmcplugin.getSetting(addon_handle, 'class_b') == 'true':
        classsifications += ('B',)
    if xbmcplugin.getSetting(addon_handle, 'class_b15') == 'true':
        classsifications += ('B15',)
    if xbmcplugin.getSetting(addon_handle, 'class_c') == 'true':
        classsifications += ('C',)
    if xbmcplugin.getSetting(addon_handle, 'class_d') == 'true':
        classsifications += ('D',)

    return ",".join(classsifications)

def get_genres():
    genres = ()
    if xbmcplugin.getSetting(addon_handle, 'accion') == 'true':
        genres += ('Acción',)
    if xbmcplugin.getSetting(addon_handle, 'sobrenatural') == 'true':
        genres += ('Sobrenatural',)
    if xbmcplugin.getSetting(addon_handle, 'romance') == 'true':
        genres += ('Romance',)
    if xbmcplugin.getSetting(addon_handle, 'suspenso') == 'true':
        genres += ('Suspenso',)
    if xbmcplugin.getSetting(addon_handle, 'terror') == 'true':
        genres += ('Terror',)
    if xbmcplugin.getSetting(addon_handle, 'demonios') == 'true':
        genres += ('Demonios',)
    if xbmcplugin.getSetting(addon_handle, 'ecchi') == 'true':
        genres += ('Ecchi',)
    if xbmcplugin.getSetting(addon_handle, 'harem') == 'true':
        genres += ('Harem',)
    if xbmcplugin.getSetting(addon_handle, 'seinen') == 'true':
        genres += ('Seinen',)
    if xbmcplugin.getSetting(addon_handle, 'hentai') == 'true':
        genres += ('Hentai',)
    if xbmcplugin.getSetting(addon_handle, 'yuri') == 'true':
        genres += ('Yuri',)
    if xbmcplugin.getSetting(addon_handle, 'yaoi') == 'true':
        genres += ('Yaoi',)

    return ",".join(genres)
