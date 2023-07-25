# coding: utf-8
import ffmpeg
import os
import sys
import time
import random
import json
import shell as shell
import threading
import shutil 
#shutil.copy(oldName, newName)
# leancloud :
#rtmp={"cmd":"ffmpeg -re -filter_threads 1 -i aux/coco/李玟-撒野.m4a -ss 0 -t 344 -f lavfi -i color=c=0x000000:s=924x520:r=25 -i img/art_coco122.jpg -filter_complex \"[2:v]scale=924x520[v2];[1:v][v2]overlay=x=0:y=0[outv];[0:0]concat=n=1:v=0:a=1[outa]\" -map [outv] -map [outa] -vcodec libx264 -acodec aac -b:a 320k -f flv \"rtmp://flag=1\""}
# mp4_re = ffmpeg -re -filter_threads 1 -i aux/coco/李玟-撒野.m4a -ss 0 -t 344 -f lavfi -i color=c=0x000000:s=924x520:r=25 -i img/art_coco122.jpg -filter_complex "[2:v]scale=924x520[v2];[1:v][v2]overlay=x=0:y=0[outv];[0:0]concat=n=1:v=0:a=1[outa]" -map [outv] -map [outa] -vcodec libx264 -acodec aac -b:a 320k -f mp4 sample_520p_a320k.mp4
# mp4 ={"cmd":"ffmpeg -filter_threads 1 -i aux/coco/李玟-撒野.m4a -ss 0 -t 344 -f lavfi -i color=c=0x000000:s=924x520:r=25 -i img/art_coco122.jpg -filter_complex \"[2:v]scale=924x520[v2];[1:v][v2]overlay=x=0:y=0[outv];[0:0]concat=n=1:v=0:a=1[outa]\" -map [outv] -map [outa] -vcodec libx264 -acodec aac -b:a 320k -f mp4 sample0_520p_a320k.mp4"}
# s=924x520 rtmp=220M, mp4_re=227M, mp4=223M
# s=960x540 mp4=230M
# s=1138x640 内存量超出该实例规格
# s=1280x720 rtmp sample.mp4 338M
############ no scale ram == scale
# s=770x432 mp4=154M

##############################################
# # 以第一个视频分辨率作为全局分辨率
# # 视频分辨率相同可以使用copy?{"cmd":"ffmpeg -re -f concat -safe 0 -i playlist.txt -f flv -codec copy -listen 1  http://127.0.0.1:8080"}
# # ffmpeg -re -f concat -safe 0 -i playlist.txt -f flv -acodec aac -listen 1 -vcodec libx264 http://127.0.0.1:8080
# # ffmpeg -re -f concat -safe 0 -i playlist.txt -f flv -acodec aac -vcodec libx264 rtmp
# # ffplay -f flv http://127.0.0.1:8080
##############################################
# playlist.txt
# file 'sample_720p_a320k.mp4'
# file 'sample_720p_a320k_bak.mp4'
# #file 'sample_432p_a320k.mp4'
##############################################


VIDEO_FRAMERATE = 25
VIDEO_P = 'hd720'
VIDEO_FORMAT = 'mp4'
IMG_SECONDS = 120
PLAYLIST_PATH = 'playlist.txt'

process_stdout = None
# ps -T -p 21097
# cat /proc/21097/status
MP4_ROOT = '/tmp/mp4'
MP3_ROOT = 'aux'
IMG_FLODER = 'img'
SOURCE_ADUIO_FLODER = 'aux/coco'
CACHE_MP4_PATH = 'cache.mp4'
sample = ['aux/coco/李玟-爱你爱到.m4a', 'aux/coco/李玟-伊甸园.m4a', 'aux/coco/李玟-过完冬季.m4a']
# OK ffmpeg -re -f concat -safe 0 -i playlist.txt -f flv -acodec aac -listen 1 -r 3 -vcodec libx264 http://127.0.0.1:8080

# ffmpeg -re -ss 0 -t 431 -f lavfi -i color=c=0x000000:s=640x360:r=30 -i mp3/img/1.jpg -i mp3/100/01.aac -i mp3/100/02.aac -filter_complex  "[1:v]scale=640:360[v1];[0:v][v1]overlay=0:0[outv];[2:0][3:0]concat=n=2:v=0:a=1[outa]"  -map [outv] -map [outa] -vcodec libx264 -acodec aac -b:a 192k -f flv test.flv

# FFMPEG::return: 137 您的实例 [web1] 使用内存量超出该实例规格，导致进程 OOM 退出。但是下载的还在

