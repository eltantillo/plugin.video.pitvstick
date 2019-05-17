# -*- coding: utf-8 -*-
import sys, os
import urllib
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

addon_handle = int(sys.argv[1])
ADDON = xbmcaddon.Addon()
ROOTDIR = ADDON.getAddonInfo('path')
FANART = os.path.join(ROOTDIR,"resources","media","fanart.jpg")
ICON = os.path.join(ROOTDIR,"resources","media","icon.png")

def main_menu():
    add_dir('Televisión', 'tvshows', 'tv', ICON)
    add_dir('Películas', 'movies', 'movies', ICON)
    add_dir('Series', 'tvshows', 'series', ICON)
    add_dir('Anime', 'movies', 'anime', ICON)
    add_dir('Adultos', 'movies', 'adults', ICON)

def tv_menu():
    add_dir('Televisión abierta', 'tvshows', 'openTv', ICON)
    add_dir('Televisión por cable', 'tvshows', 'cableTv', ICON)

def anime_menu():
    add_dir('Series', 'tvshows', 'animeSeries', ICON)
    add_dir('Películas', 'movies', 'animeMovies', ICON)

def get_open_tv_channels():
    response = urllib.urlopen('http://158.69.201.210/pitvstick/openTv.txt')
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")
        info = {'plot':data[3]}

        add_stream(data[0],data[1],'tvshows',data[2],FANART,info)

def get_cable_tv_channels():
    response = urllib.urlopen('http://158.69.201.210/pitvstick/cableTv.txt')
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")
        info = {'plot':data[3]}

        add_stream(data[0],data[1],'tvshows',data[2],FANART,info)

def get_movies():
    response = urllib.urlopen('http://158.69.201.210/pitvstick/movies.txt')
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")
        info = {'originaltitle':data[1],
                'plot':data[4],
                'genre':data[5],
                'year':data[6],
                'title':data[0],
                'duration':data[7],
                #'mpaa':movie['Rating'],
                }

        add_stream(data[0],data[2],'movies',data[3],FANART,info)

def get_anime_movies():
    response = urllib.urlopen('http://158.69.201.210/pitvstick/animeMovies.txt')
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")
        info = {'originaltitle':data[1],
                'plot':data[4],
                'genre':data[5],
                'year':data[6],
                'title':data[0],
                'duration':data[7],
                #'mpaa':movie['Rating'],
                }

        add_stream(data[0],data[2],'movies',data[3],FANART,info)

def get_adults():
    add_stream("Peli","http://161.0.157.5/PLTV/88888888/224/3221227026/03.m3u8",'movies',ICON,FANART,{"plot": "Test plot"})

def series_menu():
    response = urllib.urlopen('http://158.69.201.210/pitvstick/series.txt')
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")
        add_dir(data[0], 'episodes', data[2], data[3], FANART, data[4], data[5])

def anime_series_menu():
    response = urllib.urlopen('http://158.69.201.210/pitvstick/animeSeries.txt')
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")
        add_dir(data[0], 'episodes', data[2], data[3], FANART, data[4], data[5])

def get_series_chapters(serie_id):
    response = urllib.urlopen('http://158.69.201.210/pitvstick/chapters/{}.txt'.format(serie_id))
    lines = response.readlines()
    for line in lines:
        data = line.split(" | ")
        info = {'plot':data[3],
                'genre':data[4],
                'year':data[5],
                'title':data[0],
                'duration':data[6],
                #'mpaa':movie['Rating'],
                }

        add_stream(data[0],data[1],'episodes',data[2],FANART,info)

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


def add_dir(name, mode, id, icon, fanart=None, info=None, genre_id=None):
    xbmc.log(ROOTDIR)
    xbmc.log("ICON IMAGE = "+icon)
    ok = True
    u = sys.argv[0]+"?id="+urllib.quote_plus(id)+"&mode="+str(mode)
    if genre_id is not None: u += "&genre_id=%s" % genre_id
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
