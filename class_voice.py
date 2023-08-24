# -*- coding: utf-8 -*-
import leancloud
import os
import random
import threading
import time
import wss_danmu as wss_danmu
import class_subtitle as class_subtitle
import utils as utils

DB_NAME = 'voice'
SOURCE_VOICE_FLODER = 'aux/voice'
AMIX_DEFLAULT = 'l1000.m4a'     #欢迎来到宝宝的直播间

VOICE_LIST = []

Global_like = []
Global_danmu = []
Global_gift = []
    # SEND_GIFT   = 4                         # 有人送礼
    # GUARD_BUY = 5                           # 有人上舰
    # SUPER_CHAT_MESSAGE = 6  # 醒目留言
#{"time":int,"uid":uid,"uname":uname,"type":MsgType,"message":diff type}好想听，好喜欢，超想听，超爱，超想 点一首
Global_danmu_play = ['好想听','好想播','好想放','好想','想听','听','再听','能听','可以听',
            '好喜欢','喜欢','超想听','超想','超爱',
            '点一首','点首','点歌','点','来一首','来首','来个','播放','播送','播','放',
            '请点一首','请点首','请点歌','请点','请来一首','请来首','请来个','请播放','请播送','请播','请放',
            '麻烦点一首','麻烦点首','麻烦点歌','麻烦点','麻烦来一首','麻烦来首','麻烦来个','麻烦播放','麻烦播送','麻烦播','麻烦放',
            '再点一首','再点首','再点歌','再点','再来一首','再来首','再来个','再播放','再播送','再播','再放',
            '能不能点一首','能不能点首','能不能点歌','能不能点','能不能来一首','能不能来首','能不能来个','能不能播放','能不能播送','能不能播','能不能放',
            '能点一首','能点首','能点歌','能点','能来一首','能来首','能来个','能播放','能播送','能播','能放',
            '可以点一首','可以点首','可以点歌','可以点','可以来一首','可以来首','可以来个','可以播放','可以播送','可以播','可以放',
        ]
Global_danmu_how = [
    ]

print('voice v5.11.0 DB_NAME:',DB_NAME)
# https://peiyin.xunfei.cn/make
# https://peiyin.xunfei.cn/synth?uid=211119012301271462&ts=1691561751&sign=a20ff619b322943058f72f7eaae4ae6f&vid=60140&f=v2&cc=0000&listen=0&sid=211119012301271462&volume=-20&speed=38&content=%5Bte50%5D%E6%AC%A2%E8%BF%8E%E6%9D%A5%E5%88%B0%E6%88%91%E7%9A%84%E7%9B%B4%E6%92%AD%E9%97%B4&normal=1
# 玲姐姐 语速 50    l1001.m4a

def init_voice_list():
    """
    # 每次重启
    """
    global VOICE_LIST
    total_find = 0
    skip = 0
    find =  load_voice(skip,page=100)
    while(len(find)>0):
        total_find += len(find)
        print("total_find",total_find)
        for voice in find:
            file_path = os.path.join(SOURCE_VOICE_FLODER, voice.get('m4a'))
            if  os.path.exists(file_path):
                VOICE_LIST.append({'stype':voice.get('stype'),'gift_id':voice.get('gift_id'),'text':voice.get('text'),'path':file_path})
            else:
                print('File not exist:',voice.get('stype'),voice.get('gift_id'),voice.get('text'),file_path)
        skip += 100
        find =  load_voice(skip,page=100)
    print('init_voice_list:total find={} VOICE_LIST={}'.format(total_find,len(VOICE_LIST)))
timer=threading.Timer(31,init_voice_list,args=())
timer.start()

