# -*- coding: utf-8 -*-
import leancloud
import random
import wss_danmu as wss_danmu
import class_subtitle as class_subtitle

DB_NAME = 'voice'

Global_voice_obj_array = []   #from DB
Global_voice_amix = []  # for stream 1维

Global_like = []
Global_danmu = []
Global_gift = []
    # SEND_GIFT   = 4                         # 有人送礼
    # GUARD_BUY = 5                           # 有人上舰
    # SUPER_CHAT_MESSAGE = 6  # 醒目留言
#{"time":int,"uid":uid,"uname":uname,"type":MsgType,"message":diff type}
Global_danmu_play = ['点','播放','请点','请点']

print('voice v5.8.0 DB_NAME:',DB_NAME)
# https://peiyin.xunfei.cn/make
# https://peiyin.xunfei.cn/synth?uid=211119012301271462&ts=1691561751&sign=a20ff619b322943058f72f7eaae4ae6f&vid=60140&f=v2&cc=0000&listen=0&sid=211119012301271462&volume=-20&speed=38&content=%5Bte50%5D%E6%AC%A2%E8%BF%8E%E6%9D%A5%E5%88%B0%E6%88%91%E7%9A%84%E7%9B%B4%E6%92%AD%E9%97%B4&normal=1
# 玲姐姐 语速 50    l1001.m4a

def get_amix_voice():
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
    return None

def process_like():
    global Global_voice_amix
    global Global_like
    interact = False
    like = False
    for msg in Global_like:
        if msg.get('type') == wss_danmu.MsgType.LIKE_INFO_V3_CLICK:
            like = True
        elif msg.get('type') == wss_danmu.MsgType.INTERACT_WORD:
            interact = True
    if like:
        voice_arr = find_voice(20)
        if voice_arr:
             Global_voice_amix = [voice_arr[0].get('m4a')]
    elif interact:
        voice_arr = find_voice(10)
        if voice_arr:
             Global_voice_amix = [voice_arr[0].get('m4a')]
    return {'mp4':None,'amix':Global_voice_amix}

def process_danmu():
    global Global_voice_amix
    global Global_danmu
    mp4 = None
    Global_voice_amix = ['l3120.m4a']
    ret = {}
    for msg in Global_danmu:
        danmu = msg.get('message').msg
        for keyword in Global_danmu_play:
            if keyword == danmu[0:len(keyword)]:
                title = danmu[len(keyword):]
                print(keyword,danmu,title)
                subtitle = class_subtitle.get_m4a_name(title)
                if subtitle:
                    mp4 = subtitle.get('name') + '.mp4'
                    voice_arr = find_voice(33)
                    if voice_arr:
                        Global_voice_amix = [voice_arr[0].get('m4a')]
                        return {'mp4':mp4,'amix':Global_voice_amix}
                    else:
                        return {'mp4':mp4,'amix':[]}
                else:
                    Global_voice_amix = 'l3300.m4a'
                    ret = {'mp4':mp4,'amix':Global_voice_amix}
    if ret:
        return ret
    return {'mp4':mp4,'amix':Global_voice_amix}

def process_gift():
    global Global_voice_amix
    global Global_gift
    Global_voice_amix = ['l4009.m4a']
    return  {'mp4':None,'amix':Global_voice_amix}

def find_voice(itype):
    global Global_voice_obj_array
    find = load_voice_by_type(itype)
    voice_arr = []
    print('find voice',len(find))
    for voice in find:
        #if voice.get('type')==itype:
            voice_arr.append(voice)
            print(voice.get('m4a'),voice.get('text'),voice.get('type'))
    random.shuffle(voice_arr)
    return voice_arr
    
def load_voice_by_type(type):
    global Global_voice_obj_array
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    #query.limit(1000)
    #query.equal_to('on', True)
    query.equal_to('type', type)
    return query.find()

def load_voice():
    global Global_voice_obj_array
    #Global_voice_obj_array = load_voice_db()

if __name__ == '__main__':
    pass