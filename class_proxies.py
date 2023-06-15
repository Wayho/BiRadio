# coding: utf-8

import requests
import time
import leancloud
import base64
import json
import os
from urllib import parse
import random
import class_variable as class_variable


USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'
# https://www.kuaidaili.com/free/inha/2/
Global_Best_Proxies = {}
###########################################################
###########################################################
def get_response(url,headers,allow_redirects=True,timeout=None): 
    # def requests.request(method, url,
    # params=None, 
    # data=None, 
    # headers=None, 
    # cookies=None,
    # timeout=None, 
    # allow_redirects=True, 
    # proxies=None,
    # verify=None,  
    # json=None):
    """
    proxies requests.get
    :param url:url
    :param headers:headers
    :param allow_redirects:allow_redirects
    :param timeout:timeout
    :return: requests.get
    """
    best_obj = Global_Best_Proxies
    headers['User-Agent'] = USER_AGENT
    ipport = best_obj.get('ip') + ":" + best_obj.get('port')
    proxies_type = best_obj.get('type')
    if 'http' == proxies_type:
        proxies = {"http": "http://" + ipport}
    elif 'https' == proxies_type:
        proxies = {"https": "https://" + ipport}
    else:
        print('Unknow Type', proxies_type,ipport)
        proxies = {"http": "http://0.0.0.0:8888"  }
    #proxies = {"http": "http://114.231.45.51:8888"  }
    
    if None == timeout:
        timeout = class_variable.get_timeout()
    starttime = time.time()
    if allow_redirects:
        response = requests.get(url,headers=headers,proxies=proxies, timeout=timeout)
    else:
        response = requests.get(url,headers=headers,proxies=proxies, timeout=timeout, allow_redirects=False)
    endtime = time.time()
    print('proxies:',proxies,best_obj.get('bad'),'end-start time=',(endtime-starttime)*1000)
    if 'OK'==response.reason:
        bad(best_obj.get('objectId'),10)
    elif 'Moved Temporarily'==response.reason:
        bad(best_obj.get('objectId'),10)
    else:
        bad(best_obj.get('objectId'),300)
        print('get_response:',response.reason,response.headers)
    return response
###########################################################
###########################################################
def post_response(url,headers,data): 
    """
    proxies requests.get
    :param url:url
    :param headers:headers
    :param allow_redirects:allow_redirects
    :param timeout:timeout
    :return: requests.get
    """
    best_obj = Global_Best_Proxies
    headers['User-Agent'] = USER_AGENT
    ipport = best_obj.get('ip') + ":" + best_obj.get('port')
    proxies_type = best_obj.get('type')
    if 'http' == proxies_type:
        proxies = {"http": "http://" + ipport}
    elif 'https' == proxies_type:
        proxies = {"https": "https://" + ipport}
    else:
        print('Unknow Type', proxies_type,ipport)
        proxies = {"http": "http://0.0.0.0:8888"  }
        bad(best_obj.get('objectId'),999999)
    #proxies = {"http": "http://114.231.45.51:8888"  }
    timeout = class_variable.get_timeout()
    starttime = time.time()
    response = requests.post(url,data=data,headers=headers)
    endtime = time.time()
    print('proxies:',proxies,best_obj.get('bad'),'end-start time=',(endtime-starttime)*1000)
    if 'OK'==response.reason:
        bad(best_obj.get('objectId'),10)
    elif 'Moved Temporarily'==response.reason:
        bad(best_obj.get('objectId'),10)
    else:
        bad(best_obj.get('objectId'),300)
        print('post_response:',response.reason,response.headers)
    return response
###########################################################
###########################################################
def proxies_array():
    # return array
    DBClass = leancloud.Object.extend( "proxies" )
    query = DBClass.query
    query.ascending('bad')
    return query.find()

def best_proxies():
    global Global_Best_Proxies
    DBClass = leancloud.Object.extend( "proxies" )
    query = DBClass.query
    query.ascending('bad')
    Global_Best_Proxies = query.first()
    set_USER_AGENT()
    return Global_Best_Proxies

def bad(objectId,bad):
    DBClass = leancloud.Object.extend( "proxies" )
    proxy = DBClass.create_without_data(objectId)
    proxy.increment('bad', int(bad))
    proxy.save()

def update():
    # 待升级
    DBClass = leancloud.Object.extend( "proxies" )
    return 0

def set_USER_AGENT():
    global USER_AGENT
    with open("./user_agent.txt", "r") as ftext:
        txtlines = ftext.readlines()
        ftext.close()
        agentlist = []
        for line in txtlines:
            line = line.strip( '\n' )
            agentlist.append(line)
        random.shuffle(agentlist)
        USER_AGENT = agentlist[0]
        #print( "USER_AGENT:",USER_AGENT)

###########################################################
def test(): 
    url = 'https://www.baidu.com'
    Referer = 'https://www.baidu.com'
    headers = {
        'Connection': 'close',
        'referer': Referer,
        'user-agent': USER_AGENT
    }
    response = get_response(url=url,headers=headers,allow_redirects=False,new_proxies=True)
    print('test::',response.reason,response.content[0:200])
    time.sleep(5)
    response = get_response(url=url,headers=headers,allow_redirects=False,new_proxies=False)
    print('test::',response.reason,response.content[0:200])
    return response
###########################################################

if __name__ == '__main__':
    ss = '01-The-Beatles-yesterday.zip'
    # print(ss[-3:len(ss)])
    # print(ss[0:-4])
    #unzip_cache('img','filename.jpg')
    test()
