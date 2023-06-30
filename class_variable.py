# -*- coding: utf-8 -*-
import leancloud							#requirements leancloud-sdk>=1.0.9,<=2.0.0
import os
import json
from datetime import datetime,timedelta

COOKIES_PATH = 'cookies.json'
OBJECT_ID = '63ec4afc14f21573cb450921'
HOURS_NEW_DAY = 11
print("class_variable v1.1 HOURS_NEW_DAY=",HOURS_NEW_DAY)
#63ec4afc14f21573cb450921是variable中唯一的一行的objectId

# {
#   "BILIBILI_RTMP": "rtmp://live-push.bilivideo.com/live-bvc/",
#   "BILIBILI_CLMY": "?streamname=live_1737442657_89779234&key=22d0f9797bf072eb015148d5558d8099&schedule=rtmp&pflag=1",
#   "RADIO_NAME": "欧美流行歌曲 | 极其音乐",
#  "CHANGE_RADIO_NAME": false,
#   "PLAY_ARTIST": false,
#   "FFMPEG_MESSAGE_OUT": false,
#   "MP3_TOTAL_PLAY": 200,
#   "SLEEP": 60,
#   "MAX_DOWNLOAD": 30,
#   "MAX_MEMORY": 200,
#   "MAX_MEMORY_PY": 400,
#   "ERROR_RETRY": 5
# }

def weekday():
    now_newday = datetime.now() + timedelta(hours = -HOURS_NEW_DAY)
    #print(HOURS_NEW_DAY,now_newday)
    return now_newday.weekday()

def get_config():
    VClass = leancloud.Object.extend( "variable" )
    query = VClass.query
    variable = query.get(OBJECT_ID)
    config = variable.get('config')
    return config

def get_download_enable():
    """
    获取是否允许下载
    :param :
    :return T/F:
    """
    VClass = leancloud.Object.extend( "variable" )
    query = VClass.query
    variable = query.get(OBJECT_ID)
    return variable.get('download')

def get_timeout():
    """
    获取timeout
    :param :
    :return timeout:
    """
    VClass = leancloud.Object.extend( "variable" )
    query = VClass.query
    variable = query.get(OBJECT_ID)
    return variable.get('timeout')

def get_today_AP():
    """
    获取星期几哪个台起作用
    :param :
    :return sitename:今天是哪个台==SITENAME
    """
    VClass = leancloud.Object.extend( "variable" )
    query = VClass.query
    variable = query.get(OBJECT_ID)
    site_ap = variable.get('week_ap')
    today = weekday()
    tomorrow = today+1
    if tomorrow > 6:
        tomorrow = 0
    return (site_ap[today],site_ap[tomorrow])

def set_today_AP(sitename,am=False):
    """
    设置今天哪个台起作用
    :param sitename:
    :param am=False:am or pm
    :return :今天是哪个台==sitename
    """
    VClass = leancloud.Object.extend( "variable" )
    query = VClass.query
    variable = query.get(OBJECT_ID)
    site_list = variable.get('week_ap')
    new_v = VClass.create_without_data(OBJECT_ID)
    weekday = weekday()
    old = site_list[weekday]
    if am:
        ap = [sitename,old[1]]
    else:
        ap = [old[0],sitename]
    site_list[weekday] = ap
    new_v.set('week_ap', site_list)
    new_v.save()
    print('DB week today', old,'has update to',ap)

def set_tomorrow_AP(sitename,am=False):
    """
    设置明天哪个台起作用
    :param sitename:
    :param am=False:am or pm
    :return :今天是哪个台==sitename
    """
    VClass = leancloud.Object.extend( "variable" )
    query = VClass.query
    variable = query.get(OBJECT_ID)
    site_list = variable.get('week_ap')
    new_v = VClass.create_without_data(OBJECT_ID)
    tomorrow = (weekday() + 1) % 7
    old = site_list[tomorrow]
    if am:
        ap = [sitename,old[1]]
    else:
        ap = [old[0],sitename]
    site_list[tomorrow] = ap
    new_v.set('week_ap', site_list)
    new_v.save()
    print('DB week tomorrow', old,'has update to',ap)
