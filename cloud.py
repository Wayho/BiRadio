# coding: utf-8

from leancloud import Engine
from leancloud import LeanEngineError
import shell as shell
import time
import os
import requests
import random

import class_variable as class_variable
import danmu as danmu
import startlive as startlive
import class_sharekey as class_sharekey
import class_artist as class_artist
import down_123_proxies as download
import class_proxies as class_proxies
import class_curl as class_curl
import stream as stream
import ding_msg as ding_msg
import wss_danmu as wss_danmu
#import shutil
import psutil
import gc
import threading
import shutil 
####################mp4#######################################
TMP_ROOT = '/tmp'
MP3_ROOT = 'aux'
MP4_ROOT = '/tmp/mp4'
SUBTITLE_ROOT = '/tmp/srt'
LOOP_LOOP_MP4_PATH  = "/tmp/loop.mp4"
SAMPLE_MP4_432p_LIST = ['s365_432p_201_192k.mp4','s365_432p_101_192k.mp4','s365_432p_146_192k.mp4','sziji_432p_176_192k.mp4']
BAK_MP4_PATH = 's365_432p_201_192k.mp4'

SITENAME = os.environ.get('SITENAME') or 'none'
MEMORY = os.environ.get('MEMORY') or 'none'
WEBHOOK_DINGDING = 'https://'
#ROOM_ID = '30338274'        #7rings
#ROOM_ID = '30356247'        #mustlive
ROOM_ID = os.environ.get('ROOM_ID') or None
print('cloud v5.6.2 SITENAME:',SITENAME,'ROOM_ID:',ROOM_ID,'MEMORY:',MEMORY)
if not os.path.exists(MP4_ROOT):
        print('cloud:mkdir::',MP4_ROOT)
        os.mkdir(MP4_ROOT)
        time.sleep(0.1)
        # /tmp 下loop.mp4,next.mp4
        shutil.copy(BAK_MP4_PATH,LOOP_LOOP_MP4_PATH)
        for sample in SAMPLE_MP4_432p_LIST:
            dest_sample = os.path.join(MP4_ROOT, sample)    # '{}/{}'.format(MP4_ROOT,sample)
            if  os.path.exists(sample):
                if sample==BAK_MP4_PATH:
                    shutil.copy(sample,dest_sample)
                else:
                    os.rename(sample,dest_sample)
if not os.path.exists(SUBTITLE_ROOT):
        print('cloud:mkdir::',SUBTITLE_ROOT)
        os.mkdir(SUBTITLE_ROOT)

# 每次重启、休眠检查
def cloud_wakeup():
    print("cloud_wakeup:sleep 15 for check MP4_ROOT")
    time.sleep(15)
    Setup()
    mp4file = os.listdir(MP4_ROOT)
    if len(SAMPLE_MP4_432p_LIST)>= len(mp4file):
        # 没有音频，提醒
        print('ding_msg:{} file:'.format(MP4_ROOT),mp4file,ding_msg.dingMe(WEBHOOK_DINGDING,SITENAME+':mp4 is empty'))
send_thread = threading.Thread(target=cloud_wakeup,args=())
send_thread.start()


################# LOAD CONFIG ##############################
BILIBILI_RTMP = "rtmp://"
BILIBILI_CLMY = None

FFMPEG_MP4_CODEC = '-threads 3 -vcodec libx264 -acodec aac  -b:a 192k'
FFMPEG_RTMP_CODEC = '-threads 5 -vcodec copy -acodec aac -b:a 192k'
FFMPEG_AMIX_CODEC = '-threads 16 -vcodec copy -acodec aac -b:a 192k'
FFMPEG_FRAMERATE = None
FFMPEG_SUBTITLE = True

