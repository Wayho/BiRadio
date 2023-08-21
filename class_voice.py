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
#{"time":int,"uid":uid,"uname":uname,"type":MsgType,"message":diff type}好想听，好喜欢，超想听，超爱，超想
Global_danmu_play = ['好想听','好想播','好想放','好想','想听','听',
            '好喜欢','喜欢','超想听','超想','超爱',
            '麻烦播放','麻烦播送','麻烦播','麻烦点歌','麻烦点',
            '请播放','请播送','请播','请点歌','请点',
            '点歌','点','播放','播送','播',
            '能不能点歌','能不能点','能不能播放','能不能播送','能不能播','能不能听','能不能放',
            '能点歌','能点','能播放','能播送','能播','能听','能放',
            '可以点歌','可以点','可以播放','可以播送','可以播','可以听','可以放']
Global_danmu_how = [
    ]

print('voice v5.9.6 DB_NAME:',DB_NAME)
# https://peiyin.xunfei.cn/make
# https://peiyin.xunfei.cn/synth?uid=211119012301271462&ts=1691561751&sign=a20ff619b322943058f72f7eaae4ae6f&vid=60140&f=v2&cc=0000&listen=0&sid=211119012301271462&volume=-20&speed=38&content=%5Bte50%5D%E6%AC%A2%E8%BF%8E%E6%9D%A5%E5%88%B0%E6%88%91%E7%9A%84%E7%9B%B4%E6%92%AD%E9%97%B4&normal=1
# 玲姐姐 语速 50    l1001.m4a

def get_amix_voice():
    """
    分别按送礼、弹幕、点赞读取弹幕消息，只处理按价值最高的几条消息
    :return:  {'hasmsg':True/Flase,'mp4':None,'amix':amix}
    :hasmsg:  有无消息，用于前端的随机处理，hasmsg与mp4没有关系
    :mp4:  点的歌
    :amix:  语音obj，肯定不为空, {'type':voice.get('type'),'gift_id':voice.get('gift_id'),'text':voice.get('text'),'path':file_path}
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
    amix = [{'type':10,'gift_id':0,'text':'欢迎来到宝宝的直播间','path':os.path.join(SOURCE_VOICE_FLODER, AMIX_DEFLAULT)}]
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
        voice_arr = find_voice(20,gift_id=0)
        if voice_arr:
            amix = [voice_arr[0]]
    elif interact:
        voice_arr = find_voice(10,gift_id=0)
        if voice_arr:
            amix = [voice_arr[0]]
    if not amix:
        amix = [{'type':10,'gift_id':0,'text':'欢迎来到宝宝的直播间','path':os.path.join(SOURCE_VOICE_FLODER, AMIX_DEFLAULT)}]
    return  {'hasmsg':hasmsg,'mp4':None,'amix':amix}

def process_danmu():
    global Global_danmu
    hasmsg = False
    mp4 = None
    amix = [{'type':31,'gift_id':0,'text':'喜欢的话可以点歌，下一首播','path':os.path.join(SOURCE_VOICE_FLODER, 'l3100.m4a')}]
    ret = {}
    for msg in Global_danmu:
        hasmsg = True
        danmu = msg.get('message').msg
        for keyword in Global_danmu_play:
            if keyword == danmu[0:len(keyword)]:
                # 有点歌关键词
                song_name = danmu[len(keyword):].split('吗')
                title = song_name[0]
                print(keyword,danmu,title)
                subtitle = class_subtitle.get_m4a_name(title)
                if subtitle:
                    # 数据库找到歌
                    mp4 = subtitle.get('name') + '.mp4'
                    voice_arr = find_voice(33,gift_id=0)
                    if voice_arr:
                        amix = voice_arr
                    return {'hasmsg':hasmsg,'mp4':mp4,'amix':amix}
                else:
                    # 消息没处理完，不着急返回，先准备一个返回值备用
                    amix = [{'type':333,'gift_id':0,'text':'这首歌没有哦我换首歌送给您！','path':os.path.join(SOURCE_VOICE_FLODER, 'l3300.m4a')}]
                    ret = {'hasmsg':hasmsg,'mp4':mp4,'amix':amix}
        # can't shipei paly,try title
        title = danmu
        print(keyword,danmu,title)
        subtitle = class_subtitle.get_m4a_name(title)
        if subtitle:
            # 数据库找到歌
            mp4 = subtitle.get('name') + '.mp4'
            voice_arr = find_voice(33,gift_id=0)
            if voice_arr:
                amix = voice_arr
            return {'hasmsg':hasmsg,'mp4':mp4,'amix':amix}
    if not ret:
        # 弹幕没点歌，也说点啥
        voice_arr = find_voice(7,gift_id=0)   # 某段歌词语音
        if voice_arr:
            amix = [voice_arr[0],amix[0]]
        ret = {'hasmsg':hasmsg,'mp4':mp4,'amix':amix}
    return ret

def process_gift():
    global Global_gift
    amix = []
    try:
        for msg in Global_gift:
            #print('#'*40,'GIFT message={}'.format(msg.get('message')))
            gift_id = msg.get('message').gift_id
            voice_arr = find_voice(4,gift_id)
            if voice_arr:
                if not is_gift_id_in_amix(voice_arr[0].get('gift_id'),amix):
                    # 一种礼物留一个语音
                    amix.append(voice_arr[0])
    except:
        print('gift error')
    if not amix:
        # 没有匹配的语音，用默认
        amix = [{'type':4,'gift_id':30000,'text':'谢谢宝宝的礼物','path':os.path.join(SOURCE_VOICE_FLODER, 'l4009.m4a')}]
    return  {'hasmsg':True,'mp4':None,'amix':amix}

def is_gift_id_in_amix(gift_id,amix):
    for a_obj in amix:
        if gift_id == a_obj.get('gift_id'):
            return True
    return False

def find_voice(itype,gift_id=0):
    """
    读数据库，看看语音文件在不在，返回在的列表，已处理好fullpath
    :return: voice_arr {'type':voice.get('type'),'gift_id':voice.get('gift_id'),'text':voice.get('text'),'path':file_path}
    """
    global Global_voice_obj_array
    find = load_voice_by_type(itype,gift_id)
    voice_arr = []
    print('find voice',len(find))
    for voice in find:
        file_path = os.path.join(SOURCE_VOICE_FLODER, voice.get('m4a'))
        if  os.path.exists(file_path):
            voice_arr.append({'type':voice.get('type'),'gift_id':voice.get('gift_id'),'text':voice.get('text'),'path':file_path})
    random.shuffle(voice_arr)
    return voice_arr

def find_curl():
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.limit(100)
    query.equal_to('curl', True)
    return query.find()

    
def load_voice_by_type(itype,gift_id):
    # gift type == 4
    global Global_voice_obj_array
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.limit(100)
    #query.equal_to('on', True)
    if 4==itype:
        query.equal_to('gift_id', gift_id)
    else:
        query.equal_to('type', itype)
    return query.find()

def load_voice():
    global Global_voice_obj_array
    #Global_voice_obj_array = load_voice_db()

if __name__ == '__main__':
    pass