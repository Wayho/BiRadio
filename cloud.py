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
#import shutil
import psutil
import gc
import threading
###########################################################
MP3_ROOT = '/tmp'
SITENAME = os.environ.get('SITENAME') or 'none'
MEMORY = os.environ.get('MEMORY') or 'none'
print('cloud v1.0 SITENAME:',SITENAME,'MEMORY:',MEMORY)
################# LOAD CONFIG ##############################
BILIBILI_RTMP = "rtmp://"
BILIBILI_CLMY = None
RADIO_NAME = 'Live Music | 极其音乐'
CHANGE_RADIO_NAME = False
PLAY_ARTIST = False
FFMPEG_MESSAGE_OUT = False
MP3_TOTAL_PLAY = 30
SLEEP = 120
ERROR_RETRY = 6
MAX_DOWNLOAD = 10
MAX_MEMORY = 120

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

Global_Mp3_Info = []
Global_Time_Rtmp_Start = 0      #seconds
Global_Today_AP = ['','']


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
    global MAX_MEMORY
    global Global_Today_AP
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
        #if 'BiliRadio_py' == SITENAME:
        if '512' == MEMORY[0:3]:
            MAX_MEMORY = config.get('MAX_MEMORY_PY')
        else:
            MAX_MEMORY = config.get('MAX_MEMORY')
        if BILIBILI_CLMY:
            RTMP_URL_STR = '\"' + BILIBILI_RTMP + BILIBILI_CLMY + '\"'
    else:
        print('############## ERROR IN LOAD CONFIG ##################')
    (today,tomorrow) = class_variable.get_today_AP()
    Global_Today_AP = today
    print_v()
    class_variable.SaveCookiesFromDB()
    return True

@engine.define( 'remove' )
def cmd_remove(floder,**params):
    download.remove_by_floder(floder)
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
                cmd_ls_mp3()
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
    concat = mp3.cmdconcat_floder(RTMP_URL_STR, floder_list, MP3_TOTAL_PLAY, artist,MAX_MEMORY)
    cmd = concat.get('cmd')
    Global_Mp3_Info = concat.get('info')
    Global_Time_Rtmp_Start = int(time.time())
    if CHANGE_RADIO_NAME:
        try:
            res = startlive.getRoomBaseInfo()
            if res.get('code')==0:
                title = res.get('data').get('by_room_ids').get('27791346').get('title')
                if artist:
                    if title!=radioname:
                        startlive.update_RadioName(radioname)
                else:
                    if title!=RADIO_NAME:
                        startlive.update_RadioName(RADIO_NAME)
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
    global Global_Today_AP
    if not BILIBILI_CLMY:
        Setup()
    if SITENAME in Global_Today_AP:
        procs = shell.procs_info("ffmpeg")
        if procs:
            id3_send()
            if Global_minutes % 20 == 0:
                print('do_one_minute:',Global_Retry_Times,procs)
                requests.get( "http://localhost:3000" )
        else:
            cmd_restart_radio()
    else:
        if Global_minutes % 5 == 0:
            (today,tomorrow) = class_variable.get_today_AP()
            Global_Today_AP = today
            if Global_minutes % 59 == 0:
                print('This site is',SITENAME,'Today:',today,'Tomorrow:',tomorrow,Global_minutes)
    
    Global_minutes += 1
    return True

def cmd_restart_radio():
    global Global_Retry_Times
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
# once a day, not do call ffmpeg, only startlive
# 8 0 7 * * ?
# 确保每台推流机在do_one_minute()启动之前执行两次，以解决空机问题
@engine.define( 'startLive' )
def StartLive(**params):
    startLive_thread = threading.Thread(target=tryStartLive,args=(False,))
    startLive_thread.start()
    return True

# before restart_radio
# once a day
# 8 59 6 * * ?
@engine.define( 'startLive_update_rtmp' )
def startLive_update_rtmp(**params):
    startLive_thread = threading.Thread(target=tryStartLive,args=(True,))
    startLive_thread.start()
    return True

def tryStartLive(rtmp=False):
    global RTMP_URL_STR
    global BILIBILI_RTMP
    global BILIBILI_CLMY
    Setup()
    cmd_reset_retry()
    if not canStart():
        time.sleep(30)
        if canStart():
            res = startlive.tryStartLive()
            if rtmp:
                if res.get('code')==0:
                    BILIBILI_RTMP = res.get('rtmp').get('addr')
                    BILIBILI_CLMY = res.get('rtmp').get('code')
                    if BILIBILI_CLMY:
                        RTMP_URL_STR = '\"' + BILIBILI_RTMP + BILIBILI_CLMY + '\"'