RADIO_NAME = 'Live Music | 极其音乐'
CHANGE_RADIO_NAME = False
PLAY_ARTIST = False
FFMPEG_MESSAGE_OUT = False
MP3_TOTAL_PLAY = 30
SLEEP = 120
ERROR_RETRY = 399
MAX_DOWNLOAD = 25
MAX_MEMORY = 90

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
Global_Danmu_Retry_Times = 99   # 0 on 99 off
Global_Retry_Times = 0
Global_minutes = 0

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
    global MAX_MEMORY
    global WEBHOOK_DINGDING
    global ROOM_ID
    global Global_Danmu_Retry_Times
    global FFMPEG_MP4_CODEC
    global FFMPEG_RTMP_CODEC
    global FFMPEG_FRAMERATE
    global FFMPEG_SUBTITLE
    # config = class_variable.get_config()
    # print(config)
    variable = class_variable.get_variable()
    if variable:
        config = variable.get('config')
        ## 记得修改为通过startlive.tryStartLive()参数带来BILIBILI_RTMP+BILIBILI_CLMY
        BILIBILI_RTMP = config.get('BILIBILI_RTMP')
        BILIBILI_CLMY = config.get('BILIBILI_CLMY')
        WEBHOOK_DINGDING = config.get('WEBHOOK_DINGDING')
        RADIO_NAME = config.get('RADIO_NAME')
        CHANGE_RADIO_NAME = config.get('CHANGE_RADIO_NAME')
        PLAY_ARTIST = config.get('PLAY_ARTIST')
        FFMPEG_MESSAGE_OUT = config.get('FFMPEG_MESSAGE_OUT')
        MP3_TOTAL_PLAY = config.get('MP3_TOTAL_PLAY')
        SLEEP = config.get('SLEEP')
        ERROR_RETRY = config.get('ERROR_RETRY')
        MAX_DOWNLOAD = config.get('MAX_DOWNLOAD')
        ROOM_ID = config.get('ROOM_ID')
        FFMPEG_SUBTITLE = config.get('FFMPEG_SUBTITLE')
        Global_Danmu_Retry_Times = config.get('DEFAULT_DANMU_RETRY')
        #if 'BiliRadio_py' == SITENAME:
        if '512' == MEMORY[0:3]:
            MAX_MEMORY = config.get('MAX_MEMORY_PY')
        else:
            MAX_MEMORY = config.get('MAX_MEMORY')
        if BILIBILI_CLMY:
            RTMP_URL_STR = BILIBILI_RTMP + BILIBILI_CLMY
        # v5.0.0
        FFMPEG_MP4_CODEC = variable.get('codec_mp4')
        FFMPEG_RTMP_CODEC = variable.get('codec_rtmp')
    else:
        print('############## ERROR IN LOAD VARIABLE ##################')
    print_v()
    class_variable.SaveCookiesFromDB()
    return True

@engine.define( 'wss_danmu' )
# 一次性唤醒，无需Heart
def start_wss_danmu(**params):
    print('try:start_wss_danmu',ROOM_ID)
    cloud_thread = threading.Thread(target=try_wss_danmu,args=())
    cloud_thread.start()
    return True

def try_wss_danmu():
    requests.get( "http://localhost:3000" )
    if canStart():
        Setup()
        if not ROOM_ID:
            print('ROOM_ID==None',ROOM_ID)
        else:
            wss_danmu.start(ROOM_ID)
    else:
        print('canStart() return False')

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
    #concat = mp3.cmdconcat_floder(RTMP_URL_STR, floder_list, MP3_TOTAL_PLAY, artist,MAX_MEMORY)
    cmd = stream.rtmp_concat_mp4(RTMP_URL_STR, MP3_TOTAL_PLAY, codec=FFMPEG_RTMP_CODEC,framerate=FFMPEG_FRAMERATE,max_memory=MAX_MEMORY,floder_list=floder_list)
    ret = -9
    for i in range(6):
        ret = shell.OutputShell(cmd,FFMPEG_MESSAGE_OUT)
        print('rtmp::return:',ret)
        cmd_memory()
        cmd_memory()
        if -9 == ret:
            break
        if 1 == ret:
            break
    return ret

