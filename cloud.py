# coding: utf-8

from leancloud import Engine
from leancloud import LeanEngineError
import shell as shell
import mp3 as mp3
import time
import os
import requests

import class_variable as class_variable
import danmu as danmu
import startlive as startlive
import class_sharekey as class_sharekey
import class_artist as class_artist
import down_123_proxies as download
import class_proxies as class_proxies
import class_curl as class_curl
import mp3 as mp3
import shutil
import psutil
import gc
###########################################################
MP3_ROOT = 'mp3'
SITENAME = os.environ.get('SITENAME') or 'none'
print('SITENAME:',SITENAME)
################# LOAD CONFIG ##############################
BILIBILI_RTMP = "rtmp://"
BILIBILI_CLMY = None
RADIO_NAME = '欧美流行歌曲 | 极其音乐'
CHANGE_RADIO_NAME = False
PLAY_ARTIST = False
FFMPEG_MESSAGE_OUT = False
MP3_TOTAL_PLAY = 30
SLEEP = 120
ERROR_RETRY = 6
MAX_DOWNLOAD = 10

###########################################################
# rtmp://live-push.bilivideo.com/live-bvc/
# ?streamname=live_xxx&key=xxx&schedule=rtmp&pflag=1
###########################################################
# [rtmp @ 0x556dc4983600] Server error: Already publishing
# rtmp://live-push.bilivideo.com/live-bvc/?streamname=live_xxx&key=xxx&schedule=rtmp&pflag=1: Operation not permitted
###########################################################
# rtmp://live-push.bilivideo.com/live-bvc/?streamname=live_xxx&key=xxx&&schedule=rtmp&pflag=1: Input/output error
###########################################################
RTMP_URL_STR = '"rtmp://"'

Global_Can_RestartRadio = True
Global_Danmu_Retry_Times = 0
Global_Retry_Times = 0
Global_minutes = 0

Global_Sleeping = False
Global_Mp3_Info = []
Global_Time_Rtmp_Start = 0      #seconds


engine = Engine()

# after deploy
@engine.define( 'setup' )
def Setup(**params):
    global RTMP_URL_STR
    global BILIBILI_RTMP
    global BILIBILI_CLMY
    global RADIO_NAME
    global CHANGE_RADIO_NAME
    global PLAY_ARTIST
    global FFMPEG_MESSAGE_OUT
    global MP3_TOTAL_PLAY
    global SLEEP
    global ERROR_RETRY
    global MAX_DOWNLOAD
    config = class_variable.get_config()
    print(config)
    if config:
        ## 记得修改为通过startlive.tryStartLive()参数带来BILIBILI_RTMP+BILIBILI_CLMY
        BILIBILI_RTMP = config.get('BILIBILI_RTMP')
        BILIBILI_CLMY = config.get('BILIBILI_CLMY')
        RADIO_NAME = config.get('RADIO_NAME')
        CHANGE_RADIO_NAME = config.get('CHANGE_RADIO_NAME')
        PLAY_ARTIST = config.get('PLAY_ARTIST')
        FFMPEG_MESSAGE_OUT = config.get('FFMPEG_MESSAGE_OUT')
        MP3_TOTAL_PLAY = config.get('MP3_TOTAL_PLAY')
        SLEEP = config.get('SLEEP')
        ERROR_RETRY = config.get('ERROR_RETRY')
        MAX_DOWNLOAD = config.get('MAX_DOWNLOAD')
        if BILIBILI_CLMY:
            RTMP_URL_STR = '\"' + BILIBILI_RTMP + BILIBILI_CLMY + '\"'
    else:
        print('############## ERROR IN LOAD CONFIG ##################')
    print_v()
    class_variable.SaveCookiesFromDB()
    return True

@engine.define( 'remove' )
def cmd_remove(floder,**params):
    download.remove_by_floder(floder)
    return True

@engine.define( 'download' )
def cmd_download(key,**params):
    download.download_by_ShareKey(MAX_DOWNLOAD,key,'9945','temp',SLEEP)
    shell.OutputShell('ls mp3 -R -l')
    return True