ffmpeg_concat = 'ffmpeg -re -ss 0 -t {} -f lavfi -i color=c=0x000000:s=640x360:r=30 -i {}{} -filter_complex  \"[1:v]scale=640:360[v1];[0:v][v1]overlay=0:0[outv];{}\"  -map [outv] -map [outa] -vcodec libx264 -acodec aac -f flv {}'
#ffmpeg_concat = 'ffmpeg -re -ss 0 -t {} -f lavfi -i color=c=0x000000:s=640x360:r=30 -i {}{} -filter_complex  \"[1:v]scale=640:360[v1];[0:v][v1]overlay=0:0[outv];{}\"  -map [outv] -map [outa] -vcodec libx264 -acodec copy -f flv {}'
# last_errmsg: Streamcopy requested for output stream 0:1, which is fed from a complex filtergraph. Filtering and streamcopy cannot be used together.
# ffmpeg -re -filter_threads 4 -i aux/coco/李玟_想你的365天.mp3 -ss 0 -t 326.95 -f lavfi -i color=c=0x000000:s=770x432:r=25 -i img/art_coco101.jpg -filter_complex "[2:v]scale=770:432[v2];[1:v][v2]overlay=x=0:y=0[outv];[0:0]concat=n=1:v=0:a=1[outa]" -map [outv] -map [outa] -vcodec libx264 -acodec aac -b:a 320k -y -f mp4 sample_432p_a320k.mp4
# {"cmd":"ffmpeg -filter_threads 1 -i aux/coco/李玟_想你的365天.mp3 -ss 0 -t 326.95 -f lavfi -i color=c=0x000000:s=854x480:r=25 -i img/art_coco122.jpg -filter_complex \"[2:v]scale=854:480[v2];[1:v][v2]overlay=x=0:y=0[outv];[0:0]concat=n=1:v=0:a=1[outa]\" -map [outv] -map [outa] -vcodec libx264 -acodec aac -b:a 320k -f mp4 sample_480p_a320k.mp4"}
#ffmpeg_mp4 = "ffmpeg -i {} -ss 0 -t {} -f lavfi -i color=c=0x000000:s=770x432:r=25 -i {} -filter_complex \"[2:v]scale=770:432[v2];[1:v][v2]overlay=x=0:y=0[outv];[0:0]concat=n=1:v=0:a=1[outa]\" -map [outv] -map [outa] -vcodec libx264 -acodec aac -y -f mp4 {}"
ffmpeg_mp4 = "ffmpeg -i {} -ss 0 -t {} -f lavfi -i color=c=0x000000:s=770x432:r=25 -i {} -filter_complex \"[2:v]scale=770:432[v2];[1:v][v2]overlay=x=0:y=0[outv]\" -map [outv] -map 0:a -r 25 -vcodec libx264 -acodec copy -y -f mp4 {}"
print('pipetest v3.2:',ffmpeg_mp4)
def test(num):
    
    procs = shell.procs_info("ffmpeg")
    if procs:
        shell.OutputShell('ls {} -l'.format(MP4_ROOT),True)
        print('ffmpeg in procs,pass')
        return
    m4alist = mp3list('aux/coco')
    #m4alist = os.listdir(SOURCE_ADUIO_FLODER)   #only name
    imglist = mp3list('img')

    # 先做mp4list里面没有的
    done_num = 0
    for m4a in m4alist:
        if done_num >= num:
                break
        name = file_name(m4a)
        mp4_path = '{}/{}.mp4'.format(MP4_ROOT,name)
        # 更新mp4list
        mp4list = mp4list_by_time(MP4_ROOT)
        print('mp4:',done_num,MP4_ROOT,len(mp4list))
        img = imglist[done_num % len(imglist)]     #imglist must too large
        if not mp4_path in mp4list:
            #没有
            ret = ai_to_mp4(m4a,img)
            if 0 == ret:
                print('ok',done_num,m4a,img)
            else:
                shell.OutputShell('ls {} -l'.format(MP4_ROOT),True)
                print('ffmpeg not return 0',done_num,m4a,img)
                return
            done_num += 1
            time.sleep(3)
    print('mp4list里面没有的,OK')
    # mp4list里面没有的，做完，这里就是都有的了,先最老,mp4list[0]
    # 对MP4_ROOT/sample_432p_a320k.mp4 pass
    mp4_m4a_list = []
    mp4list = mp4list_by_time(MP4_ROOT)
    print('mp4:',done_num,MP4_ROOT,len(mp4list))
    for mp4 in mp4list:
        name = file_name(mp4)
        mp4_src_m4a_path = '{}/{}.m4a'.format(SOURCE_ADUIO_FLODER,name)
        if mp4_src_m4a_path in m4alist:
            mp4_m4a_list.append({"mp4":mp4,"m4a":mp4_src_m4a_path})
    for mp4_m4a in mp4_m4a_list:
        if done_num >= num:
            break
        m4a = mp4_m4a['m4a']
        img = imglist[done_num % len(imglist)]     #imglist must too large
        ret = ai_to_mp4(m4a,img)
        if 0 == ret:
            print('ok',done_num,m4a,img)
        else:
            shell.OutputShell('ls {} -l'.format(MP4_ROOT),True)
            print('ffmpeg not return 0',done_num,m4a,img)
            return
        done_num += 1
        time.sleep(3)
    print('mp4list里面有的,OK')
    shell.OutputShell('ls {} -l'.format(MP4_ROOT),True)