@engine.define( 'play_test' )
def play_test(floder_list=[], artist=None,radioname=RADIO_NAME):
    print('play_test:',floder_list, artist,radioname)
    #concat = mp3.cmdconcat_floder(RTMP_URL_STR, floder_list, MP3_TOTAL_PLAY, artist,MAX_MEMORY)
    cmd = stream.test(RTMP_URL_STR, MP3_TOTAL_PLAY, codec=FFMPEG_RTMP_CODEC,framerate=FFMPEG_FRAMERATE,max_memory=MAX_MEMORY,subtitle=FFMPEG_SUBTITLE,floder_list=floder_list)
    ret = -9
    for i in range(6):
        ret = shell.OutputShell(cmd,FFMPEG_MESSAGE_OUT)
        print('rtmp::return:',ret)
        cmd_memory()
        cmd_memory()
        if -9 == ret:
            break
        if 1 == ret:
            break
    return ret

@engine.define( 'ffmpeg_loop' )
def ffmpeg_loop(floder_list=[], artist=None,radioname=RADIO_NAME):
    print('ffmpeg_loop:',floder_list, artist,radioname)
    if not BILIBILI_CLMY:
        Setup()
    # make_temp_next_loop_thread = threading.Thread(target=stream.rtmp_loop,args=(RTMP_URL_STR,FFMPEG_RTMP_CODEC,FFMPEG_AMIX_CODEC,10000,FFMPEG_FRAMERATE,))
    # make_temp_next_loop_thread.start()
    cmd = stream.rtmp_loop(RTMP_URL_STR,codec=FFMPEG_RTMP_CODEC,amix_codec=FFMPEG_AMIX_CODEC,adelay=10000,framerate=FFMPEG_FRAMERATE)
    ret = -9
    make_temp_next_loop_thread = threading.Thread(target=stream.make_temp_next_loop,args=(10000,FFMPEG_AMIX_CODEC,))
    #make_temp_next_loop_thread.setDaemon(True) #线程设置守护，如果主线程结束，子线程也随之结束
    make_temp_next_loop_thread.start()
    if cmd:
        for i in range(999):
            ret = shell.OutputShell(cmd,FFMPEG_MESSAGE_OUT)
            print('rtmp::return:',ret)
            #stream.rtmp_loop_reset()
            cmd_memory()
            time.sleep(2)
            cmd_memory()
            if -9 == ret:
                break
            if 1 == ret:
                break
    return ret
    return True

@engine.define( 'ffmpeg_loop_exit' )
def ffmpeg_loop_exit(floder_list=[], artist=None,radioname=RADIO_NAME):
    print('ffmpeg_loop_exit:',floder_list, artist,radioname)
    stream.rtmp_loop_exit()
    return True

@engine.define( 'map_mp4' )
def map_mp4(floder_list=[], artist=None,radioname=RADIO_NAME):
    cloud_thread = threading.Thread(target=do_map_mp4,args=(MAX_DOWNLOAD,))
    cloud_thread.start()
    return True

@engine.define( 'map_mp4_6' )
def map_mp4_6(floder_list=[], artist=None,radioname=RADIO_NAME):
    cloud_thread = threading.Thread(target=do_map_mp4,args=(6,))
    cloud_thread.start()
    return True

def do_map_mp4(total):
    #获取SOURCE_ADUIO_FLODER下m4a，转mp4
    Setup()
    done_num = stream.map_video_audio_mp4(total,codec=FFMPEG_MP4_CODEC,framerate=FFMPEG_FRAMERATE,subtitle=FFMPEG_SUBTITLE)
    return done_num

@engine.define( 'map_mp4_sample' )
def map_mp4_sample(floder_list=[], artist=None,radioname=RADIO_NAME):
    # ffmpeg -re -i /tmp/mp4/192k-CoCo-想你的365天.mp4 -f flv -threads 8 -acodec aac -b:a 192k -vcodec copy rtmp
    Setup()
    done_num = stream.ai_to_mp4('aux/coco/192k-CoCo-想你的365天.m4a','img/art_coco1{}.jpg'.format(random.randint(10,94)))
    return done_num

