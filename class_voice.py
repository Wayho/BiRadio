# -*- coding: utf-8 -*-
import leancloud
import os
import random
import wss_danmu as wss_danmu
import class_subtitle as class_subtitle

DB_NAME = 'voice'
SOURCE_VOICE_FLODER = 'aux/voice'
AMIX_DEFLAULT = 'l1000.m4a'     #欢迎来到宝宝的直播间

Global_voice_obj_array = []   #from DB

Global_like = []
Global_danmu = []
Global_gift = []
    # SEND_GIFT   = 4                         # 有人送礼
    # GUARD_BUY = 5                           # 有人上舰
    # SUPER_CHAT_MESSAGE = 6  # 醒目留言
#{"time":int,"uid":uid,"uname":uname,"type":MsgType,"message":diff type}
Global_danmu_play = ['麻烦播放','麻烦播','麻烦点歌','麻烦点','请播放','请播','请点歌','请点','点歌','点','播放','播']

print('voice v5.9.0 DB_NAME:',DB_NAME)
# https://peiyin.xunfei.cn/make
# https://peiyin.xunfei.cn/synth?uid=211119012301271462&ts=1691561751&sign=a20ff619b322943058f72f7eaae4ae6f&vid=60140&f=v2&cc=0000&listen=0&sid=211119012301271462&volume=-20&speed=38&content=%5Bte50%5D%E6%AC%A2%E8%BF%8E%E6%9D%A5%E5%88%B0%E6%88%91%E7%9A%84%E7%9B%B4%E6%92%AD%E9%97%B4&normal=1
# 玲姐姐 语速 50    l1001.m4a

def get_amix_voice():
    """
    分别按送礼、弹幕、点赞读取弹幕消息，只处理按价值最高的几条消息
    :return:  {'hasmsg':True/Flase,'mp4':None,'amix':amix}
    :hasmsg:  有无消息，用于前端的随机处理，hasmsg与mp4没有关系
    :mp4:  点的歌
    :amix:  语音obj，肯定不为空, {'type':voice.get('type'),'text':voice.get('text'),'path':file_path}
    """
    global Global_like
    global Global_danmu
    global Global_gift
    danmu = False
    gift = False
    Global_like = wss_danmu.get_like_all()
    Global_danmu = wss_danmu.get_danmu_all()
    Global_gift = wss_danmu.get_gift_all()
    print(Global_gift)
    print(Global_danmu)
    print(Global_like)
    #从价值最高开始处理，danmu分开出来计
    # 先不管谁，重复类型留一个
    if len(Global_gift)!=0:
        Global_gift.sort(key=lambda x:x['type'].value, reverse=True)
        gift = True
        return process_gift()
    if len(Global_danmu)!=0:
        danmu = True
        return process_danmu()
    if len(Global_like)!=0:
        return process_like()
    amix = [{'type':10,'text':'欢迎来到宝宝的直播间','path':os.path.join(SOURCE_VOICE_FLODER, AMIX_DEFLAULT)}]
    return {'hasmsg':False,'mp4':None,'amix':amix}

def process_like():
    global Global_like
    hasmsg = False
    interact = False
    like = False
    amix = []
    for msg in Global_like:
        hasmsg = True
        if msg.get('type') == wss_danmu.MsgType.LIKE_INFO_V3_CLICK:
            like = True
        elif msg.get('type') == wss_danmu.MsgType.INTERACT_WORD:
            interact = True
    if like:
        voice_arr = find_voice(20)
        if voice_arr:
            amix = [voice_arr[0]]
    elif interact:
        voice_arr = find_voice(10)
        if voice_arr:
            amix = [voice_arr[0]]
    if not amix:
        amix = [{'type':10,'text':'欢迎来到宝宝的直播间','path':os.path.join(SOURCE_VOICE_FLODER, AMIX_DEFLAULT)}]
    return  {'hasmsg':hasmsg,'mp4':None,'amix':amix}

def process_danmu():
    global Global_danmu
    hasmsg = False
    mp4 = None
    amix = [{'type':31,'text':'喜欢的话可以点歌，下一首播','path':os.path.join(SOURCE_VOICE_FLODER, 'l3100.m4a')}]
    ret = {}
    for msg in Global_danmu:
        hasmsg = True
        danmu = msg.get('message').msg
        for keyword in Global_danmu_play:
            if keyword == danmu[0:len(keyword)]:
                # 有点歌关键词
                title = danmu[len(keyword):]
                print(keyword,danmu,title)
                subtitle = class_subtitle.get_m4a_name(title)
                if subtitle:
                    # 数据库找到歌
                    mp4 = subtitle.get('name') + '.mp4'
                    voice_arr = find_voice(33)
                    if voice_arr:
                        amix = [voice_arr[0]]
                    return {'hasmsg':hasmsg,'mp4':mp4,'amix':amix}
                else:
                    # 消息没处理完，不着急返回，先准备一个返回值备用
                    amix = [{'type':33,'text':'这首歌没有哦我换首歌送给您！','path':os.path.join(SOURCE_VOICE_FLODER, 'l3300.m4a')}]
                    ret = {'hasmsg':hasmsg,'mp4':mp4,'amix':amix}
    if not ret:
        # 弹幕没点歌，也说点啥
        voice_arr = find_voice(7)   # 某段歌词语音
        if voice_arr:
            amix = [voice_arr[0]]
        ret = {'hasmsg':hasmsg,'mp4':mp4,'amix':amix}
    return ret

def process_gift():
    global Global_gift
    amix = [{'type':40,'text':'谢谢宝宝的礼物','path':os.path.join(SOURCE_VOICE_FLODER, 'l4009.m4a')}]
    return  {'hasmsg':True,'mp4':None,'amix':amix}

def find_voice(itype):
    """
    读数据库，看看语音文件在不在，返回在的列表，已处理好fullpath
    :return: voice_arr {'type':voice.get('type'),'text':voice.get('text'),'path':file_path}
    """
    global Global_voice_obj_array
    find = load_voice_by_type(itype)
    voice_arr = []
    print('find voice',len(find))
    for voice in find:
        file_path = os.path.join(SOURCE_VOICE_FLODER, voice.get('m4a'))
        if  os.path.exists(file_path):
            voice_arr.append({'type':voice.get('type'),'text':voice.get('text'),'path':file_path})
    random.shuffle(voice_arr)
    return voice_arr

def find_curl():
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.limit(100)
    query.equal_to('curl', True)
    return query.find()

    
def load_voice_by_type(type):
    global Global_voice_obj_array
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.limit(100)
    #query.equal_to('on', True)
    query.equal_to('type', type)
    return query.find()

def load_voice():
    global Global_voice_obj_array
    #Global_voice_obj_array = load_voice_db()

if __name__ == '__main__':
    pass