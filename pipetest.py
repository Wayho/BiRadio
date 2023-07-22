# coding: utf-8
import ffmpeg
import os
import random
import json
import shell as shell
import threading

VIDEO_FRAMERATE = 25
VIDEO_P = 'hd720'
VIDEO_FORMAT = 'mp4'
IMG_SECONDS = 120
PLAYLIST_PATH = 'playlist.txt'

process_stdout = None
# ps -T -p 21097
# cat /proc/21097/status

MP3_ROOT = 'aux'
IMG_FLODER = 'img'
sample = ['aux/coco/李玟-爱你爱到.m4a', 'aux/coco/李玟-伊甸园.m4a', 'aux/coco/李玟-过完冬季.m4a']
# OK ffmpeg -re -f concat -safe 0 -i playlist.txt -f flv -acodec aac -listen 1 -r 3 -vcodec libx264 http://127.0.0.1:8080

# ffmpeg -re -ss 0 -t 431 -f lavfi -i color=c=0x000000:s=640x360:r=30 -i mp3/img/1.jpg -i mp3/100/01.aac -i mp3/100/02.aac -filter_complex  "[1:v]scale=640:360[v1];[0:v][v1]overlay=0:0[outv];[2:0][3:0]concat=n=2:v=0:a=1[outa]"  -map [outv] -map [outa] -vcodec libx264 -acodec aac -b:a 192k -f flv test.flv

# FFMPEG::return: 137 您的实例 [web1] 使用内存量超出该实例规格，导致进程 OOM 退出。但是下载的还在

ffmpeg_concat = 'ffmpeg -re -ss 0 -t {} -f lavfi -i color=c=0x000000:s=640x360:r=30 -i {}{} -filter_complex  \"[1:v]scale=640:360[v1];[0:v][v1]overlay=0:0[outv];{}\"  -map [outv] -map [outa] -vcodec libx264 -acodec aac -f flv {}'
#ffmpeg_concat = 'ffmpeg -re -ss 0 -t {} -f lavfi -i color=c=0x000000:s=640x360:r=30 -i {}{} -filter_complex  \"[1:v]scale=640:360[v1];[0:v][v1]overlay=0:0[outv];{}\"  -map [outv] -map [outa] -vcodec libx264 -acodec copy -f flv {}'
# last_errmsg: Streamcopy requested for output stream 0:1, which is fed from a complex filtergraph. Filtering and streamcopy cannot be used together.

def test(str_rtmp):
    str_rtmp = 'test.flv'
    total_seconds = write_playlist(sample)
    print('audio seconds:',total_seconds)
    a_concat = ffmpeg.input("playlist.txt",**{"f":"concat","safe":0})         #ffmpeg -re -f concat -safe 0 -i playlist.txt
    
    #v3 = ffmpeg.input('img/art_coco102.jpg', t=IMG_SECONDS, framerate=VIDEO_FRAMERATE, loop=1)
    process_stdin = (
            ffmpeg
            #.input('pipe:', format=format, pix_fmt=pix_fmt, s=s)
            .output(
                a_concat,
                str_rtmp,
                vcodec='libx264',
                acodec='aac',
                r=VIDEO_FRAMERATE,
                #filter_threads=1,
                #listen=1, # enables HTTP server
                f=VIDEO_FORMAT)
            .run_async(cmd=["ffmpeg", "-re"])
    )
    shell.OutputShell('ps -elf | grep ffmpeg',True)
    process_stdin.wait()
    
def testpipe(str_rtmp):
    
    a_concat = ffmpeg.input(sample[0])
    inv = ffmpeg.input('img/art_coco130.jpg', t=IMG_SECONDS, framerate=VIDEO_FRAMERATE, loop=1)
    v_concat = ffmpeg.filter(inv,filter_name='scale', size='hd720')
    
    stream_spec_pipe_thread_rtmp(str_rtmp,v_concat,a_concat, format='rawvideo', pix_fmt='yuv420p',s='1280x720')

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

def stream_spec_pipe_out(rtmp,v_spec, a_spec,format='rawvideo', pix_fmt='yuv420p',s='1280x720'):
    global process_stdout
    url = rtmp
    process_stdout = (
        ffmpeg
        .output(v_spec,'pipe:', format=format, pix_fmt=pix_fmt)
        .run_async(cmd=["ffmpeg", "-re"],pipe_stdout=True)
    )
    process_stdout.stdout.close()
    #shell.OutputShell('ps -elf | grep ffmpeg',True)
    process_stdout.wait()
def stream_spec_pipe_in(rtmp,v_spec, a_spec,format='rawvideo', pix_fmt='yuv420p',s='1280x720'):
    # OK
    #v_in = ffmpeg.input('in.mp4')
    global process_stdout
    url = rtmp 
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
            .run_async(cmd=["ffmpeg", "-re","-y"],pipe_stdin=True)
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
            .run_async(cmd=["ffmpeg", "-re","-y"],pipe_stdin=True)
        )
    while True:
        in_bytes = process_stdout.stdout.read(1280*720 * 3*8)
        if not in_bytes:
            break
        process_stdin.stdin.write(in_bytes)
    #shell.OutputShell('ps -elf | grep ffmpeg',True)
    process_stdin.stdin.close()
    process_stdin.wait()
def stream_spec_pipe_thread_rtmp(rtmp,v_spec, a_spec,format='rawvideo', pix_fmt='yuv420p',s='1280x720'):
    # OK    stream_spec_pipe_in(rtmp,v_spec, a_spec,format='rawvideo', pix_fmt='yuv420p',s='1280x720'):
    out_thread = threading.Thread(target=stream_spec_pipe_out,args=(rtmp,v_spec, a_spec,format, pix_fmt,s))
    out_thread.start()
    in_thread = threading.Thread(target=stream_spec_pipe_in,args=(rtmp,v_spec, a_spec,format, pix_fmt,s))
    in_thread.start()
    shell.OutputShell('ps -aux | grep ffmpeg',True)
def stream_spec_pipe_rtmp(rtmp,v_spec, a_spec,format='rawvideo', pix_fmt='yuv420p',s='1280x720'):
    #
    #v_in = ffmpeg.input('in.mp4')
    url = rtmp
    process_stdout = (
        ffmpeg
        .output(v_spec,'pipe:', format=format, pix_fmt=pix_fmt)
        .run_async(cmd=["ffmpeg", "-re"],pipe_stdout=True)
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
        in_bytes = process_stdout.stdout.read(1280*720 * 3*8)
        if not in_bytes:
            break
        process_stdin.stdin.write(in_bytes)
    #shell.OutputShell('ps -elf | grep ffmpeg',True)
    process_stdin.stdin.close()
    process_stdout.stdout.close()
    shell.OutputShell('ps -elf | grep ffmpeg',True)
    process_stdout.wait()
    process_stdin.wait
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
    # mp3_list = mp3list("mp3/country")

    #print(cmdconcat("mp3/100"))
    # print(mp3list("mp3/100"))
    # print(os.listdir("mp3"))
    rtmp= "http://127.0.0.1:8080"
    testpipe('pipe0.{}'.format(VIDEO_FORMAT))
    #rtmp_concat_floder(rtmp,[],total=30,artist=None,max_memory=80)
    #rtmp_concat_floder('rtmp',[''],total=3,artist=None,max_memory=80)