# 18 */1 7-23 * * ?
# 统一到一个云函数定时1分钟运行
# 需要停止restart_radio任务才能kill_ffmpeg，否则又会启动
@engine.define( 'do_one_minute' )
def do_one_minute( **params ):
    global Global_minutes
    Global_minutes += 1
    if not canStart():
        return False
    if not BILIBILI_CLMY:
        Setup()
    ffmpeg_status = stream.ffmpeg_status()
    if ffmpeg_status:
        #id3_send()
        if Global_minutes % 20 == 1:
                print('do_one_minute:',Global_Retry_Times,ffmpeg_status)
                requests.get( "http://localhost:3000" )
        is_playlist = ffmpeg_status.get('playlist') or ffmpeg_status.get('looplist')
        if is_playlist:
            return False
        else:
            # is making mp4, must kill for cmd_restart_radio
            cmd_kill_ffmpeg()
            time.sleep(3)
    cmd_restart_radio()        
    return True

def cmd_restart_radio():
    global Global_Retry_Times
    print('Restart Radio')
    if Global_Retry_Times >= ERROR_RETRY:
        print('Global_Retry_Times >= ERROR_RETRY')
        return False
    
    ffmpeg_loop()
    return True
    
    # < v5.5
    playret = 0
    if PLAY_ARTIST:
        playret = play_artist()
    else:
        playret = play_play()
    if -9 == playret:
        return False
    elif 1== playret:
        Global_Retry_Times += 1
        print('play:',ding_msg.dingMe(WEBHOOK_DINGDING,SITENAME+':ffmpeg={}:Retry times:{}'.format(playret,Global_Retry_Times)))
        #startlive.tryStartLive(str(ROOM_ID))
    elif 0 != playret:
        Global_Retry_Times += 1
        print('play:',ding_msg.dingMe(WEBHOOK_DINGDING,SITENAME+':ffmpeg={}:Retry times:{}'.format(playret,Global_Retry_Times)))
    print('*************** END *******************')
    return True
        

# 0 0 2-16 * * ?     
@engine.define( 'reset_retry' )
def cmd_reset_retry( **params ):
    global Global_Retry_Times
    global Global_minutes
    print( '***************reset_retry*******************',Global_Retry_Times,Global_Danmu_Retry_Times, Global_minutes)
    Global_Retry_Times = 0
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
    cans = canStart()
    if not cans:
        time.sleep(18)
        cans = canStart()
    if cans:
            res = startlive.tryStartLive(str(ROOM_ID))
            if rtmp:
                if res.get('code')==0:
                    BILIBILI_RTMP = res.get('rtmp').get('addr')
                    BILIBILI_CLMY = res.get('rtmp').get('code')
                    if BILIBILI_CLMY:
                        RTMP_URL_STR = '\"' + BILIBILI_RTMP + BILIBILI_CLMY + '\"'

def canStart():
    global Global_minutes
    (today,tomorrow) = class_variable.get_today_AP()
    if not SITENAME in today:
        if Global_minutes % 60 == 1:
            print('This site is',SITENAME,'Today:',today,'Tomorrow:',tomorrow,Global_minutes)
        return False   
    if not SITENAME in ['BiLive_ay','BiLive_py']:
        # 备用推流机，直接用，非备用，要看tmpfilenum
        tmpfilenum = os.listdir(MP4_ROOT)
        if len(SAMPLE_MP4_432p_LIST)>= len(tmpfilenum):
            # 没有音频，切换备用推流机
            if 'a'==SITENAME[len(SITENAME)-2]:
                class_variable.set_today_AP('BiLive_ay',True)
            else:
                class_variable.set_today_AP('BiLive_py',False)
            print('#'*40,'EMPTY VIDEO,SET TO DEFAULT','#'*40)
            print('ding_msg:{} file:'.format(MP4_ROOT),tmpfilenum,ding_msg.dingMe(WEBHOOK_DINGDING,SITENAME+':EMPTY VIDEO,SET TO DEFAULT'))
            return False
    #print('Can start live','Today:',today,'Tomorrow:',tomorrow)
    if Global_minutes % 60 == 1:
        print('This site is',SITENAME,'Today:',today,'Tomorrow:',tomorrow,Global_minutes)
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

