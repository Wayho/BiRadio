# -*- coding: UTF-8 -*-
import os
import requests
print('ding_msg v1.3 ')

def dingMe(WEBHOOK_DINGDING,content):
    mHeader = {'Content-Type': 'application/json; charset=UTF-8'}
    mBody = {
        "text": {
            "content":'dingMe:'+content
        },
        "msgtype": "text"
    }
    # 注意：json=mBody  必须用json    
    r = requests.post(url=WEBHOOK_DINGDING, json=mBody, headers=mHeader)
    return r.text

def sendText(WEBHOOK_DINGDING,content):
    mHeader = {'Content-Type': 'application/json; charset=UTF-8'}
    mBody = {
        "text": {
            "content":content
        },
        "msgtype": "text"
    }
    # 注意：json=mBody  必须用json    
    r = requests.post(url=WEBHOOK_DINGDING, json=mBody, headers=mHeader)
    return r.text

# def sendVideoMarkdown(videoInfo):
#     screenshot = AZURE_HOME + "/download?url=https://i.ytimg.com/vi/" + videoInfo.get("id") +"/mqdefault.jpg"
#     link = AZURE_HOME + "/relayvideo?id=" + videoInfo.get("id")
#     text =  " ![screenshot](" + screenshot + ")\n" 
#     text +=  videoInfo.get("title") + "\n " 
#     text +="[" + videoInfo.get("id") +"](" + link +")\n"
#     text +=  videoInfo.get("name") + "\n " 
#     text +=  videoInfo.get("channel_id") + "\n" 
#     text +=  videoInfo.get("published") + "\n" 
#     text +=  videoInfo.get("updated") + "\n" 
#     sendMarkdown(videoInfo.get("id"), text)

def sendMarkdown(WEBHOOK_DINGDING,title,text):
    mHeader = {'Content-Type': 'application/json; charset=UTF-8'}
    mBody = {
        "markdown": {
         "title":title,
         "text": text
     },
        "msgtype": "markdown"
    }
    # 注意：json=mBody  必须用json    
    r = requests.post(url=WEBHOOK_DINGDING, json=mBody, headers=mHeader)
    return r.text