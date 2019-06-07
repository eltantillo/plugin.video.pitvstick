# -*- coding: utf-8 -*-
import sys, os
import urllib, time
import xbmc, xbmcplugin, xbmcgui, xbmcaddon
from datetime import datetime
import rapidvideo
import threading

plugin_dir = xbmc.translatePath("special://home/addons/plugin.video.pitvstick/")
videos_dir = os.path.expanduser("~") + '/videos/'
keymap_xml   = xbmc.translatePath("special://profile/keymaps/pitvstick.xml")
if not(os.path.isfile(keymap_xml)):
    f = open(keymap_xml, "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?><keymap><FullscreenVideo><keyboard><backspace>Stop</backspace><backspace mod="longpress">FullScreen</backspace><escape>Stop</escape><escape mod="longpress">FullScreen</escape></keyboard></FullscreenVideo></keymap>')
    f.close()
if not(os.path.isdir(videos_dir)):
    os.mkdir(videos_dir)

addon_handle = int(sys.argv[1])

ADDON   = xbmcaddon.Addon()
ROOTDIR = ADDON.getAddonInfo('path')

FANART = os.path.join(ROOTDIR,"resources","media","fanart.jpg")

ICON      = os.path.join(ROOTDIR,"resources","media","icon.png")
SEARCH    = os.path.join(ROOTDIR,"resources","media","search.png")
MOVIES    = os.path.join(ROOTDIR,"resources","media","movies.png")
TV        = os.path.join(ROOTDIR,"resources","media","tv.png")
PAIDTV    = os.path.join(ROOTDIR,"resources","media","paidtv.png")
SERIES    = os.path.join(ROOTDIR,"resources","media","series.png")
ANIME     = os.path.join(ROOTDIR,"resources","media","anime.png")
ADULTS    = os.path.join(ROOTDIR,"resources","media","adults.png")
NEXT      = os.path.join(ROOTDIR,"resources","media","next.png")
DOWNLOADS = os.path.join(ROOTDIR,"resources","media","downloads.png")
SETTINGS  = os.path.join(ROOTDIR,"resources","media","settings.png")

URL     = 'http://158.69.201.210/pitvstick/'

def main_menu():
    #add_dir('Televisión', 'tvshows', 'tv', TV, FANART)
    add_dir('Películas', 'movies', 'movies', MOVIES, FANART)
    add_dir('Series', 'tvshows', 'series', SERIES, FANART)
    add_dir('Anime', 'movies', 'anime', ANIME, FANART)
    if xbmcplugin.getSetting(addon_handle, 'password') != '':
        add_dir('Adultos', 'movies', 'adults', ADULTS, FANART)
    add_dir('Descargas', 'movies', 'downloads', DOWNLOADS, FANART)
    add_dir('Ajustes', 'settings', 'settings', SETTINGS, FANART)

def tv_menu():
    add_dir('Televisión abierta', 'tvshows', 'openTv', TV, FANART)
    add_dir('Televisión de paga', 'tvshows', 'cableTv', PAIDTV, FANART)

def anime_menu():
    add_dir('Películas de Anime', 'movies', 'animeMovies', MOVIES, FANART)
    add_dir('Series de Anime', 'tvshows', 'animeSeries', SERIES, FANART)

def adults_menu():
    if get_pass():
        #add_dir('Televisión Adultos', 'tvshows', 'tvAdults', PAIDTV, FANART)
        add_dir('Películas Adultos', 'movies', 'moviesAdults', MOVIES, FANART)
        add_dir('Series Adultos', 'tvshows', 'seriesAdults', SERIES, FANART)
        add_dir('Anime Adultos', 'movies', 'animeAdults', ANIME, FANART)

def adults_anime_menu():
    add_dir('Películas de Anime Adultos', 'movies', 'animeMoviesAdults', MOVIES, FANART)
    add_dir('Series de Anime Adultos', 'tvshows', 'animeSeriesAdults', SERIES, FANART)

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
    add_dir('Buscar series...', 'tvshows', 'search{}Series'.format(anime_str), SEARCH, FANART, adults=adults)

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
        add_dir('Cargar más...', 'tvshows', serie_str, NEXT, page=int(page)+1)

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
            add_dir('{} - Temporada {}'.format(season_name, season_number), 'episodes', 'seasons', season_logo, season_fanart, {}, season_id)

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

        add_stream(name,link,'play',logo,fanart,info)

def get_downloads():
    directories = next(os.walk(videos_dir))[1]
    for directory in directories:
        info = {'title':directory,
                'plot':'asd',
                #'genre':data[4],
                'year':'2014',
        #        'duration':duration,
                #'mpaa':movie['Rating'],
                }
        video  = videos_dir + directory + '/video.mp4'
        icon   = videos_dir + directory + '/icon.png'
        fanart = videos_dir + directory + '/fanart.jpg'
        xbmc.executebuiltin('Notification(Control parental, {}, 5000)'.format(video))
        add_stream(directory, video, 'play', icon, fanart, info)

def download_video(url, name, icon, fanart):
    folder = videos_dir + name + '/'
    if not(os.path.isdir(folder)):
        os.mkdir(folder)

    args = '|'.join((name, folder, url, icon, fanart))
    args = args.encode('base64')
    xbmc.executebuiltin(r'xbmc.RunScript({}resources/lib/download.py,'.format(plugin_dir) + args + ')')

def play_video(url):
    if 'rapidvideo.com' in url:
        url = rapidvideo.get_video_url(url)

    playitem = xbmcgui.ListItem(path=url)
    playitem.setPath(url)
    xbmcplugin.setResolvedUrl(addon_handle, True, playitem)

def add_stream(name, id, stream_type, icon, fanart, info=None):
    url = sys.argv[0] + "?&mode=play&media_id=" + id
    if fanart == None: fanart = FANART

    download_url = sys.argv[0] + "?&mode=download&media_id=" + id + "&name=" + name + "&icon=" + icon + "&fanart=" + fanart
    listitem = xbmcgui.ListItem(name)
    listitem.addContextMenuItems([('Descargar', 'XBMC.RunPlugin({})'.format(download_url))])
    listitem.setArt({'icon': icon, 'thumb': icon, 'fanart': fanart})
    listitem.setProperty("IsPlayable", "true")
    listitem.setInfo(type="Video", infoLabels=info)

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=listitem, isFolder=False)
    xbmcplugin.setContent(addon_handle, stream_type)


