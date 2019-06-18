# -*- coding: utf-8 -*-
import sys, os
import urllib
import xbmc, xbmcplugin, xbmcaddon, xbmcgui
import time, _strptime
import datetime
import rapidvideo, mailru, streamango

ADDON   = xbmcaddon.Addon()
ROOTDIR = ADDON.getAddonInfo('path')
URL     = 'http://158.69.201.210/pitvstick/'

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

addon_path = sys.argv[0]
addon_handle = int(sys.argv[1])

plugin_dir = xbmc.translatePath("special://home/addons/plugin.video.pitvstick/")
keymap_xml = xbmc.translatePath("special://profile/keymaps/pitvstick.xml")

videos_dir = xbmcplugin.getSetting(addon_handle, 'download_folder')
parental_pass = xbmcplugin.getSetting(addon_handle, 'password')

if addon_handle == -1:
    f = open(plugin_dir + "settings.txt", "r")
    videos_dir = f.readline()[:-1]
    parental_pass = f.readline()
    f.close()
else:
    f = open(plugin_dir + "settings.txt", "w")
    f.write(videos_dir + '\n')
    f.write(parental_pass)
    f.close()

if videos_dir == '~/videos':
    videos_dir = os.path.expanduser("~") + '/videos/'
    if not(os.path.isdir(videos_dir)):
        os.mkdir(videos_dir)
    
if not(os.path.isfile(keymap_xml)):
    f = open(keymap_xml, "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?><keymap><FullscreenVideo><keyboard><backspace>Stop</backspace><backspace mod="longpress">FullScreen</backspace><escape>Stop</escape><escape mod="longpress">FullScreen</escape></keyboard></FullscreenVideo></keymap>')
    f.close()

def delete_download(name):
    folder = videos_dir + name + '/'
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(folder)
    xbmc.executebuiltin('Notification(PiTVStick, Se ha eliminado {}, 5000)'.format(name))

def download_video(url, name, icon, fanart, year):
    name = sanitize_string(name)
    folder = videos_dir + name + '/'
    if not(os.path.isdir(folder)):
        os.mkdir(folder)
        f = open(folder + "movie_data.txt", "w")
        f.write(year)
        f.close()

    args = '|'.join((name, folder, url, icon, fanart))
    args = args.encode('base64')
    xbmc.executebuiltin(r'xbmc.RunScript({}resources/lib/download.py,'.format(plugin_dir) + args + ')')

def play_video(url):
    if 'rapidvideo.com' in url:
        url = rapidvideo.get_video_url(url)
    elif 'mail.ru' in url:
        url = mailru.get_video_url(url)
    elif 'pelisplus.net' in url:
        url = pelisplus.get_video_url(url)
    elif 'streamango.com' in url:
        url = streamango.get_video_url(url)

    playitem = xbmcgui.ListItem(path=url)
    playitem.setPath(url)
    xbmcplugin.setResolvedUrl(addon_handle, True, playitem)

def add_action(name, mode, icon, fanart=None, info=None):
    url = addon_path+"?mode="+str(mode)

    listitem=xbmcgui.ListItem(name)
    listitem.setArt({'icon': icon, 'thumb': icon, 'fanart': fanart})
    if info != None:
        listitem.setInfo(type="video", infoLabels=info)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=listitem, isFolder=False)
    xbmcplugin.setContent(addon_handle, "video")

def add_stream(name, id, stream_type, icon, fanart, info=None, downloads=False):
    url = addon_path + "?&mode=play&media_id=" + id
    if fanart == None: fanart = FANART

    listitem = xbmcgui.ListItem(name)
    listitem.setArt({'icon': icon, 'thumb': icon, 'fanart': fanart, 'banner': fanart})
    listitem.setProperty("IsPlayable", "true")
    listitem.setInfo(type="video", infoLabels=info)

    if downloads:
        delete_url = addon_path + "?&mode=delete&name=" + name
        listitem.addContextMenuItems([('Eliminar', 'RunPlugin({})'.format(delete_url))])
    else:
        download_url = addon_path + "?&mode=download&media_id=" + id + "&name=" + name + "&icon=" + icon + "&fanart=" + fanart + "&year=" + info['year']
        listitem.addContextMenuItems([('Descargar', 'RunPlugin({})'.format(download_url))])

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=listitem, isFolder=False)
    xbmcplugin.setContent(addon_handle, stream_type)


