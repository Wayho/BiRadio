# coding: utf-8
import ffmpeg
import os
import sys
import random
import json
import shell as shell


VIDEO_FRAMERATE = 25
VIDEO_P = 'hd720'
VIDEO_FORMAT = 'flv'
IMG_SECONDS = 60
PLAYLIST_PATH = 'playlist.txt'

# ps -T -p 21097
# cat /proc/21097/status
MP4_ROOT = '/tmp/mp4'
MP3_ROOT = 'aux'
IMG_FLODER = 'img'

# OK ffmpeg -re -f concat -safe 0 -i playlist.txt -f flv -acodec aac -listen 1 -r 3 -vcodec libx264 http://127.0.0.1:8080
##ffplay -f flv http://127.0.0.1:8080
##############################################
# # 以第一个视频分辨率作为全局分辨率
# # 视频分辨率相同可以使用copy?{"cmd":"ffmpeg -re -f concat -safe 0 -i playlist.txt -f flv -codec copy -listen 1  http://127.0.0.1:8080"}
# # ffmpeg -re -f concat -safe 0 -i playlist.txt -f flv -acodec aac -listen 1 -vcodec libx264 http://127.0.0.1:8080
# # ffmpeg -re -f concat -safe 0 -i playlist.txt -f flv -acodec aac -vcodec libx264 rtmp
# # ffplay -f flv http://127.0.0.1:8080
##############################################
# playlist.txt
# file 'sample_720p_a320k.mp4'
# file 'sample_480p_a320k.mp4'
# #file 'sample_432p_a320k.mp4'
##############################################

# ffmpeg -re -ss 0 -t 431 -f lavfi -i color=c=0x000000:s=640x360:r=30 -i mp3/img/1.jpg -i mp3/100/01.aac -i mp3/100/02.aac -filter_complex  "[1:v]scale=640:360[v1];[0:v][v1]overlay=0:0[outv];[2:0][3:0]concat=n=2:v=0:a=1[outa]"  -map [outv] -map [outa] -vcodec libx264 -acodec aac -b:a 192k -f flv test.flv

# FFMPEG::return: 137 您的实例 [web1] 使用内存量超出该实例规格，导致进程 OOM 退出。但是下载的还在

ffmpeg_concat = 'ffmpeg -re -ss 0 -t {} -f lavfi -i color=c=0x000000:s=640x360:r=30 -i {}{} -filter_complex  \"[1:v]scale=640:360[v1];[0:v][v1]overlay=0:0[outv];{}\"  -map [outv] -map [outa] -vcodec libx264 -acodec aac -f flv {}'
#ffmpeg_concat = 'ffmpeg -re -ss 0 -t {} -f lavfi -i color=c=0x000000:s=640x360:r=30 -i {}{} -filter_complex  \"[1:v]scale=640:360[v1];[0:v][v1]overlay=0:0[outv];{}\"  -map [outv] -map [outa] -vcodec libx264 -acodec copy -f flv {}'
# last_errmsg: Streamcopy requested for output stream 0:1, which is fed from a complex filtergraph. Filtering and streamcopy cannot be used together.

#ffmpeg_playlist = "ffmpeg -re -f concat -safe 0 -i playlist.txt -vcodec libx264 -acodec aac -f flv {}"
ffmpeg_playlist = "ffmpeg -re -f concat -safe 0 -i playlist.txt -codec copy -f flv {}"
print('stream v3.0:',ffmpeg_playlist)
def rtmp_concat_mp4(str_rtmp,floder_list,total=30,artist=None,max_memory=80):
    """
    获取floder_list下所有path mp3的串接cmd，不够total的话，复制自身补足
    :param str_rtmp:'"rtmp://"'
    :param floder_list:[fullpath]
    :param total=MP3_TOTAL_PLAY:最多串接文件个数
    :param artist=None:artist key word
    :return:
    """
    str_rtmp = '\"{}\"'.format(str_rtmp)
    root_list = mp3list(MP4_ROOT)
    mp4list=[]
    for file_path in root_list: 
        mp4list.append(file_path)
        if len(mp4list) >= total:
            break
    total_seconds = write_playlist(mp4list)
    print('total seconds:',total_seconds)
    cmd = ffmpeg_playlist.format(str_rtmp)
    return cmd#shell.OutputShell(cmd,True)

    #test(str_rtmp)
    
