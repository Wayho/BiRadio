# coding: utf-8
import eyed3
import os
import random
import ffmpeg
import json

###### 直播间播放器 ########
# Mime Type: video/mp4;codecs="avc1.640028,mp4a.40.2"
# Player Core: Hls7Player(sisterFetcher)
# Video Video Info:1920x1080,30FPS
# Audio Info: 48KHz,Stereo,256Kbps
# Encoder: BVC-SRT LiveHime/4.45.0
# Stream Host: cn-jssz-cm-02-19.bilivideo.com

# Mime Type: video/mp4;codecs="mp4a.40.2,avc1.64001e"
# Player Core: fMp4Player(Fetch)
# Video Video Info:640x36030FPS
# Audio Info: 44.1KHz,Stereo,125Kbps
# Encoder: Lavf58.29.100
# Stream Host: cn-jxnc-cm-01-11.bilivideo.com
###########################################################
## 记得修改为通过参数带来BILIBILI_RTMP+BILIBILI_CLMY
###########################################################
# rtmp://live-push.bilivideo.com/live-bvc/
# ?streamname=live_xxx&key=xxx&schedule=rtmp&pflag=1
###########################################################
# [rtmp @ 0x556dc4983600] Server error: Already publishing
# rtmp://live-push.bilivideo.com/live-bvc/?streamname=live_xxx&key=xxx&schedule=rtmp&pflag=1: Operation not permitted
###########################################################
# rtmp://live-push.bilivideo.com/live-bvc/?streamname=live_xxx&key=xxx&&schedule=rtmp&pflag=1: Input/output error
###########################################################
MP3_ROOT = 'aux'
IMG_FLODER = 'img'

# ffmpeg -re -ss 0 -t 431 -f lavfi -i color=c=0x000000:s=640x360:r=30 -i mp3/img/1.jpg -i mp3/100/01.aac -i mp3/100/02.aac -filter_complex  "[1:v]scale=640:360[v1];[0:v][v1]overlay=0:0[outv];[2:0][3:0]concat=n=2:v=0:a=1[outa]"  -map [outv] -map [outa] -vcodec libx264 -acodec aac -b:a 192k -f flv test.flv

# FFMPEG::return: 137 您的实例 [web1] 使用内存量超出该实例规格，导致进程 OOM 退出。但是下载的还在

ffmpeg_concat = 'ffmpeg -re -ss 0 -t {} -f lavfi -i color=c=0x000000:s=640x360:r=30 -i {}{} -filter_complex  \"[1:v]scale=640:360[v1];[0:v][v1]overlay=0:0[outv];{}\"  -map [outv] -map [outa] -vcodec libx264 -acodec aac -f flv {}'
#ffmpeg_concat = 'ffmpeg -re -ss 0 -t {} -f lavfi -i color=c=0x000000:s=640x360:r=30 -i {}{} -filter_complex  \"[1:v]scale=640:360[v1];[0:v][v1]overlay=0:0[outv];{}\"  -map [outv] -map [outa] -vcodec libx264 -acodec copy -f flv {}'
# last_errmsg: Streamcopy requested for output stream 0:1, which is fed from a complex filtergraph. Filtering and streamcopy cannot be used together.

def cmdconcat_floder(str_rtmp,floder_list,total=30,artist=None,max_memory=120):
    """
    获取floder_list下所有path mp3的串接cmd，不够total的话，复制自身补足
    :param str_rtmp:'"rtmp://"'
    :param floder_list:[fullpath]
    :param total=MP3_TOTAL_PLAY:最多串接文件个数
    :param artist=None:artist key word
    :return:
    """
    mp3_list = []
    if len(floder_list)==0:
        # 空的floder_list表示所有floder
        for file_floder_name in os.listdir(MP3_ROOT):
            full_path = MP3_ROOT + '/' + file_floder_name
            if os.path.isdir(full_path):
                floder_list.append(full_path)
    random.shuffle(floder_list)
    for floder_path in floder_list:
        a_mp3_list = mp3list(floder_path)
        for file_path in a_mp3_list: 
            # img_floder = IMG_FLODER
            # if file_path[0:len(img_floder)] != img_floder:
            #     # 排除 mp3/img
                mp3_list.append(file_path)
                if len(mp3_list) >=total:
                    break
    
    mp3_total = len(mp3_list)
    # 不够total的话，复制自身补足
    if mp3_total > 0:
        for lo in range(0,int(total/mp3_total)):
            if len(mp3_list) >=total:
                    break
            for item in mp3_list:
                if len(mp3_list) >=total:
                    break
                mp3_list.append(item)
    mp3_512M = []
    total_size = 0
    CONST_MB = float(1024 * 1024)
    for file_path in mp3_list:
        fsize = os.path.getsize(file_path) / CONST_MB
        if total_size + fsize > max_memory:
            break
        mp3_512M.append(file_path)
        total_size += fsize
    print('Total files:',len(mp3_512M),',Total size:',total_size)
    if 0==total_size:
        return {'cmd':'ls mp3 -R -l', 'info':[]}
    return cmdconcat_by_list(str_rtmp,mp3_512M,artist)