@engine.define( 'danmu_on_off' )
def danmu_off(**params):
    global Global_Danmu_Retry_Times
    if 99==Global_Danmu_Retry_Times:
        Global_Danmu_Retry_Times = 0
    else:
        Global_Danmu_Retry_Times = 99
    print('############## Global_Danmu_Retry_Times #############',Global_Danmu_Retry_Times)
    return True

# 35 */1 7-23 * * ?
#@engine.define( 'id3_send' )
def id3_send():
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
    ffmpeg_status = stream.ffmpeg_status()
    print('This site is',SITENAME,'Today:',today,'Tomorrow:',tomorrow,Global_minutes,ffmpeg_status)
    
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

@engine.define( 'a_shell' )
# 调试 {"cmd":"ls -l" }
def cmd_shell( cmd, **params ):
    shell.OutputShell(cmd)
    return True
        
@engine.define( 'ls_mp3' )
def cmd_ls_mp3( **params):
    shell.OutputShell('ls {} -R -l'.format(MP3_ROOT))
    return True
        
@engine.define( 'ls_mp4' )
def cmd_ls_mp4( **params):
    shell.OutputShell('ls {} -R -l'.format(MP4_ROOT))
    return True

@engine.define( 'ls_srt' )
def cmd_ls_srt( **params):
    shell.OutputShell('ls {} -R -l'.format(SUBTITLE_ROOT))
    return True

@engine.define( 'ls_img' )
def cmd_ls_img( **params):
    shell.OutputShell('ls img -R -l')
    return True

@engine.define( 'ls_tmp' )
def cmd_ls_tmp( **params):
    shell.OutputShell('ls /tmp -l')
    return True

@engine.define( 'ls' )
def cmd_ls( **params):
    shell.OutputShell('ls -l')
    return True

@engine.define( 'ps_aux_p' )
# 调试 {"cmd":"ls -l" }
def cmd_ps( **params ):
    shell.OutputShell('ps -aux')
    return True
 
@engine.define( 'ps_aux_ffmpeg' )
# 调试 {"cmd":"ls -l" }
def cmd_ps_ef_ffmpeg( **params ):
    infolist = shell.procs_info("ffmpeg")
    shell.OutputShell('ps -aux | grep ffmpeg')
    try:
        for info in infolist:
            pid = info['pid']
            shell.OutputShell('cat /proc/{}/status'.format(pid))
    finally:
        pass
    return 

@engine.define( 'python' )
# 调试 {"cmd":"ls -l" }
def cmd_python(cmd, **params ):
    shell.OutputShell('python {}'.format(cmd))
    return True

@engine.define( 'python_pipe' )
# 调试 {"cmd":"ls -l" }
def cmd_python_pipe(**params ):
    shell.OutputShell('python pipetest.py {}'.format(MAX_DOWNLOAD))
    cmd_memory()
    return True

@engine.define( 'python_test' )
# 调试 {"cmd":"ls -l" }
def cmd_python_test(**params ):
    shell.OutputShell('python test.py '.format(MAX_DOWNLOAD))
    cmd_memory()
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
    print(BILIBILI_CLMY,'RADIO_NAME:',RADIO_NAME,'CHANGE_RADIO_NAME:',CHANGE_RADIO_NAME,'PLAY_ARTIST:',PLAY_ARTIST,'FFMPEG_MESSAGE_OUT:',FFMPEG_MESSAGE_OUT,'MP3_TOTAL_PLAY:',MP3_TOTAL_PLAY,'SLEEP:',SLEEP,'ERROR_RETRY:',ERROR_RETRY,'MAX_DOWNLOAD:',MAX_DOWNLOAD,'MAX_MEMORY:',MAX_MEMORY)
    print('FFMPEG_FRAMERATE:',FFMPEG_FRAMERATE,'FFMPEG_MP4_CODEC:',FFMPEG_MP4_CODEC,'FFMPEG_RTMP_CODEC:',FFMPEG_RTMP_CODEC,'Global_minutes:',Global_minutes,'Global_Danmu_Retry_Times:',Global_Danmu_Retry_Times)
    return True