@engine.define( 'download_all_key' )
def cmd_download_all_key(**params):
    Setup()
    key_list = class_sharekey.ShareKeyArray(SITENAME)
    for k in key_list:
        if k.get('download'):
            print(k.get('ShareKey'),'down:',k.get('download'),'play:',k.get('play'),k.get('floder'),k.get('artist'),k.get('desc'))
            total_download = download.download_by_ShareKey(MAX_DOWNLOAD,k.get('ShareKey'),k.get('SharePwd'),k.get('floder'),SLEEP)
            if total_download > 0:
                # 只下载一个ShareKey，避免内存超限
                shell.OutputShell('ls mp3 -R -l')
                return True
            time.sleep(20+SLEEP)
    return False

@engine.define( 'play_play' )
# play ShareKey.play==True
def play_play():
    key_list = class_sharekey.ShareKeyArray(SITENAME)
    floder_list = []
    for k in key_list:
        if k.get('play'):
            print(k.get('ShareKey'),'down:',k.get('download'),'play:',k.get('play'),k.get('floder'),k.get('artist'),k.get('desc'))
            floder_list.append(MP3_ROOT + '/' + k.get('floder'))
    return play_floder(floder_list,None,RADIO_NAME)

@engine.define( 'play_artist' )
# play ShareKey.artist==artist.artist
def play_artist():
    radioname=RADIO_NAME
    artist = None
    floder_list = []
    artist_list = class_artist.artist_array(SITENAME)
    key_list = class_sharekey.ShareKeyArray(SITENAME)
    
    for theartist in artist_list:
        artist = theartist.get('artist')
        floder_add = False
        for k in key_list:
            if k.get('artist')==artist:
                print(k.get('ShareKey'),'down:',k.get('download'),'play:',k.get('play'),k.get('floder'),k.get('artist'),k.get('desc'))
                floder_list.append(MP3_ROOT + '/' + k.get('floder'))
                floder_add = True
        if floder_add:
            radioname = theartist.get('radioname')
            class_artist.rank(theartist.get('objectId'))
            break
    return play_floder(floder_list, artist,radioname)

@engine.define( 'play_root' )
# ffmpeg 的唯一入口
# call by play_play /  play_artist
def play_floder(floder_list=[], artist=None,radioname=RADIO_NAME):
    """
    获取floder_list下所有path mp3的串接cmd
    :param floder_list:[fullpath]
    :param total=MP3_TOTAL_PLAY:最多串接文件个数
    :return:
    """
    global Global_Mp3_Info
    global Global_Time_Rtmp_Start
    print('play_floder:',floder_list, artist,radioname)
    # today_sitename = class_variable.get_today_sitename()
    # if today_sitename != SITENAME:
    #     print('Today site name is',today_sitename,',This site is',SITENAME)
    #     return 0
    concat = mp3.cmdconcat_floder(RTMP_URL_STR, floder_list, MP3_TOTAL_PLAY, artist)
    cmd = concat.get('cmd')
    Global_Mp3_Info = concat.get('info')
    Global_Time_Rtmp_Start = int(time.time())
    if CHANGE_RADIO_NAME:
        try:
            res = startlive.getRoomBaseInfo()
            if res.get('code')==0:
                title = res.get('data').get('by_room_ids').get('27791346').get('title')
            if title!=radioname:
                startlive.update_RadioName(radioname)
        except:
            print('play_floder::getRoomBaseInfo::error')
    print_v()
    cmd_memory()
    ret = shell.OutputShell(cmd,FFMPEG_MESSAGE_OUT)
    print('FFMPEG::return:',ret)
    cmd_memory()
    return ret

# 18 */1 7-23 * * ?
# 统一到一个云函数定时1分钟运行
# 需要停止restart_radio任务才能kill_ffmpeg，否则又会启动
@engine.define( 'do_one_minute' )
def do_one_minute( **params ):
    global Global_minutes
    if not BILIBILI_CLMY:
        Setup()
    if Global_minutes % 3 == 0:
        cmd_restart_radio()
    id3_send()
    Global_minutes += 1
    return True