def ai_to_mp4(m4a,img):
    name = file_name(m4a)
    probe = ffmpeg.probe(m4a)
    format = probe.get('format')
    t = float(format.get('duration'))
    cmd = ffmpeg_mp4.format(m4a,t,img,CACHE_MP4_PATH)
    ret = shell.OutputShell(cmd,False)
    if 0 == ret:
        mp4_path = '{}/{}.mp4'.format(MP4_ROOT,name)
        shutil.copy(CACHE_MP4_PATH,mp4_path)
        #os.path.remove(CACHE_MP4_PATH,'{}/{}.mp4'.format(MP4_ROOT,name))
    return ret

def file_name(fullpath,ext=3):
    # 无扩展名
    names = fullpath.split('/')
    name = names[len(names)-1]
    return name[0:-ext-1]

def mp4list_by_time(path="aux/coco"):
    """
    获取mp4最近修改（modify）时间,path列表
    :param path:
    :return:
    """
    # os.path.getctime()：获取文件创建（create）时间
    # os.path.getatime()：获取文件最近访问（access）时间
    # os.path.getmtime()：获取文件最近修改（modify）时间
    mp3list = []
    file_list = []
    if os.path.exists(path):
        for file_name in os.listdir(path):
            #print(os.path.join(path, file_name))
            file_list.append(os.path.join(path, file_name))
        # 获取按照文件时间修改排序的列表，默认是按时间升序
        mp3list = sorted(file_list, key=lambda file: os.path.getmtime(file))
        #random.shuffle(mp3list)
    return mp3list

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

def mp3list(path="aux/coco"):
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
#################### Not need ##############################
    
def testpipe(str_rtmp):
    
    a_concat = ffmpeg.input(sample[0])
    inv = ffmpeg.input('img/art_coco130.jpg', t=IMG_SECONDS, framerate=VIDEO_FRAMERATE, loop=1)
    v_concat = ffmpeg.filter(inv,filter_name='scale', size='hd720')
    
    stream_spec_pipe_rtmp(str_rtmp,v_concat,a_concat, format='rawvideo', pix_fmt='yuv420p',s='1280x720')

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
    #process_stdout.stdout.close()
    #shell.OutputShell('ps -elf | grep ffmpeg',True)
    #process_stdout.wait()
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
    nn = 0
    while True:
        in_bytes = process_stdout.stdout.read(1280*720 * 3)
        if not in_bytes:
            nn += 1
            if nn > 100:
                break
        process_stdin.stdin.write(in_bytes)
    #shell.OutputShell('ps -elf | grep ffmpeg',True)
    process_stdin.stdin.close()
    process_stdout.stdout.close()
    shell.OutputShell('ps -aux | grep ffmpeg',True)
    process_stdout.wait()
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
    nn =0
    while True:
        in_bytes = process_stdout.stdout.read(1280*720 * 3)
        if not in_bytes:
            nn+=1
            if nn > 10000:
                break
        process_stdin.stdin.write(in_bytes)
    #shell.OutputShell('ps -elf | grep ffmpeg',True)
    process_stdin.stdin.close()
    process_stdout.stdout.close()
    shell.OutputShell('ps -elf | grep ffmpeg',True)
    process_stdout.wait()
    process_stdin.wait()


if __name__ == '__main__':
    # python pipetest.py 5
    # <class 'list'> ['pipetest.py', '5']
    rtmp= "http://127.0.0.1:8080"
    try:
        argv = sys.argv[1]
        print(type(argv),argv)
        test(int(argv))
    except:
        print('No argv, sample: python pipetest.py 5')
        test(5)
    #testpipe('pipe0.{}'.format(VIDEO_FORMAT))
    #rtmp_concat_floder(rtmp,[],total=30,artist=None,max_memory=80)
    #rtmp_concat_floder('rtmp',[''],total=3,artist=None,max_memory=80)