def canStart():
    (today,tomorrow) = class_variable.get_today_AP()
    if not SITENAME in today:
        print('This site is',SITENAME,'Today:',today,'Tomorrow:',tomorrow,Global_minutes)
        return False
    tmpfilenum = os.listdir(MP3_ROOT)
    print('os.listdir(MP3_ROOT)',tmpfilenum)
    if 3>= len(tmpfilenum):
        # 没有音频，切换备用推流机
        if 'a'==SITENAME[len(SITENAME)-2]:
            class_variable.set_today_AP('BiliRadio_ay',True)
        else:
            class_variable.set_today_AP('BiliRadio_py',False)
        print('#'*40,'EMPTY VIDEO,SET TO DEFAULT','#'*40)
        return False
    return True

@engine.define( 'today_am_mine' )
def today_am_mine(**params):
    class_variable.set_today_AP(SITENAME,True)
    return True

@engine.define( 'today_pm_mine' )
def today_pm_mine(**params):
    class_variable.set_today_AP(SITENAME,False)
    return True

@engine.define( 'tomorrow_am_mine' )
def tomorrow_am_mine(**params):
    class_variable.set_tomorrow_AP(SITENAME,True)
    return True

@engine.define( 'tomorrow_pm_mine' )
def tomorrow_pm_mine(**params):
    class_variable.set_tomorrow_AP(SITENAME,False)
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
#@engine.define( 'id3_send' )
def id3_send():
    global Global_Danmu_Retry_Times
    if 5< Global_Danmu_Retry_Times:
         print('Global_Danmu_Retry_Times>5')
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
                #artist = info.get('artist')
                title = info.get('title')
                
                if title:
                    print(duration_total,title, info.get('path'))
                    code = danmu.send(title)
                    if 0!=code:
                        print('***********danmu::return code:',code,title)
                        Global_Danmu_Retry_Times += 1
                #     time.sleep(5)
                # if artist:
                #     artist = 'by ' + artist
                #     print(duration_total,artist, info.get('path'))
                #     code = danmu.send(artist)
                #     if 0!=code:
                #         print('***********danmu::return code:',code,artist)
                #         Global_Danmu_Retry_Times += 1
                return True
    return False


# 到时运行免费时长
# 58 59 23 * * ?
@engine.define( 'kill_ffmpeg' )
def cmd_kill_ffmpeg( **params ):
    shell.proc_kill('ffmpeg',True)
    return True

# restart engine
@engine.define( 'kill_python' )
def cmd_kill_python( **params ):
    shell.proc_kill('python',False)
    return True

@engine.define( 'heart' )
def cmd_heart( **params ):
    requests.get( "http://localhost:3000" )
    (today,tomorrow) = class_variable.get_today_AP()
    print('This site is',SITENAME,'Today:',today,'Tomorrow:',tomorrow,Global_minutes)
    return True

# # 待升级
@engine.define( 'curl' )
def cmd_curl( **params ):
    print('class_curl.update_code')
    return class_curl.update_code()

# # 待升级
#@engine.define( 'update_proxies' )
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
    shell.OutputShell('ls /tmp -R -l')
    return True

@engine.define( 'ls_img' )
def cmd_ls_img( **params):
    shell.OutputShell('ls mp3/img -R -l')
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
    # print('Memory total:',mem.total//mem_r)
    # print('Memory available:',mem.available//mem_r)
    # print('Memory percent:',mem.percent)
    # print('Memory used:',mem.used//mem_r)
    print('Memory free:',mem.free//mem_r)
    # print('Memory active:',mem.active//mem_r)
    # print('Memory inactive:',mem.inactive//mem_r)
    # print('Memory buffers:',mem.buffers//mem_r)
    # print('Memory cached:',mem.cached//mem_r)
    # print('Memory shared:',mem.shared//mem_r)
    # print('Memory slab:',mem.slab//mem_r)
    print('gc.collect()',gc.collect())
    return True

@engine.define( 'print_v' )
def print_v( **params ):
    print(BILIBILI_CLMY,'RADIO_NAME:',RADIO_NAME,'CHANGE_RADIO_NAME:',CHANGE_RADIO_NAME,'PLAY_ARTIST:',PLAY_ARTIST,'FFMPEG_MESSAGE_OUT:',FFMPEG_MESSAGE_OUT,'MP3_TOTAL_PLAY:',MP3_TOTAL_PLAY,'SLEEP:',SLEEP,'ERROR_RETRY:',ERROR_RETRY,'MAX_DOWNLOAD:',MAX_DOWNLOAD,'MAX_MEMORY:',MAX_MEMORY,'Global_minutes:',Global_minutes,'Global_Today_AP:',Global_Today_AP)
    return True