def cmdconcat_by_list(str_rtmp,mp3_list,artist=None):
    """
    根据mp3_list的串接cmd
    :param str_rtmp:'"rtmp://"'
    :param mp3_list:['fullpath']
    :param artist=None:artist key word
    :return: {'cmd':cmd, 'info':mp3_info_list}
    """
    duration_total = 0
    str_input = ''
    # [2:0][3:0]concat=n=2:v=0:a=1[outa]
    str_contac = ''
    index = 2
    mp3_info_list = []
    for file_path in mp3_list:
        audio_info = get_audio_info(file_path)
        # duration = get_duration_mp3(file_path)
        # id3 = get_id3_mp3(file_path)
        duration = audio_info.get('duration')
        duration_total += duration
        mp3_info_list.append({'duration':duration, 'title':audio_info.get('title'), 'artist':audio_info.get('artist'),'path':file_path, 'send':False})
        str_input += ' -i ' + file_path
        str_contac += '[' + str(index) + ':0]'
        index += 1
   
    str_contac += 'concat=n={}:v=0:a=1[outa]'
    str_contac = str_contac.format(len(mp3_list))
    img_list = mp3list(IMG_FLODER)
    random.shuffle(img_list)
    str_img = img_list[0]
    if artist:
        # 查找文件名里有artist
        finded = False
        for item in img_list:
            if -1!=item.find(artist):
                finded = True
                str_img = item
        if not finded:
            # 如果没有，就不要把有 art_的图播出来
            # 查找文件名里没有art_
            for item in img_list:
                if -1==item.find('art_'):
                    str_img = item
    else:
        # 保证不出有 art_的图
        # 查找文件名里没有art_
        for item in img_list:
            if -1==item.find('art_'):
                str_img = item
    cmd = ffmpeg_concat.format(str(int(duration_total)+1), str_img, str_input, str_contac, str_rtmp)
    return {'cmd':cmd, 'info':mp3_info_list}

def get_audio_info(file_path):
    """
    获取mp3/aac音频文件时长
    :param file_path:
    :return:
    """
    title = None
    artist = None
    probe = ffmpeg.probe(file_path)
    format = probe.get('format')
    duration = float(format.get('duration'))
    if format.get('tags'):
        tags = format.get('tags')
        if tags.get('title'):
            title = tags.get('title')
        if tags.get('artist'):
            artist = tags.get('artist')
    return {'duration':duration,'title':title,'artist':artist}

# 废弃
def get_duration_mp3(file_path):
    """
    获取mp3音频文件时长
    :param file_path:
    :return:
    """
    audiofile = eyed3.load(file_path)
    return audiofile.info.time_secs
# 废弃
def get_id3_mp3(file_path):
    """
    获取mp3音频文件id3
    :param file_path:
    :return:
    """
    audiofile = eyed3.load(file_path)
    return {'title':audiofile.tag.title,'artist':audiofile.tag.artist}

def mp3list(path="mp3/100"):
    """
    获取mp3音频文件path列表
    :param path:
    :return:
    """
    mp3list = []
    if os.path.exists(path):
        for file_name in os.listdir(path):
            mp3list.append(path+'/' +file_name)
        random.shuffle(mp3list)
    return mp3list

if __name__ == '__main__':
    # mp3_list = mp3list("mp3/country")

    #print(cmdconcat("mp3/100"))
    # print(mp3list("mp3/100"))
    # print(os.listdir("mp3"))
    cmd = cmdconcat_floder('r',[],3,None)
    print(cmd)