def get_amix_voice():
    """
    分别按送礼、弹幕、点赞读取弹幕消息，只处理按价值最高的几条消息
    先说欢迎，然后感谢，然后点歌
    如果只有欢迎，在前面加歌词
    :return:  {'hasmsg':True/Flase,'mp4':None,'amix':amix}
    :hasmsg:  有无消息，用于前端的随机处理，hasmsg与mp4没有关系
    :mp4:  点的歌
    :amix:  语音obj，肯定不为空, {'stype':voice.get('stype'),'gift_id':voice.get('gift_id'),'text':voice.get('text'),'path':file_path}
    """
    global Global_like
    global Global_danmu
    global Global_gift
    amix = []
    hasmsg = False
    mp4 = None
    danmu =  {'hasmsg':False,'mp4':None,'amix':[]}
    gift =  {'hasmsg':False,'mp4':None,'amix':[]}
    like =  {'hasmsg':False,'mp4':None,'amix':[]}
    Global_like = wss_danmu.get_like_all()
    Global_danmu = wss_danmu.get_danmu_all()
    Global_gift = wss_danmu.get_gift_all()
    print(Global_gift,Global_danmu,Global_like)
    #从价值最高开始处理，danmu分开出来计
    # mp4 按danmu
    # 先不管谁，重复类型留一个
    interact = process_interact()
    gift = process_gift()
    like = process_like()
    danmu = process_danmu()
    if interact.get('hasmsg'):
        hasmsg = True
        amix.append(interact.get('amix')[0])
    if gift.get('hasmsg'):
        hasmsg = True
        for am in gift.get('amix'):
            amix.append(am)
    if like.get('hasmsg'):
        hasmsg = True
        amix.append(like.get('amix')[0])
    start = time.time()
    if danmu.get('hasmsg'):
        hasmsg = True
        mp4 = danmu.get('mp4')
        amix.append(danmu.get('amix')[0])
    print('get_amix_voice:process_danmu:',time.time()-start)
    if len(amix) <= 1:
        # 必须有一个音频
        voice_arr = find_voice("7",gift_id="0")   # 某段歌词语音
        if voice_arr:
            if len(amix) == 1:
                amix = [voice_arr[0],amix[0]]
            else:
                amix = [voice_arr[0]]
        else:
            if len(amix) == 0:
                amix = [{'stype':"10",'gift_id':"0",'text':'欢迎来到宝宝的直播间','path':os.path.join(SOURCE_VOICE_FLODER, AMIX_DEFLAULT)}]           
    return {'hasmsg':hasmsg,'mp4':mp4,'amix':amix}

def process_interact():
    # INTERACT_WORD:hasmsg = False
    global Global_like
    hasmsg = False
    amix = []
    for msg in Global_like:
        if msg.get('type') == wss_danmu.MsgType.INTERACT_WORD:
            hasmsg = True
    if hasmsg:
        voice_arr = find_voice("10",gift_id="0")
        if voice_arr:
            amix = [voice_arr[0]]
    if not amix:
        amix = [{'stype':"10",'gift_id':"0",'text':'欢迎来到宝宝的直播间','path':os.path.join(SOURCE_VOICE_FLODER, AMIX_DEFLAULT)}]
    return  {'hasmsg':hasmsg,'mp4':None,'amix':amix}

def process_like():
    global Global_like
    hasmsg = False
    amix = []
    for msg in Global_like:
        if msg.get('type') == wss_danmu.MsgType.LIKE_INFO_V3_CLICK:
            hasmsg = True
    if hasmsg:
        voice_arr = find_voice("20",gift_id="0")
        if voice_arr:
            amix = [voice_arr[0]]
    if not amix:
        amix = [{'stype':"20",'gift_id':"0",'text':'谢谢宝宝的点赞','path':os.path.join(SOURCE_VOICE_FLODER, 'l2002')}]
    return  {'hasmsg':hasmsg,'mp4':None,'amix':amix}

def process_danmu():
    #amix只有0/1内容
    global Global_danmu
    hasmsg = False
    mp4 = None
    amix = [{'stype':"31",'gift_id':"0",'text':'喜欢的话可以点歌，下一首播','path':os.path.join(SOURCE_VOICE_FLODER, 'l3100.m4a')}]
    ret = {'hasmsg':False,'mp4':None,'amix':[]}
    for msg in Global_danmu:
        danmu = utils.lower_delete_punctuation_and_emoj(msg.get('message').msg)
        for keyword in Global_danmu_play:
            if keyword == danmu[0:len(keyword)]:
                # 有点歌关键词
                hasmsg = True
                title = danmu[len(keyword):]
                print(keyword,danmu,title)
                subtitle = class_subtitle.get_m4a_name(title)
                if subtitle:
                    # 数据库找到歌
                    mp4 = subtitle.get('name') + '.mp4'
                    voice_arr = find_voice("33",gift_id="0")
                    if voice_arr:
                        amix = voice_arr
                    return {'hasmsg':hasmsg,'mp4':mp4,'amix':amix}
                else:
                    # 消息没处理完，不着急返回，先准备一个返回值备用
                    amix = [{'stype':"333",'gift_id':"0",'text':'这首歌没有哦我换首歌送给您！','path':os.path.join(SOURCE_VOICE_FLODER, 'l3300.m4a')}]
                    ret = {'hasmsg':hasmsg,'mp4':mp4,'amix':amix}
        if not hasmsg:
            # 不能适配关键词，试试直接歌名
            print('try song name',danmu)
            subtitle = class_subtitle.get_m4a_name(danmu)
            if subtitle:
                # 数据库找到歌
                mp4 = subtitle.get('name') + '.mp4'
                hasmsg = True
                voice_arr = find_voice("33",gift_id="0")
                if voice_arr:
                    amix = voice_arr
                return {'hasmsg':hasmsg,'mp4':mp4,'amix':amix}
    return ret