# 28 */5 7-23 * * ?
# 需要停止restart_radio任务才能kill_ffmpeg，否则又会启动
@engine.define( 'restart_radio' )
def cmd_restart_radio( **params ):
    global Global_Sleeping
    global Global_Retry_Times
    today_sitename = class_variable.get_today_sitename()
    if today_sitename != SITENAME:
        if Global_minutes % 60 == 0:
            print('Today site name is',today_sitename,',This site is',SITENAME)
        return False
    requests.get( "http://localhost:3000" )
    procs = shell.procs_info("ffmpeg")
    if procs:
        if Global_minutes % 9 == 0:
            print('restart_radio:',Global_Retry_Times,procs)
        return False
    else:
        if Global_Sleeping:
             print('Sleeping,Not do restart')
        else:
            print('Restart Radio')
            if Global_Retry_Times >= ERROR_RETRY:
                print('Global_Retry_Times >= ERROR_RETRY')
                return False
            playret = 0
            if PLAY_ARTIST:
                playret = play_artist()
            else:
                playret = play_play()
            if -9 == playret:
                return False
            elif 1== playret:
                Global_Retry_Times += 1
                startlive.tryStartLive()
                return True
            elif 0 != playret:
                    Global_Retry_Times += 1
            print('*************** END *******************')
            Global_Sleeping = True
            time.sleep(5)
            Global_Sleeping = False
            return True


# 0 0 2-16 * * ?     
@engine.define( 'reset_retry' )
def cmd_reset_retry( **params ):
    global Global_Retry_Times
    global Global_Danmu_Retry_Times
    global Global_minutes
    print( '***************reset_retry*******************',Global_Retry_Times,Global_Danmu_Retry_Times, Global_minutes)
    Global_Retry_Times = 0
    Global_Danmu_Retry_Times = 0
    Global_minutes = 0
    return True

# before restart_radio
# once a day
# 8 0 7 * * ?
@engine.define( 'startLive' )
def StartLive(**params):
    Setup()
    today_sitename = class_variable.get_today_sitename()
    if today_sitename != SITENAME:
        print('Today site name is',today_sitename,',This site is',SITENAME)
        return False
    res = startlive.tryStartLive()
    cmd_reset_retry()
    if res.get('code')==0 or 1==res.get('code'):
        time.sleep(1)
        cmd_restart_radio()
    return True

# before restart_radio
# once a day
# 8 59 6 * * ?
@engine.define( 'startLive_update_rtmp' )
def startLive_update_rtmp(**params):
    global RTMP_URL_STR
    global BILIBILI_RTMP
    global BILIBILI_CLMY
    Setup()
    today_sitename = class_variable.get_today_sitename()
    if today_sitename != SITENAME:
        print('Today site name is',today_sitename,',This site is',SITENAME)
        return False
    res = startlive.tryStartLive()
    if res.get('code')==0:
        time.sleep(3)
        BILIBILI_RTMP = res.get('rtmp').get('addr')
        BILIBILI_CLMY = res.get('rtmp').get('code')
        if BILIBILI_CLMY:
            RTMP_URL_STR = '\"' + BILIBILI_RTMP + BILIBILI_CLMY + '\"'
        cmd_restart_radio()
    elif res.get('code')==1:
        time.sleep(3)
        cmd_restart_radio()
    return True

@engine.define( 'today_mine' )
def today_mine(**params):
    class_variable.set_today_sitename(SITENAME)
    return True

@engine.define( 'tomorrow_mine' )
def tomorrow_mine(**params):
    class_variable.set_tomorrow_sitename(SITENAME)
    return True

# before restart_radio
# once a week
# 8 58 6 * * ?
@engine.define( 'play_artist_on_off' )
def play_artist_on_off(**params):
    global PLAY_ARTIST
    PLAY_ARTIST = not PLAY_ARTIST
    print('############## PLAY_ARTIST #############',PLAY_ARTIST)
    return True

@engine.define( 'ffmpeg_msgout_on_off' )
def ffmpeg_msgout_on_off(**params):
    global FFMPEG_MESSAGE_OUT
    FFMPEG_MESSAGE_OUT = not FFMPEG_MESSAGE_OUT
    print('############## FFMPEG_MESSAGE_OUT #############',FFMPEG_MESSAGE_OUT)
    return True

