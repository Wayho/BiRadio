# coding=utf-8
import leancloud							#requirements leancloud-sdk>=1.0.9,<=2.0.0
import os
import time
import shutil 
import shell as shell
import class_voice as class_voice

SOURCE_ADUIO_FLODER = 'aux/coco'
SOURCE_VOICE_FLODER = 'aux/voice'
SOURCE_ADUIO_EXT = 'm4a'
GIT_VOICE_FLODER = 'https://raw.githubusercontent.com/Wayho/BiRadio/master/voice/'
IMG_FLODER = 'img'
IMG_EXT = 'jpg'
print('class_curl  v 5.8.2 cp:m4a,jpg:',SOURCE_VOICE_FLODER,IMG_FLODER)

def update_code():
    # return array len
    m4a = False
    jpg = False
    curl_arr = CurlArray()
    for item in curl_arr:
        url = item.get('url')
        cmd = 'curl -O ' + url
        shell.OutputShell(cmd,True)
        names = url.split('/')
        name = names[len(names)-1]
        if name[-len(SOURCE_ADUIO_EXT):len(name)]==SOURCE_ADUIO_EXT:
            m4a = True
            if  os.path.exists(name):
                shutil.copy(name,os.path.join(SOURCE_VOICE_FLODER, name))
                os.remove(name)
        elif name[-len(IMG_EXT):len(name)]==IMG_EXT:
            jpg = True
            if  os.path.exists(name):
                shutil.copy(name,os.path.join(IMG_FLODER, name))
                os.remove(name)
    update_voice(GIT_VOICE_FLODER)
    shell.OutputShell('ls -l')
    if m4a:
        time.sleep(0.3)
        shell.OutputShell('ls {} -l'.format(SOURCE_ADUIO_FLODER))
    if jpg:
        time.sleep(0.3)
        shell.OutputShell('ls {} -l'.format(IMG_FLODER))
    return len(curl_arr)

def update_voice(floder):
    # return array len
    m4a = False
    jpg = False
    voice_arr = class_voice.get_voice(7)
    for item in voice_arr:
        name = item.get('m4a')
        dest = os.path.join(SOURCE_VOICE_FLODER, name)
        if  os.path.exists(dest):
            continue
        url = GIT_VOICE_FLODER + name
        cmd = 'curl -O ' + url
        shell.OutputShell(cmd,True)
        names = url.split('/')
        name = names[len(names)-1]
        if name[-len(SOURCE_ADUIO_EXT):len(name)]==SOURCE_ADUIO_EXT:
            if  os.path.exists(name):
                shutil.copy(name,os.path.join(SOURCE_VOICE_FLODER, name))
                os.remove(name)
    shell.OutputShell('ls {} -l'.format(SOURCE_VOICE_FLODER))

def CurlArray():
    # return array
    DBClass = leancloud.Object.extend( "curl" )
    query = DBClass.query
    query.equal_to('on', True)
    return query.find()

if __name__ == '__main__':
        a=1
        
