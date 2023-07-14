# coding: utf-8
import requests
import time
import class_variable as class_variable

def tryStartLive():
    live_status = getRoom_live_status()
    if 0==live_status:
        return startLive()
    return {"code":live_status, "rtmp":None}

###########################################################
# https://link.bilibili.com/p/center/index#/my-room/start-live
# https://api.live.bilibili.com/room/v1/Room/startLive
# 请求头
# POST /room/v1/Room/startLive HTTP/1.1
# Host: api.live.bilibili.com
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: application/json, text/plain, */*
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Referer: https://link.bilibili.com/p/center/index?visit_id=9ad3vc184yyo
# Content-Type: application/x-www-form-urlencoded; charset=UTF-8
# Content-Length: 122
# Origin: https://link.bilibili.com
# Connection: keep-alive
# Cookie: CURRENT_FNVAL=4048; blackside_state=0; PVID=3; buvid_fp=729cdf417a68b28b8c4460abcb848244; CURRENT_BLACKGAP=0; buvid4=51E9A338-9398-30FD-79B6-66BE70478E3859395-022061517-evGPtmzq9mS4FLeL9SwcZcGLHBxu%2BpcV3jIk91w1fNXgtAHaLFVYuA%3D%3D; LIVE_BUVID=AUTO4816553411747335; i-wanna-go-back=-1; b_ut=5; fingerprint=729cdf417a68b28b8c4460abcb848244; buvid_fp_plain=undefined; SESSDATA=a9ad8e96%2C1700006742%2Ce7b9c%2A52; bili_jct=87405b0f1bc27ab69aed36a41bfd1899; DedeUserID=1737442657; DedeUserID__ckMd5=9c213abdbe66d1ae; CURRENT_QUALITY=16; nostalgia_conf=-1; hit-dyn-v2=1; fingerprint3=51cfcf9172ceffa6746f041b84422696; b_nut=100; is-2022-channel=1; rpdid=|(k||u)mJY0J'uYY)l~kR)Y; hit-new-style-dyn=0; _uuid=51010CAE41-13610-10319-F21E-1056DB9E7D811088245infoc; theme_style=light; sid=6dj9uaju; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=1373-771; buvid3=E4B0EFF0-58A7-40D6-BAF5-FDE28935C06D148805infoc; bp_video_offset_1737442657=797187080480358400; b_lsid=98A2E411_18832AA95AF; innersign=0; _dfcaptcha=85a74f364782dc7ff7ed428fcd442c2c
# Pragma: no-cache
# Cache-Control: no-cache

# POST数据
# room_id=27791346
# platform=pc
# area_v2=192
# csrf_token=87405b0f1bc27ab69aed36a41bfd1899
# csrf=87405b0f1bc27ab69aed36a41bfd1899

# result
#       {"code":0,"data":{"change":1,"status":"LIVE","try_time":"0000-00-00 00:00:00","room_type":0,"live_key":"366480222136569842","sub_session_key":"366480222136569842sub_time:1684480035","rtmp":{"addr":"rtmp://live-push.bilivideo.com/live-bvc/","code":"?streamname=live_1737442657_89779234&key=22d0f9797bf072eb015148d5558d8099&schedule=rtmp&pflag=1","new_link":"https://core.bilivideo.com/video/uplinkcore/selfbuild/schedule?up_rtmp=live-push.bilivideo.com%2Flive-bvc%2F%3Fstreamname%3Dlive_1737442657_89779234%26key%3D22d0f9797bf072eb015148d5558d8099%26schedule%3Drtmp%26pflag%3D1&edge=edge","provider":"live"},"protocols":[{"protocol":"rtmp","addr":"rtmp://live-push.bilivideo.com/live-bvc/","code":"?streamname=live_1737442657_89779234&key=22d0f9797bf072eb015148d5558d8099&schedule=rtmp&pflag=1","new_link":"https://core.bilivideo.com/video/uplinkcore/selfbuild/schedule?up_rtmp=live-push.bilivideo.com%2Flive-bvc%2F%3Fstreamname%3Dlive_1737442657_89779234%26key%3D22d0f9797bf072eb015148d5558d8099%26schedule%3Drtmp%26pflag%3D1&edge=edge","provider":"txy"}],"notice":{"type":1,"status":0,"title":"","msg":"","button_text":"","button_url":""},"qr":"","need_face_auth":false,"service_source":"room-service"},"message":"","msg":""}
# call {'code': 0, 'data': {'change': 1, 'status': 'LIVE', 'try_time': '0000-00-00 00:00:00', 'room_type': 0, 'live_key': '370281439992221682', 'sub_session_key': '370281439992221682sub_time:1685586055', 'rtmp': {'addr': 'rtmp://live-push.bilivideo.com/live-bvc/', 'code': '?streamname=live_1737442657_89779234&key=22d0f9797bf072eb015148d5558d8099&schedule=rtmp&pflag=1', 'new_link': 'https://core.bilivideo.com/video/uplinkcore/selfbuild/schedule?up_rtmp=live-push.bilivideo.com%2Flive-bvc%2F%3Fstreamname%3Dlive_1737442657_89779234%26key%3D22d0f9797bf072eb015148d5558d8099%26schedule%3Drtmp%26pflag%3D1&edge=edge', 'provider': 'live'}, 'protocols': [{'protocol': 'rtmp', 'addr': 'rtmp://live-push.bilivideo.com/live-bvc/', 'code': '?streamname=live_1737442657_89779234&key=22d0f9797bf072eb015148d5558d8099&schedule=rtmp&pflag=1', 'new_link': 'https://core.bilivideo.com/video/uplinkcore/selfbuild/schedule?up_rtmp=live-push.bilivideo.com%2Flive-bvc%2F%3Fstreamname%3Dlive_1737442657_89779234%26key%3D22d0f9797bf072eb015148d5558d8099%26schedule%3Drtmp%26pflag%3D1&edge=edge', 'provider': 'txy'}], 'notice': {'type': 1, 'status': 0, 'title': '', 'msg': '', 'button_text': '', 'button_url': ''}, 'qr': '', 'need_face_auth': False, 'service_source': 'room-service'}, 'message': '', 'msg': ''}
###########################################################
def startLive():
    # {"code":0,"data":{"change":1,"status":"LIVE","try_time":"0000-00-00 00:00:00","room_type":0,
    COOKIES = class_variable.getCookies()
    url = 'https://api.live.bilibili.com/room/v1/Room/startLive'
    data = {
        'room_id':'27791346',               # 这个是直播房间的id号
        'platform':'pc',               # 平台
        'area_v2':'192',                    # 聊天电台
        'rnd':str(int(time.time())),   # 这个是时间戳
        'csrf_token':COOKIES['csrf_token'],
        'csrf': COOKIES['csrf'],
    }            
    headers = {
        'cookie': COOKIES['cookie'],
        'origin': 'https://link.bilibili.com',
        'referer': 'https://link.bilibili.com/p/center/index#/my-room/start-live',
        'user-agent': 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    }

    response = requests.post(url,data=data,headers=headers)
    res = response.json()
    print(res)
    return {"code":res['code'], "rtmp":res['data']['rtmp']}

###########################################################
# https://api.live.bilibili.com/room/v1/Room/stopLive
# 请求头
# POST /room/v1/Room/stopLive HTTP/1.1
# Host: api.live.bilibili.com
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: application/json, text/plain, */*
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Referer: https://link.bilibili.com/p/center/index?visit_id=9ad3vc184yyo
# Content-Type: application/x-www-form-urlencoded; charset=UTF-8
# Content-Length: 110
# Origin: https://link.bilibili.com
# Connection: keep-alive
# Cookie: CURRENT_FNVAL=4048; blackside_state=0; PVID=4; buvid_fp=729cdf417a68b28b8c4460abcb848244; CURRENT_BLACKGAP=0; buvid4=51E9A338-9398-30FD-79B6-66BE70478E3859395-022061517-evGPtmzq9mS4FLeL9SwcZcGLHBxu%2BpcV3jIk91w1fNXgtAHaLFVYuA%3D%3D; LIVE_BUVID=AUTO4816553411747335; i-wanna-go-back=-1; b_ut=5; fingerprint=729cdf417a68b28b8c4460abcb848244; buvid_fp_plain=undefined; SESSDATA=a0b8bd80%2C1700275367%2C317fd%2A52; bili_jct=86f340e7ff3ca5b640bcb1523ec7d86e; DedeUserID=1737442657; DedeUserID__ckMd5=9c213abdbe66d1ae; CURRENT_QUALITY=16; nostalgia_conf=-1; hit-dyn-v2=1; fingerprint3=51cfcf9172ceffa6746f041b84422696; b_nut=100; is-2022-channel=1; rpdid=|(k||u)mJY0J'uYY)l~kR)Y; hit-new-style-dyn=0; _uuid=51010CAE41-13610-10319-F21E-1056DB9E7D811088245infoc; theme_style=light; sid=7gj2bi7x; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=1373-771; buvid3=E4B0EFF0-58A7-40D6-BAF5-FDE28935C06D148805infoc; bp_video_offset_1737442657=797187080480358400; b_lsid=45EB1E10E_1884156427F; innersign=1; bsource=search_sougo; _dfcaptcha=801b2988d2caf0eac219e91534da8d4b
# Pragma: no-cache
# Cache-Control: no-cache