def add_dir(name, mode, id, icon, fanart=None, info=None, media_id=None, page=1, adults=False):
    url = addon_path+"?id="+urllib.quote_plus(id)+"&mode="+str(mode)
    if media_id is not None: url += "&media_id=%s" % media_id

    url += "&page=%s" % page
    if adults: url += "&adults=%s" % adults

    listitem=xbmcgui.ListItem(name)
    listitem.setArt({'icon': icon, 'thumb': icon, 'fanart': fanart, 'banner': fanart})
    if info is not None: listitem.setInfo(type="Video", infoLabels=info)

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=listitem, isFolder=True)
    xbmcplugin.setContent(addon_handle, mode)

def get_pass():
    if parental_pass == '':
        return(True)

    success = False
    pass_input = get_string('Clave control parental', True)
    if pass_input == parental_pass:
        success = True
    else:
        xbmc.executebuiltin('Notification(Control parental, La clave es incorrecta., 5000)')

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
    if internet_access():
        phone = xbmcplugin.getSetting(addon_handle, 'phone')

        # Teléfono no registrado en el addon
        if phone == '':
            xbmc.executebuiltin('Notification(PiTVStick, Registre su número de teléfono., 5000)')
            open_settings()
        else:
            expiration = urllib.urlopen('http://158.69.201.210/pitvstick/subscription.php?phone={}'.format(phone)).readlines()

            # Teléfono en la base de datos
            if len(expiration) > 0:
                expiration = expiration[0]
                timestamp  = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                timestamp  = datetime.datetime(*(time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")[:6]))
                expiration = datetime.datetime(*(time.strptime(expiration, "%Y-%m-%d %H:%M:%S")[:6]))

                # Cuenta expirada
                if timestamp > expiration:
                    pass
                    xbmc.executebuiltin('Notification(PiTVStick, Su cuenta ha expirado, 5000)')

                    info = {'plot': '''Su cuenta se encuentra suspendida debido a que no tenemos registro de su último pago. Por favor realice un pago de [B]$100(MXN)[/B] utilizando cualquiera de las siguientes opciones:

- Transferencia desde su banca en linea con CLABE Interbancaria [B]127 18001 64800 79464[/B].

- Depósito en su OXXO más cercano al número de tarjeta [B]4198 2101 4671 1055[/B] (se le cobrará una comisión adicional de [B]$10 MXN[/B]).

* [B]IMPORTANTE[/B]: No olvide indicar su número de teléfono [B]{}[/B] como referencia.'''.format(phone)
                            }

                    add_action('Su cuenta ha expirado', 'movies', ICON, FANART, info)
                elif timestamp > expiration - datetime.timedelta( days = 5 ):
                    xbmc.executebuiltin('Notification(PiTVStick, Su cuenta expira en {}, 5000)'.format(str(expiration - timestamp)))
                else:
                    valid = True

            else:
                xbmc.executebuiltin('Notification(PiTVStick, No se encontró el número telefónico., 5000)')
                open_settings()
    else:
        valid = True

    return valid

def internet_access():
    try:
    	urllib.urlopen(URL)
    	return True
    except: 
        xbmc.executebuiltin('Notification(PiTVStick, No se pudo conectar a internet. Revise su conexión., 5000)')
        return False

def encode(code, msg):  
    for k in code:  
        msg = msg.replace(k,code[k])  
    return msg

def sanitize_string(string):
    letters = {":": " -", "\n": "", "\r": ""}
    string = encode(letters, string)
    
    return string

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
                    splitparams=pairsofparams[i].split('=', 1)
                    if (len(splitparams))==2:
                        param[splitparams[0]]=splitparams[1]
                        

    return param