# coding=utf-8
import leancloud							#requirements leancloud-sdk>=1.0.9,<=2.0.0
import os
import time
import shutil 
import shell as shell
import class_voice as class_voice
import class_subtitle as class_subtitle

SOURCE_ADUIO_FLODER = 'aux/coco'
SOURCE_VOICE_FLODER = 'aux/voice'
SOURCE_ADUIO_EXT = 'm4a'
GIT_VOICE_PATH = 'https://raw.githubusercontent.com/Wayho/BiRadio/master/voice/'
GIT_AUDIO_PATH = 'https://raw.githubusercontent.com/Wayho/BiRadio/master/coco/'
GIT_IMAGE_PATH = 'https://raw.githubusercontent.com/Wayho/BiRadio/master/img/'
IMG_FLODER = 'img'
IMG_EXT = 'jpg'
print('class_curl  v 5.8.3 update_resource:',SOURCE_ADUIO_FLODER,SOURCE_VOICE_FLODER,IMG_FLODER)

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
        if name[-len(IMG_EXT):len(name)]==IMG_EXT:
            jpg = True
            if  os.path.exists(name):
                shutil.copy(name,os.path.join(IMG_FLODER, name))
                os.remove(name)
    shell.OutputShell('ls -l')
    if jpg:
        time.sleep(0.3)
        shell.OutputShell('ls {} -l'.format(IMG_FLODER))
    return len(curl_arr)

def update_resource():
    # return array len
    voice_arr = class_voice.find_curl()
    update_voice(GIT_VOICE_PATH,voice_arr,SOURCE_VOICE_FLODER,SOURCE_ADUIO_EXT)
    audio_arr = class_subtitle.find_curl()
    update_voice(GIT_AUDIO_PATH,audio_arr,SOURCE_ADUIO_FLODER,SOURCE_ADUIO_EXT)
    return True

def update_voice(src_path,res_arr,dest_floder,ext=SOURCE_ADUIO_EXT):
    # return array len
    for item in res_arr:
        name = item.get('m4a')
        dest = os.path.join(dest_floder, name)
        if  os.path.exists(dest):
            print('exist:',dest)
            continue
        url = src_path + name
        cmd = 'curl -O ' + url
        shell.OutputShell(cmd,True)
        names = url.split('/')
        name = names[len(names)-1]
        if name[-len(ext):len(name)]==ext:
            if  os.path.exists(name):
                shutil.copy(name,os.path.join(dest_floder, name))
                os.remove(name)
    shell.OutputShell('ls {} -l'.format(dest_floder))

def update_audio():
    # return array len
    voice_arr = class_voice.find_curl()
    for item in voice_arr:
        name = item.get('m4a')
        dest = os.path.join(SOURCE_VOICE_FLODER, name)
        if  os.path.exists(dest):
            print('exist:',dest)
            continue
        url = GIT_AUDIO_PATH + name
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
        