def process_gift():
    global Global_gift
    hasmsg = False
    amix = []
    #Global_gift.sort(key=lambda x:x['type'].value, reverse=True)
    try:
        for msg in Global_gift:
            hasmsg = True
            #print('#'*40,'GIFT message={}'.format(msg.get('message')))
            gift_id = msg.get('message').gift_id
            voice_arr = find_voice("4",gift_id)
            if voice_arr:
                if not is_gift_id_in_amix(voice_arr[0].get('gift_id'),amix):
                    # 一种礼物留一个语音
                    amix.append(voice_arr[0])
    except:
        print('gift error')
    if not amix:
        # 没有匹配的语音，用默认
        amix = [{'stype':"4",'gift_id':"30000",'text':'谢谢宝宝的礼物','path':os.path.join(SOURCE_VOICE_FLODER, 'l4009.m4a')}]
    return  {'hasmsg':hasmsg,'mp4':None,'amix':amix}

def is_gift_id_in_amix(gift_id,amix):
    for a_obj in amix:
        if gift_id == a_obj.get('gift_id'):
            return True
    return False

def find_voice(stype,gift_id="0"):
    """
    读ram，看看语音文件在不在，返回在的列表，已处理好fullpath
    :return: voice_arr {'stype':voice.get('stype'),'gift_id':voice.get('gift_id'),'text':voice.get('text'),'path':file_path}
    """
    if len(VOICE_LIST)==0:
        return find_voice_db(stype,gift_id)
    voice_arr = []
    for voice in VOICE_LIST:
        if "4"==stype:
            if voice.get('gift_id')==gift_id:
                voice_arr.append(voice)
        else:
            if voice.get('stype')==stype:
                voice_arr.append(voice)
    print('find voice len={} stype={} gift_id={}'.format(len(voice_arr),stype,gift_id))
    random.shuffle(voice_arr)
    return voice_arr

def find_voice_db(stype,gift_id="0"):
    """
    读数据库，看看语音文件在不在，返回在的列表，已处理好fullpath
    :return: voice_arr {'stype':voice.get('stype'),'gift_id':voice.get('gift_id'),'text':voice.get('text'),'path':file_path}
    """
    find = load_voice_by_type(stype,gift_id)
    voice_arr = []
    for voice in find:
        file_path = os.path.join(SOURCE_VOICE_FLODER, voice.get('m4a'))
        if  os.path.exists(file_path):
            voice_arr.append({'stype':voice.get('stype'),'gift_id':voice.get('gift_id'),'text':voice.get('text'),'path':file_path})
    print('find voice from db len={} stype={} gift_id={}'.format(len(voice_arr),stype,gift_id))
    random.shuffle(voice_arr)
    return voice_arr

def find_curl():
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.limit(100)
    query.equal_to('curl', True)
    return query.find()

    
def load_voice_by_type(stype,gift_id):
    # gift type == 4
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.select(['text', 'm4a', 'stype', 'gift_id','-objectId','-createdAt', '-updatedAt'])
    query.limit(150)
    #query.equal_to('on', True)
    if "4"==stype:
        query.equal_to('gift_id', gift_id)
    else:
        query.equal_to('stype', stype)
    return query.find()

def load_voice(skip=0,page=100):
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.limit(page)
    query.skip(skip)
    #query.equal_to('on', True)
    query.ascending('m4a')
    return  query.find()

if __name__ == '__main__':
    pass