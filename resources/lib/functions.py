# -*- coding: utf-8 -*-
import sys, os
import urllib
import xbmc, xbmcplugin

URL = 'http://158.69.201.210/pitvstick/'

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
            xbmc.executebuiltin('Notification(PiTVStick, No se encontró el número telefónico., 5000)')
            open_settings()

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
                    splitparams=pairsofparams[i].split('=')
                    if (len(splitparams))==2:
                            param[splitparams[0]]=splitparams[1]

    return param