# POST数据
# room_id=27791346
# platform=pc
# csrf_token=86f340e7ff3ca5b640bcb1523ec7d86e
# csrf=86f340e7ff3ca5b640bcb1523ec7d86e

# result
# {"code":0,"msg":"","message":"","data":{"change":1,"status":"PREPARING"}}
###########################################################
###########################################################
# https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo?room_id=27791346&protocol=0,1&format=0,1,2&codec=0,1&qn=0&platform=web&ptype=8&dolby=5&panorama=1
# 请求头
# GET /xlive/web-room/v2/index/getRoomPlayInfo?room_id=27791346&protocol=0,1&format=0,1,2&codec=0,1&qn=10000&platform=web&ptype=8&dolby=5&panorama=1 HTTP/1.1
# Host: api.live.bilibili.com
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: */*
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Referer: https://live.bilibili.com/27791346
# Origin: https://live.bilibili.com
# Connection: keep-alive
# Cookie: CURRENT_FNVAL=4048; blackside_state=0; PVID=7; buvid_fp=729cdf417a68b28b8c4460abcb848244; CURRENT_BLACKGAP=0; buvid4=51E9A338-9398-30FD-79B6-66BE70478E3859395-022061517-evGPtmzq9mS4FLeL9SwcZcGLHBxu%2BpcV3jIk91w1fNXgtAHaLFVYuA%3D%3D; LIVE_BUVID=AUTO4816553411747335; i-wanna-go-back=-1; b_ut=5; fingerprint=729cdf417a68b28b8c4460abcb848244; buvid_fp_plain=undefined; SESSDATA=a0b8bd80%2C1700275367%2C317fd%2A52; bili_jct=86f340e7ff3ca5b640bcb1523ec7d86e; DedeUserID=1737442657; DedeUserID__ckMd5=9c213abdbe66d1ae; CURRENT_QUALITY=16; nostalgia_conf=-1; hit-dyn-v2=1; fingerprint3=51cfcf9172ceffa6746f041b84422696; b_nut=100; is-2022-channel=1; rpdid=|(k||u)mJY0J'uYY)l~kR)Y; hit-new-style-dyn=0; _uuid=51010CAE41-13610-10319-F21E-1056DB9E7D811088245infoc; theme_style=light; sid=7gj2bi7x; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=1373-771; buvid3=E4B0EFF0-58A7-40D6-BAF5-FDE28935C06D148805infoc; bp_video_offset_1737442657=797187080480358400; b_lsid=45EB1E10E_1884156427F; innersign=1; bsource=search_sougo; _dfcaptcha=801b2988d2caf0eac219e91534da8d4b
# Pragma: no-cache
# Cache-Control: no-cache

# result
# {"code":0,"message":"0","ttl":1,"data":{"room_id":27791346,"short_id":0,"uid":1737442657,"is_hidden":false,"is_locked":false,"is_portrait":false,"live_status":1,"hidden_till":0,"lock_till":0,"encrypted":false,"pwd_verified":true,"live_time":1684725662,"room_shield":0,"all_special_types":[],"playurl_info":{"conf_json":"{\"cdn_rate\":10000,\"report_interval_sec\":150}","playurl":{"cid":27791346,"g_qn_desc":[{"qn":30000,"desc":"杜比","hdr_desc":"","attr_desc":null},{"qn":20000,"desc":"4K","hdr_desc":"","attr_desc":null},{"qn":10000,"desc":"原画","hdr_desc":"","attr_desc":null},{"qn":400,"desc":"蓝光","hdr_desc":"HDR","attr_desc":null},{"qn":250,"desc":"超清","hdr_desc":"HDR","attr_desc":null},{"qn":150,"desc":"高清","hdr_desc":"","attr_desc":null},{"qn":80,"desc":"流畅","hdr_desc":"","attr_desc":null}],"stream":[{"protocol_name":"http_stream","format":[{"format_name":"flv","codec":[{"codec_name":"avc","current_qn":10000,"accept_qn":[10000],"base_url":"/live-bvc/238232/live_1737442657_89779234.flv?","url_info":[{"host":"https://cn-jxnc-cm-01-11.bilivideo.com","extra":"expires=1684729710&pt=web&deadline=1684729710&len=0&oi=0x2409896a05580267dcedd3a1901d2fe3&platform=web&qn=10000&trid=1000260393c8194b44b19095fc1a477112b5&uipk=100&uipv=100&nbs=1&uparams=cdn,deadline,len,oi,platform,qn,trid,uipk,uipv,nbs&cdn=cn-gotcha01&upsig=ea5d20e2f422226e5f61f7a72acd3082&sk=cc16e243d61363d44194927863825fbd&p2p_type=1&sl=1&free_type=0&mid=1737442657&sid=cn-jxnc-cm-01-11&chash=1&bmt=1&sche=ban&score=1&pp=rtmp&source=onetier&trace=10c9&site=60121caf24ce819edead4e54171f4760&order=1","stream_ttl":3600}],"hdr_qn":null,"dolby_type":0,"attr_name":""}]}]},{"protocol_name":"http_hls","format":[{"format_name":"ts","codec":[{"codec_name":"avc","current_qn":10000,"accept_qn":[10000],"base_url":"/live-bvc/238232/live_1737442657_89779234.m3u8?","url_info":[{"host":"https://d1--cn-gotcha101.bilivideo.com","extra":"expires=1684729710&len=0&oi=0x2409896a05580267dcedd3a1901d2fe3&pt=web&qn=10000&trid=1003260393c8194b44b19095fc1a477112b5&sigparams=cdn,expires,len,oi,pt,qn,trid&cdn=cn-gotcha01&sign=b1106602bf50f22073984ddb496dfdf1&sk=cc16e243d61363d44194927863825fbd&p2p_type=1&sl=1&free_type=0&mid=1737442657&pp=rtmp&source=onetier&trace=40&site=60121caf24ce819edead4e54171f4760&order=1","stream_ttl":3600}],"hdr_qn":null,"dolby_type":0,"attr_name":""}]}]}],"p2p_data":{"p2p":true,"p2p_type":1,"m_p2p":false,"m_servers":null},"dolby_qn":null}},"official_type":0,"official_room_id":0}}
###########################################################
def getRoom_live_status():
    # {"code":0,"message":"0","ttl":1,"data":{"room_id":27791346,"short_id":0,"uid":1737442657,"is_hidden":false,"is_locked":false,"is_portrait":false,"live_status":1,
    #COOKIES = class_variable.getCookies()
    url = 'https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo?room_id=27791346&protocol=0,1&format=0,1,2&codec=0,1&qn=0&platform=web&ptype=8&dolby=5&panorama=1'
    headers = {
        #'cookie': COOKIES['cookie'],
        'origin': 'https://live.bilibili.com',
        'referer': 'https://live.bilibili.com/27791346',
        'user-agent': 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    }

    response = requests.get(url,headers=headers)
    res = response.json()
    if 0 != res['code']:
        print(res)
        return 999
    return res.get('data').get('live_status')

###########################################################
# https://api.live.bilibili.com/room/v1/Room/update
# 请求头
# POST /room/v1/Room/update HTTP/1.1
# Host: api.live.bilibili.com
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: application/json, text/plain, */*
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Referer: https://link.bilibili.com/p/center/index?visit_id=9ad3vc184yyo
# Content-Type: application/x-www-form-urlencoded; charset=UTF-8
# Content-Length: 225
# Origin: https://link.bilibili.com
# Connection: keep-alive
# Cookie: CURRENT_FNVAL=4048; blackside_state=0; PVID=2; buvid_fp=729cdf417a68b28b8c4460abcb848244; CURRENT_BLACKGAP=0; buvid4=51E9A338-9398-30FD-79B6-66BE70478E3859395-022061517-evGPtmzq9mS4FLeL9SwcZcGLHBxu%2BpcV3jIk91w1fNXgtAHaLFVYuA%3D%3D; LIVE_BUVID=AUTO4816553411747335; i-wanna-go-back=-1; b_ut=5; fingerprint=729cdf417a68b28b8c4460abcb848244; buvid_fp_plain=undefined; SESSDATA=a0b8bd80%2C1700275367%2C317fd%2A52; bili_jct=86f340e7ff3ca5b640bcb1523ec7d86e; DedeUserID=1737442657; DedeUserID__ckMd5=9c213abdbe66d1ae; CURRENT_QUALITY=16; nostalgia_conf=-1; hit-dyn-v2=1; fingerprint3=51cfcf9172ceffa6746f041b84422696; b_nut=100; is-2022-channel=1; rpdid=|(k||u)mJY0J'uYY)l~kR)Y; hit-new-style-dyn=0; _uuid=51010CAE41-13610-10319-F21E-1056DB9E7D811088245infoc; theme_style=light; sid=7gj2bi7x; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=1373-771; buvid3=E4B0EFF0-58A7-40D6-BAF5-FDE28935C06D148805infoc; bp_video_offset_1737442657=797187080480358400; b_lsid=3FED6A17_18855FF2E98; innersign=1; bsource=search_sougo; _dfcaptcha=be9d1e030763be0de01f321ebca30068
# Pragma: no-cache
# Cache-Control: no-cache

