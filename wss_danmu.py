# -*- coding: utf-8 -*-
import asyncio
import random
import time
import blivedm
import os
from queue import Queue
import class_viewer
from enum import Enum
 # 继承枚举类
class MsgType(Enum):
    INTERACT_WORD = 1               #入场消息
    LIKE_INFO_V3_CLICK = 2      #Like消息
    DANMU_MSG  = 3                      # 收到弹幕
    SEND_GIFT   = 4                         # 有人送礼
    GUARD_BUY = 5                           # 有人上舰
    SUPER_CHAT_MESSAGE = 6  # 醒目留言
    #SUPER_CHAT_MESSAGE_DELETE = 7# 删除醒目留言

ROOM_IDS = [
    30356247,
    30338274,
    27791346
]


Global_30s_times = 0
__Global_like_queue = Queue()  # 创建进入、点赞队列对象
__Global_danmu_queue = Queue()  # 创建弹幕队列对象
__Global_gift_queue = Queue()  # 创建送礼队列对象
#{"time":int,"uid":uid,"uname":uname,"type":MsgType,"message":diff type}

print('wss_danmu v5.6.0 ROOM_IDS:',ROOM_IDS)

####################### class_voice #########################################
def put_like(uid,uname,type,message):
    global __Global_like_queue
    now = time.time()
    msg = {
        "time":now,
        "uid":uid,
        "uname":uname,
        "type":type,
        "message":message
    }
    __Global_like_queue.put(msg)

def get_like_all():
    global __Global_like_queue
    msg_arr = []
    while not __Global_like_queue.empty():
        msg = __Global_like_queue.get()
        msg_arr.append(msg)
    return msg_arr

def put_danmu(uid,uname,type,message):
    global __Global_danmu_queue
    now = time.time()
    msg = {
        "time":now,
        "uid":uid,
        "uname":uname,
        "type":type,
        "message":message
    }
    __Global_danmu_queue.put(msg)

def get_danmu_all():
    global __Global_danmu_queue
    msg_arr = []
    while not __Global_danmu_queue.empty():
        msg = __Global_danmu_queue.get()
        msg_arr.append(msg)
    return msg_arr

def put_gift(uid,uname,type,message):
    global __Global_gift_queue
    now = time.time()
    msg = {
        "time":now,
        "uid":uid,
        "uname":uname,
        "type":type,
        "message":message
    }
    __Global_gift_queue.put(msg)

def get_gift_all():
    global __Global_gift_queue
    msg_arr = []
    while not __Global_gift_queue.empty():
        msg = __Global_gift_queue.get()
        msg_arr.append(msg)
    return msg_arr
################################################################

async def start_client(room_id):
    #room_id = 23718393 #ROOM_ID#27791346
    # 如果SSL验证失败就把ssl设为False，B站真的有过忘续证书的情况
    client = blivedm.BLiveClient(room_id, ssl=True)
    handler = MyHandler()
    client.add_handler(handler)
    client.start()
    try:
        # 演示5秒后停止
        await asyncio.sleep(12*60*60)
        client.stop()
        await client.join()
    finally:
        await client.stop_and_close()

class MyHandler(blivedm.BaseHandler):
    # # 演示如何添加自定义回调
    _CMD_CALLBACK_DICT = blivedm.BaseHandler._CMD_CALLBACK_DICT.copy()
    #
    # # 入场消息回调
    async def __interact_word_callback(self, client: blivedm.BLiveClient, command: dict):
        # print(f"[{client.room_id}] INTERACT_WORD: self_type={type(self).__name__}, room_id={client.room_id},"
        #       f" uname={command['data']['uname']}")
        put_like(command['data']['uid'],command['data']['uname'],MsgType.INTERACT_WORD,None)
        obj = class_viewer.new_viewer(client.room_id,command['data']['uid'],command['data']['uname'])
        if obj:
            print(ROOM_IDS[0],obj.get('t_'+str(ROOM_IDS[0])),ROOM_IDS[1],obj.get('t_'+str(ROOM_IDS[1])),ROOM_IDS[2],obj.get('t_'+str(ROOM_IDS[2])),"like:",obj.get('like'),obj.get('uid'),obj.get('uname'))
        else:
            print(f"INTERACT_WORD: {command['data']['uname']}")
    _CMD_CALLBACK_DICT['INTERACT_WORD'] = __interact_word_callback  # noqa

    # # Like消息回调
    async def __like_info_v3_click_callback(self, client: blivedm.BLiveClient, command: dict):
        # print(f"[{client.room_id}] LIKE_INFO_V3_CLICK: self_type={type(self).__name__}, room_id={client.room_id},"
        #       f" uname={command['data']['uname']}")
        put_like(command['data']['uid'],command['data']['uname'],MsgType.LIKE_INFO_V3_CLICK,None)
        obj = class_viewer.like(command['data']['uid'])
        if obj:
            print(ROOM_IDS[0],obj.get('t_'+str(ROOM_IDS[0])),ROOM_IDS[1],obj.get('t_'+str(ROOM_IDS[1])),"like:",obj.get('like'),obj.get('uid'),obj.get('uname'))
        else:
            print(f"LIKE_INFO_V3_CLICK: {command['data']['uname']}")
    _CMD_CALLBACK_DICT['LIKE_INFO_V3_CLICK'] = __like_info_v3_click_callback

    # #watch消息回调
    async def __watch_change_callback(self, client: blivedm.BLiveClient, command: dict):
        print(f"[{client.room_id}] WATCHED_CHANGE: self_type={type(self).__name__}, room_id={client.room_id},"
              f" num={command['data']['num']}")
    _CMD_CALLBACK_DICT['WATCHED_CHANGE'] = __watch_change_callback

    async def _on_heartbeat(self, client: blivedm.BLiveClient, message: blivedm.HeartbeatMessage):
        global Global_30s_times
        if Global_30s_times % 20==0:
            print(f'[{client.room_id}] 当前人气值：{message.popularity}')
        Global_30s_times += 1

    async def _on_danmaku(self, client: blivedm.BLiveClient, message: blivedm.DanmakuMessage):
        put_danmu(message.uid,message.uname,MsgType.DANMU_MSG,message)
        print(f'[{client.room_id}] {message.uname}：{message.msg}')

    async def _on_gift(self, client: blivedm.BLiveClient, message: blivedm.GiftMessage):
        put_gift(message.uid,message.uname,MsgType.SEND_GIFT,message)
        print(f'[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
              f' （{message.coin_type}瓜子x{message.total_coin}）')

    async def _on_buy_guard(self, client: blivedm.BLiveClient, message: blivedm.GuardBuyMessage):
        put_gift(message.uid,message.username,MsgType.GUARD_BUY,message)
        print(f'[{client.room_id}] {message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, client: blivedm.BLiveClient, message: blivedm.SuperChatMessage):
        put_gift(message.uid,message.username,MsgType.SUPER_CHAT_MESSAGE,message)
        print(f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')

def start(room_id):
    asyncio.run(start_client(room_id))

if __name__ == '__main__':
    asyncio.run(start_client(ROOM_IDS[0]))
    #asyncio.run(await_start())
