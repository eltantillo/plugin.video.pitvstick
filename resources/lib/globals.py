# -*- coding: utf-8 -*-
import sys, os
import urllib
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

addon_handle = int(sys.argv[1])

ADDON   = xbmcaddon.Addon()
ROOTDIR = ADDON.getAddonInfo('path')

FANART  = os.path.join(ROOTDIR,"resources","media","fanart.jpg")
ICON    = os.path.join(ROOTDIR,"resources","media","icon.png")
SEARCH  = os.path.join(ROOTDIR,"resources","media","search.png")
MOVIES  = os.path.join(ROOTDIR,"resources","media","movies.png")
TV      = os.path.join(ROOTDIR,"resources","media","tv.png")
SERIES  = os.path.join(ROOTDIR,"resources","media","series.png")
ANIME   = os.path.join(ROOTDIR,"resources","media","anime.png")
ADULTS  = os.path.join(ROOTDIR,"resources","media","adults.png")

URL     = 'http://158.69.201.210/pitvstick/'

def main_menu():
    add_dir('Televisión', 'tvshows', 'tv', TV, FANART)
    add_dir('Películas', 'movies', 'movies', MOVIES, FANART)
    add_dir('Series', 'tvshows', 'series', SERIES, FANART)
    add_dir('Anime', 'movies', 'anime', ANIME, FANART)
    # add_dir('Adultos', 'movies', 'adults', ADULTS, FANART)

def tv_menu():
    add_dir('Televisión abierta', 'tvshows', 'openTv', TV, FANART)
    add_dir('Televisión por cable', 'tvshows', 'cableTv', TV, FANART)

def anime_menu():
    add_dir('Películas', 'movies', 'animeMovies', MOVIES, FANART)
    add_dir('Series', 'tvshows', 'animeSeries', SERIES, FANART)

def get_tv_channels(cable=False):
    tv_url = 'tv.php'
    if cable:
        tv_url += '?cable'
    response = urllib.urlopen(URL + tv_url)
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")
        info = {'originaltitle':data[0],
                'plot':data[4],
                #'mpaa':data[5],
                }

        add_stream(data[0],data[1],'tvshows',data[2],data[3],info)

def get_movies(anime=False, search=None):
    anime_str = ''
    if anime:
        anime_str = 'Anime'
    add_dir('Buscar películas', 'movies', 'search{}Movies'.format(anime_str), SEARCH, FANART)

    movies_url = 'movies.php'
    if anime:
        movies_url += '?anime'
    if search:
        if anime:
            movies_url += '&'
        else:
            movies_url += '?'
        movies_url += 'search=' + search

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

        add_stream(data[0],data[2],'movies',data[3], data[4], info)

def search_movies(anime=False):
    search = get_string('Buscar Película')
    get_movies(anime, search)

def get_adults():
    add_stream("Peli","http://161.0.157.5/PLTV/88888888/224/3221227026/03.m3u8",'movies',ICON,FANART,{"plot": "Test plot"})

def series_menu(anime=False, search=None):
    anime_str = ''
    if anime:
        anime_str = 'Anime'
    add_dir('Buscar series', 'tvshows', 'search{}Series'.format(anime_str), SEARCH, FANART)

    series_url = 'series.php'
    if anime:
        series_url += '?anime'
    if search:
        if anime:
            series_url += '&'
        else:
            series_url += '?'
        series_url += 'search=' + search

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
        #add_dir(name, mode, id, icon, fanart=None, info=None, media_id=None):

def search_series(anime=False):
    search = get_string('Buscar Serie')
    series_menu(anime, search)

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
            add_dir('Temporada {}'.format(data[1]), 'episodes', 'seasons', ICON, FANART, {}, data[0])

def get_series_chapters(season):
    chapters_url = 'chapters.php?id={}'.format(season)
    response = urllib.urlopen(URL + chapters_url)
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")
        info = {'title':data[0],
                'plot':data[4],
                #'genre':data[4],
                'year':data[5],
                'duration':data[6],
                #'mpaa':movie['Rating'],
                }

        add_stream(data[0],data[1],'episodes',data[2],data[3],info)

def add_stream(name, id, stream_type, icon, fanart, info=None):
    ok = True
    u=id
    #u=sys.argv[0]+"?id="+urllib.quote_plus(id)+"&mode="+str(103)+"&type="+urllib.quote_plus(stream_type)
    liz=xbmcgui.ListItem(name)
    if fanart == None: fanart = FANART
    liz.setArt({'icon': icon, 'thumb': icon, 'fanart': fanart})
    liz.setProperty("IsPlayable", "true")
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setInfo( type="Video", infoLabels=info)
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz,isFolder=False)
    xbmcplugin.setContent(addon_handle, stream_type)
    return ok


def add_dir(name, mode, id, icon, fanart=None, info=None, media_id=None):
    xbmc.log(ROOTDIR)
    xbmc.log("ICON IMAGE = "+icon)
    ok = True
    u = sys.argv[0]+"?id="+urllib.quote_plus(id)+"&mode="+str(mode)
    if media_id is not None: u += "&media_id=%s" % media_id
    liz=xbmcgui.ListItem(name)
    if fanart is not None: fanart = FANART
    liz.setArt({'icon': icon, 'thumb': icon, 'fanart': fanart})
    if info is not None:
        liz.setInfo( type="Video", infoLabels=info)
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz,isFolder=True)
    xbmcplugin.setContent(addon_handle, 'tvshows')
    return ok

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                    params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                    splitparams={}
                    splitparams=pairsofparams[i].split('=')
                    if (len(splitparams))==2:
                            param[splitparams[0]]=splitparams[1]

    return param

def get_pass():
    if xbmcplugin.getSetting(addon_handle, 'password') == '':
        return(True)

    success = False
    pass_input = get_string('Clave control parental')
    if pass_input == xbmcplugin.getSetting(addon_handle, 'password'):
        success = True
    else:
        xbmc.executebuiltin('Notification(Control parental, La clave es incorrecta, 5000)')

    return(success)

def get_string(heading):
    input = ''
    kb = xbmc.Keyboard('default', 'heading', True)
    kb.setDefault('')
    kb.setHeading(heading)
    kb.setHiddenInput(False)
    kb.doModal()

    if (kb.isConfirmed()):
        input = kb.getText()

    return input