# POST数据
# room_id=27791346
# title=试播 | 经典英文歌 | 极其音乐 
# csrf_token=86f340e7ff3ca5b640bcb1523ec7d86e
# csrf=86f340e7ff3ca5b640bcb1523ec7d86e

# result
# {"code":0,"msg":"ok","message":"ok","data":[]}
###########################################################
def update_RadioName(title):
    if len(title) < 5:
        print('updateRoomTitle:string must >5',title)
        return
    COOKIES = class_variable.getCookies()
    url = 'https://api.live.bilibili.com/room/v1/Room/update'
    data = {
        'room_id':'27791346',               # 这个是直播房间的id号
        'title':title, 
        'csrf_token':COOKIES['csrf_token'],
        'csrf': COOKIES['csrf'],
    }            
    headers = {
        'cookie': COOKIES['cookie'],
        'origin': 'https://link.bilibili.com',
        'referer': 'https://link.bilibili.com/p/center/index#/my-room/start-live',
        'user-agent': 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    }

    response = requests.post(url,data=data,headers=headers)
    res = response.json()
    print(res)
    return res['code']

###########################################################
# https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo?room_ids=27791346&req_biz=link-center
# 请求头
# GET /xlive/web-room/v1/index/getRoomBaseInfo?room_ids=27791346&req_biz=link-center HTTP/1.1
# Host: api.live.bilibili.com
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: application/json, text/plain, */*
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Referer: https://link.bilibili.com/p/center/index
# Origin: https://link.bilibili.com
# Connection: keep-alive
# Cookie: CURRENT_FNVAL=4048; blackside_state=0; PVID=8; buvid_fp=729cdf417a68b28b8c4460abcb848244; CURRENT_BLACKGAP=0; buvid4=51E9A338-9398-30FD-79B6-66BE70478E3859395-022061517-evGPtmzq9mS4FLeL9SwcZcGLHBxu%2BpcV3jIk91w1fNXgtAHaLFVYuA%3D%3D; LIVE_BUVID=AUTO4816553411747335; i-wanna-go-back=-1; b_ut=5; fingerprint=729cdf417a68b28b8c4460abcb848244; buvid_fp_plain=undefined; SESSDATA=a0b8bd80%2C1700275367%2C317fd%2A52; bili_jct=86f340e7ff3ca5b640bcb1523ec7d86e; DedeUserID=1737442657; DedeUserID__ckMd5=9c213abdbe66d1ae; CURRENT_QUALITY=16; nostalgia_conf=-1; hit-dyn-v2=1; fingerprint3=51cfcf9172ceffa6746f041b84422696; b_nut=100; is-2022-channel=1; rpdid=|(k||u)mJY0J'uYY)l~kR)Y; hit-new-style-dyn=0; _uuid=51010CAE41-13610-10319-F21E-1056DB9E7D811088245infoc; theme_style=light; sid=7gj2bi7x; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=1373-771; buvid3=E4B0EFF0-58A7-40D6-BAF5-FDE28935C06D148805infoc; bp_video_offset_1737442657=797187080480358400; b_lsid=5B5348A4_18856A4293C; innersign=1; bsource=search_sougo; _dfcaptcha=fd4144c83aef4fdf2a4351a43de4a08e
# Pragma: no-cache
# Cache-Control: no-cache

# result
# {"code":0,"message":"0","ttl":1,"data":{"by_uids":{},"by_room_ids":{"27791346":{"room_id":27791346,"uid":1737442657,"area_id":192,"live_status":1,"live_url":"https://live.bilibili.com/27791346","parent_area_id":5,"title":"试播 | 欧美流行歌曲 | 极其音乐","parent_area_name":"电台","area_name":"聊天电台","live_time":"2023-05-26 14:07:29","description":"只播音乐,暂时不回弹幕","tags":"音乐爱好者","attention":1260,"online":5,"short_id":0,"uname":"CC双语_中英CC字幕","cover":"https://i0.hdslb.com/bfs/live/1f25d8747696d488e93cf6feaa986eff614f49c5.png","background":"","join_slide":1,"live_id":368537653205274600,"live_id_str":"368537653205274610"}}}}
###########################################################
def getRoomBaseInfo():
    url = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo?room_ids=27791346&req_biz=link-center'
    headers = {
        #'cookie': COOKIES['cookie'],
        'origin': 'https://live.bilibili.com',
        'referer': 'https://link.bilibili.com/p/center/index',
        'user-agent': 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    }

    response = requests.get(url,headers=headers)
    res = response.json()
    if 0 != res['code']:
        print(res)
    return res

if __name__ == '__main__':
    a=1
    res = getRoomBaseInfo()
    RadioName = res.get('data').get('by_room_ids').get('27791346').get('title')
    print(RadioName)
    # retcode =updateRoomTitle('试播 | 欧美流行歌曲 | 极其音乐')
    # print(retcode)