def rtmp_concat_floder(str_rtmp,floder_list,total=30,artist=None,max_memory=80):
    """
    获取floder_list下所有path mp3的串接cmd，不够total的话，复制自身补足
    :param str_rtmp:'"rtmp://"'
    :param floder_list:[fullpath]
    :param total=MP3_TOTAL_PLAY:最多串接文件个数
    :param artist=None:artist key word
    :return:
    """
    #test(str_rtmp)
    #return
    mp3_list = []
    str_rtmp = '\"{}\"'.format(str_rtmp)
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
        return {'cmd':'ls {} -R -l'.format(MP3_ROOT), 'info':[]}
    #return ffmpeg_concat_by_list(str_rtmp,mp3_512M,artist)
    return all_2_rtmp(str_rtmp,mp3_512M,artist)

def all_2_rtmp(str_rtmp,mp3_512M,artist):
    # OK ffmpeg -re -f concat -safe 0 -i playlist.txt -f flv -acodec aac -listen 1 -r 3 -vcodec libx264 http://127.0.0.1:8080
    # a_c = ffmpeg.input("concat:a1.m4a|a2.m4a")    #ok first
    total_seconds = write_playlist(mp3_512M)
    print('audio seconds:',total_seconds)
    a_concat = ffmpeg.input("playlist.txt",**{"f":"concat","safe":0})         #ffmpeg -re -f concat -safe 0 -i playlist.txt
    v_in_arr = []
    img_seconds = 0
    img_list = mp3list(IMG_FLODER)
    random.shuffle(img_list)
    for fn in img_list:
        if img_seconds+IMG_SECONDS>=total_seconds:
            break
        inv = ffmpeg.input(fn, t=IMG_SECONDS, framerate=VIDEO_FRAMERATE, loop=1)
        v_s = ffmpeg.filter(inv,filter_name='scale', size='hd720')
        v_in_arr.append(v_s)
        img_seconds += IMG_SECONDS
    print('image seconds:',img_seconds)
    v_concat = ffmpeg.concat(*v_in_arr, v=1,a=0)

    try:
        out, err = (ffmpeg
            .output(
                a_concat, v_concat,     #!!!! a_concat must first !!!!
                str_rtmp,
                vcodec='libx264',
                acodec='aac',
                r=VIDEO_FRAMERATE,
                #listen=1, # enables HTTP server
                f=VIDEO_FORMAT)
            .run(cmd=["ffmpeg", "-re"])#capture_stderr=True)
        )
        print(ffmpeg.compile(out))
        #print('err:',type(err.decode()),err.decode())
    except ffmpeg.Error as error:
        #print("stderr:",error.stderr.decode())
        print("stderr:")
    return {'cmd':'OK {} seconds'.format(total_seconds), 'info':[]}

def write_playlist(mp3_list):
    """
    根据mp3_list,write playlist.txt
    :param mp3_list:['fullpath']
    :return: duration_total
    """
    duration_total = 0
    lineArray = []
    
    for file_path in mp3_list:
        lineArray.append("file \'{}\'".format(file_path))
        audio_info = get_audio_info(file_path)
        duration = audio_info.get('duration')
        duration_total += duration
    lineArray.append("# rem")
    playlist_str = '\r\n'.join(lineArray)
    playlist = open(PLAYLIST_PATH, 'w')
    playlist.write(playlist_str)
    playlist.close()
    print(playlist_str)
    return duration_total

########################## no need, pipe version ###############################