def add_dir(name, mode, id, icon, fanart=None, info=None, media_id=None, page=1, adults=False):
    url = sys.argv[0]+"?id="+urllib.quote_plus(id)+"&mode="+str(mode)
    if media_id is not None: url += "&media_id=%s" % media_id

    url += "&page=%s" % page
    if adults: url += "&adults=%s" % adults

    listitem=xbmcgui.ListItem(name)
    listitem.setArt({'icon': icon, 'thumb': icon, 'fanart': fanart})
    if info is not None: listitem.setInfo(type="Video", infoLabels=info)

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=listitem, isFolder=True)
    xbmcplugin.setContent(addon_handle, 'tvshows')

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


def get_pass():
    if xbmcplugin.getSetting(addon_handle, 'password') == '':
        return(True)

    success = False
    pass_input = get_string('Clave control parental', True)
    if pass_input == xbmcplugin.getSetting(addon_handle, 'password'):
        success = True
    else:
        xbmc.executebuiltin('Notification(Control parental, La clave es incorrecta, 5000)')

    return(success)

def get_string(heading, password=False):
    input = ''
    kb = xbmc.Keyboard('default', 'heading', True)
    kb.setDefault('')
    kb.setHeading(heading)
    kb.setHiddenInput(password)
    kb.doModal()

    if (kb.isConfirmed()):
        input = kb.getText()

    return input

def open_settings():
    if get_pass():
        ADDON.openSettings()

def check_subscription():
    valid = False
    phone = xbmcplugin.getSetting(addon_handle, 'phone')

    # Teléfono no registrado en el addon
    if phone == '':
        xbmc.executebuiltin('Notification(PiTVStick, Registre su número de teléfono, 5000)')
        open_settings()
    else:
        expiration = urllib.urlopen('http://158.69.201.210/pitvstick/subscription.php?phone={}'.format(phone)).readlines()

        # Teléfono en la base de datos
        if len(expiration) > 0:
            expiration = expiration[0]
            timestamp  = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            timestamp  = time.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            expiration = time.strptime(expiration, '%Y-%m-%d %H:%M:%S')

            # Cuenta expirada
            if timestamp > expiration:
                pass
                xbmc.executebuiltin('Notification(PiTVStick, Su cuenta ha expirado, 5000)')

                info = {'plot': '''Su cuenta se encuentra suspendida debido a que no tenemos registro de su último pago.

Por favor haga un depósito de $100(MXN) al número de tarjeta 1234-5678-9123-4567 en su OXXO más cercano (se le cobrará una comisión de $10 MXN).

No olvide mandar un Whatsapp con su número de teléfono {} y una foto de su recibo al número (656)-412-6134'''.format(phone)
#dar su número de teléfono {} como número de referencia o
                        }

                add_stream('Su cuenta ha expirado','movies','movies',ICON,FANART,info)
            else:
                valid = True

        else:
            xbmc.executebuiltin('Notification(PiTVStick, No se encontró el número telefónico, 5000)')
            open_settings()

    return valid