# 35 */1 7-23 * * ?
@engine.define( 'id3_send' )
def id3_send(**params):
    global Global_Danmu_Retry_Times
    if 5< Global_Danmu_Retry_Times:
         print('Global_Danmu_Retry_Times>5')
         return False
    procs = shell.procs_info("ffmpeg")
    if not procs:
         if Global_minutes % 30 == 0:
            print('ffmpeg not start')
         return False
    now = int(time.time())
    duration_total = 0
    #print(Global_Mp3_Info)
    for index in range(0,len(Global_Mp3_Info)):
        info = Global_Mp3_Info[index]
        duration_total += info.get('duration')        
        if now-Global_Time_Rtmp_Start-20 < duration_total:
            if info.get('send'):
                return False
            else:
                Global_Mp3_Info[index]['send'] = True
                artist = info.get('artist')
                title = info.get('title')
                
                if title:
                    print(duration_total,title, info.get('path'))
                    code = danmu.send(title)
                    if 0!=code:
                        print('***********danmu::return code:',code,title)
                        Global_Danmu_Retry_Times += 1
                    time.sleep(5)
                if artist:
                    artist = 'by ' + artist
                    print(duration_total,artist, info.get('path'))
                    code = danmu.send(artist)
                    if 0!=code:
                        print('***********danmu::return code:',code,artist)
                        Global_Danmu_Retry_Times += 1
                return True
    return False

# 15 */5 2-16 * * ?
@engine.define( 'ffmpeg_procs' )
def cmd_ffmpeg_procs( **params ):
    procs = shell.procs_info("ffmpeg")
    if procs:
        print(procs)
    else:
         print('ffmpeg_procs:sleep',Global_Sleeping)
    return True

# 到时运行免费时长
# 58 59 23 * * ?
@engine.define( 'ffmpeg_kill' )
def cmd_ffmpeg_kill( **params ):
    shell.kill_ffmpeg(True)
    return True

@engine.define( 'heart' )
def cmd_heart( **params ):
    requests.get( "http://localhost:3000" )
    today_sitename = class_variable.get_today_sitename()
    print('Today site name is',today_sitename,',This site is',SITENAME,Global_minutes)
    return True

# # 待升级
@engine.define( 'curl' )
def cmd_curl( **params ):
    print('class_curl.update_code')
    return class_curl.update_code()

# # 待升级
@engine.define( 'update_proxies' )
def cmd_update_proxies( **params ):
    update_num = class_proxies.update()
    print('class_proxies.update:',update_num)
    return True

@engine.define( 'shell' )
# 调试 {"cmd":"ls -l" }
def cmd_shell( cmd, **params ):
    shell.OutputShell(cmd)
    return True
        
@engine.define( 'ls_mp3' )
def cmd_ls_mp3( **params):
    shell.OutputShell('ls mp3 -R -l')
    return True

@engine.define( 'ls' )
def cmd_ls( **params):
    shell.OutputShell('ls -l')
    return True

@engine.define( 'ps' )
# 调试 {"cmd":"ls -l" }
def cmd_ps( **params ):
    shell.OutputShell('ps -elf')
    return True
        
@engine.define( 'memory' )
def cmd_memory( **params ):
    mem_r = 2**20
    # total, used, free = shutil.disk_usage("/")
    # print("Disk total: %d GiB" % (total // (2**30)))
    # print("Disk used: %d GiB" % (used // (2**30)))
    # print("Disk free: %d GiB" % (free // (2**30)))
    mem = psutil.virtual_memory()
    print('Memory total:',mem.total//mem_r)
    print('Memory available:',mem.available//mem_r)
    print('Memory percent:',mem.percent)
    print('Memory used:',mem.used//mem_r)
    print('Memory free:',mem.free//mem_r)
    print('Memory active:',mem.active//mem_r)
    print('Memory inactive:',mem.inactive//mem_r)
    print('Memory buffers:',mem.buffers//mem_r)
    print('Memory cached:',mem.cached//mem_r)
    print('Memory shared:',mem.shared//mem_r)
    print('Memory slab:',mem.slab//mem_r)
    print('gc.collect()',gc.collect())
    return True

@engine.define( 'print_v' )
def print_v( **params ):
    print(BILIBILI_CLMY,'RADIO_NAME:',RADIO_NAME,'CHANGE_RADIO_NAME:',CHANGE_RADIO_NAME,'PLAY_ARTIST:',PLAY_ARTIST,'FFMPEG_MESSAGE_OUT:',FFMPEG_MESSAGE_OUT,'MP3_TOTAL_PLAY:',MP3_TOTAL_PLAY,'SLEEP:',SLEEP,'ERROR_RETRY:',ERROR_RETRY,'MAX_DOWNLOAD:',MAX_DOWNLOAD,'Global_minutes:',Global_minutes)
    return True