##########################

def get_today_sitename():
    """
    获取星期几哪个台起作用
    :param :
    :return sitename:今天是哪个台==SITENAME
    """
    VClass = leancloud.Object.extend( "variable" )
    query = VClass.query
    variable = query.get(OBJECT_ID)
    sitename = variable.get('week')
    today = weekday()
    tomorrow = today+1
    if tomorrow > 6:
        tomorrow = 0
    return (sitename[today],sitename[tomorrow])

def set_today_sitename(sitename):
    """
    设置今天哪个台起作用
    :param sitename:
    :return :今天是哪个台==sitename
    """
    VClass = leancloud.Object.extend( "variable" )
    query = VClass.query
    variable = query.get(OBJECT_ID)
    site_list = variable.get('week')
    new_v = VClass.create_without_data(OBJECT_ID)
    weekday = weekday()
    old = site_list[weekday]
    site_list[weekday] = sitename
    new_v.set('week', site_list)
    new_v.save()
    print('DB week today', old,'has update to',sitename)

def set_tomorrow_sitename(sitename):
    """
    设置明天哪个台起作用
    :param sitename:
    :return :今天是哪个台==sitename
    """
    VClass = leancloud.Object.extend( "variable" )
    query = VClass.query
    variable = query.get(OBJECT_ID)
    site_list = variable.get('week')
    new_v = VClass.create_without_data(OBJECT_ID)
    tomorrow = weekday() + 1
    old = site_list[tomorrow%6]
    site_list[tomorrow] = sitename
    new_v.set('week', site_list)
    new_v.save()
    print('DB week tomorrow', old,'has update to',sitename)

def getCookies():
    with open(COOKIES_PATH,'r',encoding='utf-8') as fp :
        cookie_obj = json.load(fp)
        cookies = cookie_obj['cookie_info']['cookies']
        cookies_str = ''
        for cookies_item in cookies:
            cookies_str += cookies_item['name'] + '=' + cookies_item['value'] + '; '
        
        csrf = cookie_obj['cookie_info']['cookies'][1]['value']
        csrf_token = cookie_obj['token_info']['access_token']
        ret = {'cookie':cookies_str,'csrf':csrf, 'csrf_token':csrf_token}
        #print(ret)
        return ret

def SaveCookiesFromDB():
    # 生成cookies.json
    #if not os.path.exists(COOKIES_PATH):
    #部署时不要上传cookies.json，cookies.json由定时云函数进行创建
    VClass = leancloud.Object.extend( "variable" )
    query = VClass.query
    #variable = query.first()
    variable = query.get(OBJECT_ID)
    #63ec4afc14f21573cb450921是variable中唯一的一行的objectId
    cookies = variable.get('cookies')
    if None != cookies:
        time_db = cookies['cookie_info']['cookies'][0]['expires']
        date_time = datetime.fromtimestamp(time_db)
        print('SaveCookiesFromDB::time_db:',time_db,date_time)
        with open('cookies.json', 'w') as fp:
            json.dump(cookies, fp,indent=2)
    
        

def Json2DB():
    with open(COOKIES_PATH,'r',encoding='utf-8') as fp :
        cookies = json.load(fp)
        time_file = cookies['cookie_info']['cookies'][0]['expires']
        date_time = datetime.fromtimestamp(time_file)
        print('Json2DB::time_file:',time_file,date_time)
        VClass = leancloud.Object.extend('variable')
        query = VClass.query
        variable = query.get(OBJECT_ID)
        cookies_db = variable.get('cookies')
        if None != cookies_db:
            time_db = cookies_db['cookie_info']['cookies'][0]['expires']
            date_time = datetime.fromtimestamp(time_db)
            print('Json2DB::time_db:',time_db,date_time)
            if time_file > time_db:
                new_v = VClass.create_without_data(OBJECT_ID)
                #63ec4afc14f21573cb450921是variable中唯一的一行的objectId
                new_v.set('cookies', cookies)
                new_v.save()
                print('DB cookies has update')

if __name__ == '__main__':
    getCookies()