def ffmpeg_concat_by_list(str_rtmp,mp3_list,artist=None):
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
   

    img_list = mp3list(IMG_FLODER)
    random.shuffle(img_list)

    return all_list_pipe_rtmp(str_rtmp,img_list,mp3_list)

def all_list_pipe_rtmp(str_rtmp,image_files,audio_files):
    a_in_arr = []
    total_seconds = 0
    for fn in audio_files:
        ina = ffmpeg.input(fn)
        a_in_arr.append(ina)
        probe = ffmpeg.probe(fn)
        format = probe.get('format')
        duration = float(format.get('duration'))
        total_seconds += duration
    print('total seconds:',total_seconds)
    a_concat = ffmpeg.concat(*a_in_arr, v=0,a=1)
    v_in_arr = []
    img_seconds = 0
    for fn in image_files:
        if img_seconds+IMG_SECONDS>=total_seconds:
            break
        inv = ffmpeg.input(fn, t=IMG_SECONDS, framerate=VIDEO_FRAMERATE, loop=1)
        v_s = ffmpeg.filter(inv,filter_name='scale', size='hd720')
        v_in_arr.append(v_s)
        img_seconds += IMG_SECONDS
    print('image seconds:',img_seconds)
    v_concat = ffmpeg.concat(*v_in_arr, v=1,a=0)
    stream_spec_pipe_rtmp(str_rtmp,v_concat,a_concat, format='rawvideo', pix_fmt='yuv420p',s='1280x720')

def stream_spec_pipe_rtmp(rtmp,v_spec, a_spec,format='rawvideo', pix_fmt='yuv420p',s='1280x720'):
    # OK
    #v_in = ffmpeg.input('in.mp4')
    url = rtmp
    process_stdout = (
        ffmpeg
        .output(v_spec,'pipe:', format=format, pix_fmt=pix_fmt)
        .run_async(cmd=["ffmpeg"],pipe_stdout=True)
    )
    
    if a_spec:
        v3 = ffmpeg.input('pipe:', format=format, pix_fmt=pix_fmt, s=s,thread_queue_size=1)
        process_stdin = (
            ffmpeg
            #.input('pipe:', format=format, pix_fmt=pix_fmt, s=s)
            .output(
                v3,a_spec,
                url,
                vcodec='libx264',
                acodec='aac',
                r=VIDEO_FRAMERATE,
                filter_threads=1,
                #listen=1, # enables HTTP server
                f=VIDEO_FORMAT)
            .run_async(cmd=["ffmpeg", "-re"],pipe_stdin=True)
        )
    else:
        process_stdin = (
            ffmpeg
            .input('pipe:', format=format, pix_fmt=pix_fmt, s=s,thread_queue_size=1)
            .output(
                #v3,
                url,
                vcodec='libx264',
                acodec='aac',
                r=VIDEO_FRAMERATE,
                filter_threads=1,
                #listen=1, # enables HTTP server
                f=VIDEO_FORMAT)
            .run_async(cmd=["ffmpeg", "-re"],pipe_stdin=True)
        )
    while True:
        in_bytes = process_stdout.stdout.read(1280*720 * 3)
        if not in_bytes:
            break
        process_stdin.stdin.write(in_bytes)
    process_stdin.stdin.close()
    process_stdout.stdout.close()
    process_stdout.wait()
    process_stdin.wait()

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

def mp3list(path="a/coco"):
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
    # python stream.py 30
    # <class 'list'> ['stream.py', '30']
    rtmp= "http://127.0.0.1:8080"
    try:
        argv = sys.argv[1]
        print(type(argv),argv)
        rtmp_concat_floder('rtmp',[''],total=int(argv),artist=None,max_memory=80)
    except:
        print('No argv, sample: python stream.py 30')
        rtmp_concat_floder('rtmp',[''],total=30,artist=None,max_memory=80)
    #rtmp_concat_floder(rtmp,[],total=30,artist=None,max_memory=80)
    