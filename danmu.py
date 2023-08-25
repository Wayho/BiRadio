# coding: utf-8

import requests
import time
import threading
import class_variable as class_variable

TIME_LAST_DANMU_SEND = time.time()      # 上次弹幕发送时间
SECONDS_BETWEEN_DANMU = 6                   #弹幕发送时间间隔
print('danmu v5.9.1:SECONDS_BETWEEN_DANMU=',SECONDS_BETWEEN_DANMU)

def delay_send(room_id,msg,delay=5):
    # 延时执行发送弹幕
    # 自行决定避免发送太快
    global TIME_LAST_DANMU_SEND
    now = time.time()
    delta = now-TIME_LAST_DANMU_SEND - SECONDS_BETWEEN_DANMU
    if delta < 0: 
        delay = delay - delta
    TIME_LAST_DANMU_SEND = now+delay
    timer=threading.Timer(delay,send,args=(room_id,msg,))
    timer.start()
###########################################################
# https://api.live.bilibili.com/msg/send
# 请求头
# POST /msg/send HTTP/1.1
# Host: api.live.bilibili.com
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: */*
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Referer: https://live.bilibili.com/27791346
# Content-Type: multipart/form-data; boundary=---------------------------40503028312528542463548396133
# Origin: https://live.bilibili.com
# Content-Length: 1391
# Connection: keep-alive
# Cookie: CURRENT_FNVAL=4048; blackside_state=0; PVID=7; buvid_fp=729cdf417a68b28b8c4460abcb848244; CURRENT_BLACKGAP=0; buvid4=51E9A338-9398-30FD-79B6-66BE70478E3859395-022061517-evGPtmzq9mS4FLeL9SwcZcGLHBxu%2BpcV3jIk91w1fNXgtAHaLFVYuA%3D%3D; LIVE_BUVID=AUTO4816553411747335; i-wanna-go-back=-1; b_ut=5; fingerprint=729cdf417a68b28b8c4460abcb848244; buvid_fp_plain=undefined; SESSDATA=a9ad8e96%2C1700006742%2Ce7b9c%2A52; bili_jct=87405b0f1bc27ab69aed36a41bfd1899; DedeUserID=1737442657; DedeUserID__ckMd5=9c213abdbe66d1ae; CURRENT_QUALITY=16; nostalgia_conf=-1; hit-dyn-v2=1; fingerprint3=51cfcf9172ceffa6746f041b84422696; b_nut=100; is-2022-channel=1; rpdid=|(k||u)mJY0J'uYY)l~kR)Y; hit-new-style-dyn=0; _uuid=51010CAE41-13610-10319-F21E-1056DB9E7D811088245infoc; theme_style=light; sid=6dj9uaju; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=1373-771; buvid3=E4B0EFF0-58A7-40D6-BAF5-FDE28935C06D148805infoc; bp_video_offset_1737442657=797187080480358400; b_lsid=98A2E411_18832AA95AF; innersign=0; _dfcaptcha=85a74f364782dc7ff7ed428fcd442c2c
# Pragma: no-cache
# Cache-Control: no-cache

# POST数据
# -----------------------------40503028312528542463548396133
# Content-Disposition: form-data; name="bubble"

# 0
# -----------------------------40503028312528542463548396133
# Content-Disposition: form-data; name="msg"

# 极其音乐
# -----------------------------40503028312528542463548396133
# Content-Disposition: form-data; name="color"

# 16777215
# -----------------------------40503028312528542463548396133
# Content-Disposition: form-data; name="mode"

# 1
# -----------------------------40503028312528542463548396133
# Content-Disposition: form-data; name="room_type"

# 0
# -----------------------------40503028312528542463548396133
# Content-Disposition: form-data; name="jumpfrom"

# 0
# -----------------------------40503028312528542463548396133
# Content-Disposition: form-data; name="fontsize"

# 25
# -----------------------------40503028312528542463548396133
# Content-Disposition: form-data; name="rnd"

# 1684480440
# -----------------------------40503028312528542463548396133
# Content-Disposition: form-data; name="roomid"

# 27791346
# -----------------------------40503028312528542463548396133
# Content-Disposition: form-data; name="csrf"

# 87405b0f1bc27ab69aed36a41bfd1899
# -----------------------------40503028312528542463548396133
# Content-Disposition: form-data; name="csrf_token"

# 87405b0f1bc27ab69aed36a41bfd1899
# -----------------------------40503028312528542463548396133--


# result
# {"code":0,"data":{"mode_info":{"mode":0,"show_player_type":0,"extra":"{\"send_from_me\":true,\"mode\":0,\"color\":16777215,\"dm_type\":0,\"font_size\":25,\"player_mode\":1,\"show_player_type\":0,\"content\":\"极其音乐\",\"user_hash\":\"3815732837\",\"emoticon_unique\":\"\",\"bulge_display\":0,\"recommend_score\":1,\"main_state_dm_color\":\"\",\"objective_state_dm_color\":\"\",\"direction\":0,\"pk_direction\":0,\"quartet_direction\":0,\"anniversary_crowd\":0,\"yeah_space_type\":\"\",\"yeah_space_url\":\"\",\"jump_to_url\":\"\",\"space_type\":\"\",\"space_url\":\"\",\"animation\":{},\"emots\":null,\"is_audited\":false,\"id_str\":\"6e9e2278dd93e22f69db7c07c35654d713\"}"},"dm_v2":"CiI2ZTllMjI3OGRkOTNlMjJmNjlkYjdjMDdjMzU2NTRkNzEzEAEYGSD///8HKghlMzZmNzY2NTIM5p6B5YW26Z+z5LmQOO/Q8paDMUi4w5yjBmIAigEAkAEBmgEQCggxREVDNzk3MBD1w5yjBqIBiQEI4Yq9vAYSF0ND5Y+M6K+tX+S4reiLsUND5a2X5bmVIkpodHRwczovL2kxLmhkc2xiLmNvbS9iZnMvZmFjZS9kNzBlYzlhZGZhNzA5YTg1YWFmZTliMjFhMDNkZTgyNDExMzM0ZTA4LmpwZziQTkABWgIIAWIPEJat2gQaBj41MDAwMCABagByAKoBBRjyn6AN"},"message":"","msg":""}
###########################################################
# https://api.live.bilibili.com/xlive/web-room/v1/index/getDanmuInfo?id=27791346&type=0
# {"code":0,"message":"0","ttl":1,"data":{"group":"live","business_id":0,"refresh_row_factor":0.125,"refresh_rate":100,"max_delay":5000,"token":"Q2OPtrqAjyWngWKn-9E0Mxr5mrH2bmYHjSgZ27IzEu9ZFXbEBGFWafCkNOmuAjV_47rjSZV9NrQEWMzxrOfHETDpbbU_BBhenvi8v91wrLh_jobSuymTKU2dZbdYeym990qXEfN_ilQKZAuRPTCcrMahdG0IU_KCPXzYp7_UHxEl","host_list":[{"host":"dsa-cn-live-comet-01.chat.bilibili.com","port":2243,"wss_port":2245,"ws_port":2244},{"host":"tx-sh-live-comet-03.chat.bilibili.com","port":2243,"wss_port":2245,"ws_port":2244},{"host":"hw-sh-live-comet-03.chat.bilibili.com","port":2243,"wss_port":2245,"ws_port":2244},{"host":"broadcastlv.chat.bilibili.com","port":2243,"wss_port":2245,"ws_port":2244}]}}
###########################################################
# https://blog.csdn.net/npccccccccc/article/details/124576745
def send(room_id,msg):
    # {'code': 0, 'data': {'mode_info': {'mode': 0, 'show_player_type': 0
    # {'code': -101, 'message': '账号未登录', 'ttl': 1}
    # {'code': -111, 'message': 'csrf 校验失败', 'ttl': 1}
    room_id = str(room_id)
    if len(room_id)<3:
        return 0
    if not msg:
        return 0
    if len(msg)==0:
        return 0
    msg = msg[0:20]
    COOKIES = class_variable.getCookies()
    url = 'https://api.live.bilibili.com/msg/send'
    data = {
        'color':'16777215',            # 颜色
        'fontsize':'25',               # 字体大小
        'mode':'1',                    # 模式
        'msg':msg,                    # 消息内容
        'rnd':str(int(time.time())),   # 这个是时间戳
        'roomid':room_id,#'27791346',               # 这个是直播房间的id号
        'bubble':'0',
        'room_type':'0',
        'csrf_token':COOKIES['csrf_token'],
        'csrf': COOKIES['csrf'],
    }            
    headers = {
        'cookie': COOKIES['cookie'],
        'origin': 'https://live.bilibili.com',
        'referer': 'https://live.bilibili.com/{}'.format(room_id),
        'user-agent': 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    }

    response = requests.post(url,data=data,headers=headers)
    res = response.json()
    if 0 != res['code']:
        print(res)
    return res['code']
    # 系统对消息的敏感内容有屏蔽措施

def barrage():
    url = "http://api.live.bilibili.com/ajax/msg?roomid="
    room = "27791346"
    res = requests.get(url+room).json()
    res = res['data']['room'][-1]
    print(res)

if __name__ == '__main__':
    # retcode =send('')
    # print(retcode)
    barrage()
