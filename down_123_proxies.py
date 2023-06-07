# coding: utf-8

#import requests
import time

import base64
import json
import os
from urllib import parse
import zipfile
import random
import class_variable as class_variable
import class_proxies as class_proxies
import gc
import psutil

MP3_ROOT = 'mp3'
IMG_FLODER = 'img'
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'
###########################################################
# https://www.123pan.com/s/MrBtVv-KUxpA.html提取码:9945
# GET https://www.123pan.com/b/api/share/get?limit=100&next=1&orderBy=share_id&orderDirection=desc&shareKey=MrBtVv-DUxpA&SharePwd=9945&ParentFileId=0&Page=1
# 请求头
# GET /b/api/share/get?limit=100&next=1&orderBy=share_id&orderDirection=desc&shareKey=MrBtVv-DUxpA&SharePwd=9945&ParentFileId=0&Page=1 HTTP/1.1
# Host: www.123pan.com
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: */*
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# platform: web
# App-Version: 3
# Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODYwMTcyMzAsImlhdCI6MTY4NTQxMjQzMCwiaWQiOjE4MTUxODE1MjQsIm5pY2tuYW1lIjoiMTM2MzkxMDk5NDUiLCJzdXBwZXIiOmZhbHNlLCJ1c2VybmFtZSI6MTM2MzkxMDk5NDUsInYiOjB9.r7ygoPcR8GDMYgiQ4qKO4k0S_uNQBzE_Ej7n_Hxd_VE
# Connection: keep-alive
# Referer: https://www.123pan.com/s/MrBtVv-DUxpA.html
# Cookie: UM_distinctid=188462e8395414-01ffec5b65d7718-7f2c6753-13c680-188462e839668e; CNZZDATA1280304515=1889281670-1684804468-%7C1684883187; Hm_lvt_d815f2e1f682c86565c1063aafaef292=1684804643; Hm_lpvt_d815f2e1f682c86565c1063aafaef292=1685326309
# Pragma: no-cache
# Cache-Control: no-cache

# result
# {"code":0,"message":"ok","data":{"Next":"-1","Len":2,"IsFirst":true,"Expired":false,"InfoList":[{"FileId":2685677,"FileName":"requirements.txt","Type":0,"Size":148,"ContentType":"0","S3KeyFlag":"1815181524-0","CreateAt":"2023-05-22T16:23:38+08:00","UpdateAt":"2023-05-22T16:25:34+08:00","Etag":"34fa77af43679699096c7606a7f46050","DownloadUrl":"","Status":2,"ParentFileId":2678796,"Category":6,"PunishFlag":0,"StorageNode":"m2"},{"FileId":2679052,"FileName":"downloadFileList1815181524.txt","Type":0,"Size":269,"ContentType":"0","S3KeyFlag":"1815181524-0","CreateAt":"2023-05-19T23:14:25+08:00","UpdateAt":"2023-05-20T13:54:43+08:00","Etag":"84df2d1b3a154e534e33f9cdf48a3df9","DownloadUrl":"","Status":2,"ParentFileId":2678796,"Category":6,"PunishFlag":0,"StorageNode":"m2"}]}}
###########################################################
def get_g_initialProps_password(ShareKey,SharePwd): 
    """
    window.g_initialProps
    :param ShareKey:ShareKey
    :param SharePwd:SharePwd
    :return: {}
    info.data = {
        'ShareKey':ShareKey,  
        'FileID':info.get('FileId'), 
        'S3keyFlag':info.get('S3KeyFlag'), 
        'Size':info.get('Size'), 
        'Etag':info.get('Etag'), 
    }
    """
    url = 'https://www.123pan.com/b/api/share/get?limit=100&next=1&orderBy=share_id&orderDirection=desc&shareKey={}&SharePwd={}&ParentFileId=0&Page=1'
    url = url.format(ShareKey,SharePwd)
    Referer = 'https://www.123pan.com/s/' + ShareKey + '.html'
    headers = {
        'Connection': 'close',
        'referer': Referer,
        'user-agent': USER_AGENT
    }
    print('JSON::',url)
    #response = requests.get(url,headers=headers,allow_redirects=False)
    response = class_proxies.get_response(url,headers=headers,allow_redirects=False)
    res = response.json()
    return res
###########################################################
###########################################################
# GET https://www.123pan.com/s/MrBtVv-30xpA.html
# GET /s/MrBtVv-30xpA.html HTTP/1.1
# Host: www.123pan.com
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Connection: keep-alive
# Cookie: UM_distinctid=188462e8395414-01ffec5b65d7718-7f2c6753-13c680-188462e839668e; CNZZDATA1280304515=1889281670-1684804468-%7C1684804468; Hm_lvt_d815f2e1f682c86565c1063aafaef292=1684804643; Hm_lpvt_d815f2e1f682c86565c1063aafaef292=1684804643
# Upgrade-Insecure-Requests: 1
# Pragma: no-cache
# Cache-Control: no-cache

# result
# ...window.g_initialProps = {"res":{"code":0,"message":"ok","data":{"UserNickName":"13********5","UserID":1815181524,"ShareName":"requirements.t...等2个文件","HasPwd":false,"Expiration":"2099-12-12T08:00:00+08:00","CreateAt":"2023-05-22T16:25:14+08:00","Expired":false,"ShareKey":"MrBtVv-30xpA","HeadImage":"https:\u002F\u002Fstatics.123pan.com\u002Fstatic-by-custom\u002Fdefault_avatar.png","IsVip":false}},"reslist":{"code":0,"message":"ok","data":{"Next":"-1","Len":2,"IsFirst":true,"Expired":false,"InfoList":[{"FileId":2685677,"FileName":"requirements.txt","Type":0,"Size":148,"ContentType":"0","S3KeyFlag":"1815181524-0","CreateAt":"2023-05-22T16:23:38+08:00","UpdateAt":"2023-05-22T16:25:34+08:00","Etag":"34fa77af43679699096c7606a7f46050","DownloadUrl":"","Status":2,"ParentFileId":2678796,"Category":6,"PunishFlag":0,"StorageNode":"m2"},{"FileId":2679052,"FileName":"downloadFileList1815181524.txt","Type":0,"Size":269,"ContentType":"0","S3KeyFlag":"1815181524-0","CreateAt":"2023-05-19T23:14:25+08:00","UpdateAt":"2023-05-20T13:54:43+08:00","Etag":"84df2d1b3a154e534e33f9cdf48a3df9","DownloadUrl":"","Status":2,"ParentFileId":2678796,"Category":6,"PunishFlag":0,"StorageNode":"m2"}]}},"publicPath":"https:\u002F\u002Fwww.123pan.com\u002Fb\u002Fapi\u002F"};
###########################################################
def get_g_initialProps(ShareKey): 
    """
    window.g_initialProps
    :param ShareKey:ShareKey
    :return: {}
    res_json.get('reslist').get('data').get('InfoList')[].get('FileName')
    info.data = {
        'ShareKey':ShareKey,  
        'FileID':info.get('FileId'), 
        'S3keyFlag':info.get('S3KeyFlag'), 
        'Size':info.get('Size'), 
        'Etag':info.get('Etag'), 
    }
    """
    keyword = 'window.g_initialProps = '
    res = '{"code":-1,"message":"response error"}'
    url = 'https://www.123pan.com/s/' + ShareKey + '.html'
    headers = {
        'Connection': 'close',
        'user-agent': USER_AGENT
    }
    print('HTML::',url)
    #response = requests.get(url,headers=headers,allow_redirects=False)
    response = class_proxies.get_response(url,headers=headers,allow_redirects=False)
    # response = {"status_code":200,
    #             "text":'window.g_initialProps = {"res":{"code":0,"message":"ok","data":{"UserNickName":"13********5","UserID":1815181524,"ShareName":"01-The-Beatles...等3个文件","HasPwd":false,"Expiration":"2099-12-12T08:00:00+08:00","CreateAt":"2023-05-23T10:03:59+08:00","Expired":false,"ShareKey":"MrBtVv-w0xpA","HeadImage":"https:\u002F\u002Fstatics.123pan.com\u002Fstatic-by-custom\u002Fdefault_avatar.png","IsVip":false}},"reslist":{"code":0,"message":"ok","data":{"Next":"-1","Len":3,"IsFirst":true,"Expired":false,"InfoList":[{"FileId":2688790,"FileName":"01-The-Beatles-yesterday.zip","Type":0,"Size":2941909,"ContentType":"0","S3KeyFlag":"1815181524-0","CreateAt":"2023-05-23T10:03:46+08:00","UpdateAt":"2023-05-23T10:03:59+08:00","Etag":"bed028af2040ede661e5dbee392c7505","DownloadUrl":"","Status":5,"ParentFileId":2678796,"Category":10,"PunishFlag":0,"StorageNode":"m2"},{"FileId":2685677,"FileName":"requirements.txt","Type":0,"Size":148,"ContentType":"0","S3KeyFlag":"1815181524-0","CreateAt":"2023-05-22T16:23:38+08:00","UpdateAt":"2023-05-22T16:25:34+08:00","Etag":"34fa77af43679699096c7606a7f46050","DownloadUrl":"","Status":2,"ParentFileId":2678796,"Category":6,"PunishFlag":0,"StorageNode":"m2"},{"FileId":2679052,"FileName":"downloadFileList1815181524.txt","Type":0,"Size":269,"ContentType":"0","S3KeyFlag":"1815181524-0","CreateAt":"2023-05-19T23:14:25+08:00","UpdateAt":"2023-05-20T13:54:43+08:00","Etag":"84df2d1b3a154e534e33f9cdf48a3df9","DownloadUrl":"","Status":2,"ParentFileId":2678796,"Category":6,"PunishFlag":0,"StorageNode":"m2"}]}},"publicPath":"https:\u002F\u002Fwww.123pan.com\u002Fb\u002Fapi\u002F"};'
    #             }
    #print(response.reason,response.headers)
    if 'OK'==response.reason:
        html = str(response.content,encoding='utf-8')
        g_initialProps_start = html.find(keyword)
        if -1!=g_initialProps_start:
            temp = html[g_initialProps_start:]
            g_initialProps_end = temp.find(';')
            if -1!=g_initialProps_end:
                json_str = temp[len(keyword):g_initialProps_end]                
                #print('HTML::',json_str)
                g_initialProps = json.loads(json_str)
                res = g_initialProps.get('reslist')
                return res
            else:
                res['message'] = 'Not find ;'
        else:
            res['message'] = 'Not find window.g_initialProps'
    else:
        res['message'] = response.reason
    print('res::',res['message'],url)
    return res
###########################################################
# POST https://www.123pan.com/b/api/share/download/info

# POST
# {"ShareKey":"MrBtVv-30xpA","FileID":2685677,"S3keyFlag":"1815181524-0","Size":148,"Etag":"34fa77af43679699096c7606a7f46050"}

# 请求头
# POST /b/api/share/download/info HTTP/1.1
# Host: www.123pan.com
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: */*
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Content-Type: application/json;charset=UTF-8
# platform: web
# App-Version: 3
# Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODUzNDcyNzgsImlhdCI6MTY4NDc0MjQ3OCwiaWQiOjE4MTUxODE1MjQsIm5pY2tuYW1lIjoiMTM2MzkxMDk5NDUiLCJzdXBwZXIiOmZhbHNlLCJ1c2VybmFtZSI6MTM2MzkxMDk5NDUsInYiOjB9.1vJSM4pT6XuTG2LZD-iCipatdvAVmz5O_eD6i0GiyZU
# Content-Length: 124
# Origin: https://www.123pan.com
# Connection: keep-alive
# Referer: https://www.123pan.com/s/MrBtVv-30xpA.html
# Pragma: no-cache
# Cache-Control: no-cache

# Cookies = null

# result
# {'code': 400, 'message': 'ShareKey格式异常', 'data': None}
# {"code":0,"message":"success","data":{"DownloadURL":"https://web-pro2.cjjd18.com/download-v2/?params=aHR0cHM6Ly9kb3dubG9hZC1jZG4uMTIzcGFuLmNuLzEyMy04MC8zNGZhNzdhZi8xODE1MTgxNTI0LTAvMzRmYTc3YWY0MzY3OTY5OTA5NmM3NjA2YTdmNDYwNTAvYy1tMj92PTUmdD0xNjg0ODMwMzQ3JnM9MTY4NDgzMDM0NzQ3NDU3NDRmMjg3ZTI2ZDAzODA3NWZjNDQ4NzM0MTRlJnI9MENRTEw3JmZpbGVuYW1lPXJlcXVpcmVtZW50cy50eHQmeC1tZi1iaXotY2lkPWUzZjdhNjJmLTQ0ODQtNDk1ZS1hZWY5LTI3ZGNhMWFlNGEwMi02ZWFhNzcmYXV0b19yZWRpcmVjdD0w&is_s3=0"}}
###########################################################
def get_info(ShareKey,info,Referer):
    url = 'https://www.123pan.com/b/api/share/download/info'
    data = {
        'ShareKey':ShareKey,  
        'FileID':info.get('FileId'), 
        'S3keyFlag':info.get('S3KeyFlag'), 
        'Size':info.get('Size'), 
        'Etag':info.get('Etag'), 
    }            
    headers = {
        'Connection': 'close',
        'origin': 'https://www.123pan.com',
        'referer': Referer,
        'user-agent': USER_AGENT
    }

    #response = requests.post(url,data=data,headers=headers)
    response = class_proxies.post_response(url,headers=headers,data=data)
    res = response.json()
    return res
###########################################################
# base64_decode https://web-pro2.cjjd18.com/download-v2/?params=aHR0cHM6Ly9kb3dubG9hZC1jZG4uMTIzcGFuLmNuLzEyMy04MC8zNGZhNzdhZi8xODE1MTgxNTI0LTAvMzRmYTc3YWY0MzY3OTY5OTA5NmM3NjA2YTdmNDYwNTAvYy1tMj92PTUmdD0xNjg0ODMwMzQ3JnM9MTY4NDgzMDM0NzQ3NDU3NDRmMjg3ZTI2ZDAzODA3NWZjNDQ4NzM0MTRlJnI9MENRTEw3JmZpbGVuYW1lPXJlcXVpcmVtZW50cy50eHQmeC1tZi1iaXotY2lkPWUzZjdhNjJmLTQ0ODQtNDk1ZS1hZWY5LTI3ZGNhMWFlNGEwMi02ZWFhNzcmYXV0b19yZWRpcmVjdD0w&is_s3=0
# direct_json_url = base64.decodestring(b'aHR0cHM6Ly9kb3dubG9hZC1jZG4uMTIzcGFuLmNuLzEyMy04MC8zNGZhNzdhZi8xODE1MTgxNTI0LTAvMzRmYTc3YWY0MzY3OTY5OTA5NmM3NjA2YTdmNDYwNTAvYy1tMj92PTUmdD0xNjg0ODMwMzQ3JnM9MTY4NDgzMDM0NzQ3NDU3NDRmMjg3ZTI2ZDAzODA3NWZjNDQ4NzM0MTRlJnI9MENRTEw3JmZpbGVuYW1lPXJlcXVpcmVtZW50cy50eHQmeC1tZi1iaXotY2lkPWUzZjdhNjJmLTQ0ODQtNDk1ZS1hZWY5LTI3ZGNhMWFlNGEwMi02ZWFhNzcmYXV0b19yZWRpcmVjdD0w')
# result https://download-cdn.123pan.cn/123-80/34fa77af/1815181524-0/34fa77af43679699096c7606a7f46050/c-m2?v=5&t=1684830347&s=16848303474745744f287e26d038075fc44873414e&r=0CQLL7&filename=requirements.txt&x-mf-biz-cid=e3f7a62f-4484-495e-aef9-27dca1ae4a02-6eaa77&auto_redirect=0
###########################################################
# GET https://download-cdn.123pan.cn/123-80/34fa77af/1815181524-0/34fa77af43679699096c7606a7f46050/c-m2?v=5&t=1684830347&s=16848303474745744f287e26d038075fc44873414e&r=0CQLL7&filename=requirements.txt&x-mf-biz-cid=e3f7a62f-4484-495e-aef9-27dca1ae4a02-6eaa77&auto_redirect=0
# 请求头
# GET /123-80/34fa77af/1815181524-0/34fa77af43679699096c7606a7f46050/c-m2?v=5&t=1684973261&s=1684973261f42a3ccbd28548ce183b51d71ebfb145&r=SOQXG4&filename=requirements.txt&x-mf-biz-cid=dfa3aa54-e8bb-4a80-9964-d1bd37360cd1-6eaa77&auto_redirect=0 HTTP/1.1
# Host: download-cdn.123pan.cn
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: */*
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Origin: https://web-pro2.cjjd18.com
# Connection: keep-alive
# Referer: https://web-pro2.cjjd18.com/download-v2/?params=aHR0cHM6Ly9kb3dubG9hZC1jZG4uMTIzcGFuLmNuLzEyMy04MC8zNGZhNzdhZi8xODE1MTgxNTI0LTAvMzRmYTc3YWY0MzY3OTY5OTA5NmM3NjA2YTdmNDYwNTAvYy1tMj92PTUmdD0xNjg0OTczMjYxJnM9MTY4NDk3MzI2MWY0MmEzY2NiZDI4NTQ4Y2UxODNiNTFkNzFlYmZiMTQ1JnI9U09RWEc0JmZpbGVuYW1lPXJlcXVpcmVtZW50cy50eHQmeC1tZi1iaXotY2lkPWRmYTNhYTU0LWU4YmItNGE4MC05OTY0LWQxYmQzNzM2MGNkMS02ZWFhNzcmYXV0b19yZWRpcmVjdD0w&is_s3=0
# Pragma: no-cache
# Cache-Control: no-cache

# result
# {"message":"ok","data":{"redirect_url":"https://223-95-79-65.d.cjjd15.com:30443/download-cdn.123pan.cn/123-80/34fa77af/1815181524-0/34fa77af43679699096c7606a7f46050/c-m2?v=5&t=1684830347&s=16848303474745744f287e26d038075fc44873414e&r=0CQLL7&filename=requirements.txt&x-mf-biz-cid=e3f7a62f-4484-495e-aef9-27dca1ae4a02-6eaa77&auto_redirect=0&xmfcid=b94ced9b-f097-409f-9979-915339b5c440-50111d3b1-9758-98"},"code":0}
###########################################################
def get_redirect_url(url,Referer): 
    p = parse.urlparse(Referer)
    Origin = p.scheme + '://' + p.netloc
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        #"Accept-Encoding": "gzip, deflate, br",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        #'Host':'download-cdn.123pan.cn',
        'Origin': Origin,
        'Connection': 'close',
        'Referer': Referer,
        'User-Agent': USER_AGENT
    }
    #response = requests.get(url,headers=headers,allow_redirects=False)
    response = class_proxies.get_response(url,headers=headers,allow_redirects=False)

    if 'OK'==response.reason:
        html = response.content
        return json.loads(html)
    elif 'Moved Temporarily'==response.reason:
        resUrl = response.headers.get('Location')
        res = {"message":"ok","data":{"redirect_url":resUrl},"code":0}
        return res
    else:
        print('get_redirect_url::',response.reason,response.content[0:200],url)
        return {"message":  response.reason }
###########################################################
###########################################################
# GET https://111-40-113-9.d.cjjd15.com:30443/download-cdn.123pan.cn/123-80/34fa77af/1815181524-0/34fa77af43679699096c7606a7f46050/c-m2?v=5&t=1684973261&s=1684973261f42a3ccbd28548ce183b51d71ebfb145&r=SOQXG4&filename=requirements.txt&x-mf-biz-cid=dfa3aa54-e8bb-4a80-9964-d1bd37360cd1-6eaa77&auto_redirect=0&xmfcid=36161c8e-8e24-494b-b6db-3d15f5cd8147-cd8a62355-6450-65
# 请求头
# 1 OPTIONS /download-cdn.123pan.cn/123-80/34fa77af/1815181524-0/34fa77af43679699096c7606a7f46050/c-m2?v=5&t=1684973261&s=1684973261f42a3ccbd28548ce183b51d71ebfb145&r=SOQXG4&filename=requirements.txt&x-mf-biz-cid=dfa3aa54-e8bb-4a80-9964-d1bd37360cd1-6eaa77&auto_redirect=0&xmfcid=36161c8e-8e24-494b-b6db-3d15f5cd8147-cd8a62355-6450-65 HTTP/1.1
# Host: 111-40-113-9.d.cjjd15.com:30443
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: */*
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Access-Control-Request-Method: GET
# Access-Control-Request-Headers: action,range
# Referer: https://web-pro2.cjjd18.com/download-v2/?params=aHR0cHM6Ly9kb3dubG9hZC1jZG4uMTIzcGFuLmNuLzEyMy04MC8zNGZhNzdhZi8xODE1MTgxNTI0LTAvMzRmYTc3YWY0MzY3OTY5OTA5NmM3NjA2YTdmNDYwNTAvYy1tMj92PTUmdD0xNjg0OTczMjYxJnM9MTY4NDk3MzI2MWY0MmEzY2NiZDI4NTQ4Y2UxODNiNTFkNzFlYmZiMTQ1JnI9U09RWEc0JmZpbGVuYW1lPXJlcXVpcmVtZW50cy50eHQmeC1tZi1iaXotY2lkPWRmYTNhYTU0LWU4YmItNGE4MC05OTY0LWQxYmQzNzM2MGNkMS02ZWFhNzcmYXV0b19yZWRpcmVjdD0w&is_s3=0
# Origin: https://web-pro2.cjjd18.com
# Connection: keep-alive
# Pragma: no-cache
# Cache-Control: no-cache

# 2 GET /download-cdn.123pan.cn/123-80/34fa77af/1815181524-0/34fa77af43679699096c7606a7f46050/c-m2?v=5&t=1684973261&s=1684973261f42a3ccbd28548ce183b51d71ebfb145&r=SOQXG4&filename=requirements.txt&x-mf-biz-cid=dfa3aa54-e8bb-4a80-9964-d1bd37360cd1-6eaa77&auto_redirect=0&xmfcid=36161c8e-8e24-494b-b6db-3d15f5cd8147-cd8a62355-6450-65 HTTP/1.1
# Host: 111-40-113-9.d.cjjd15.com:30443
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: */*
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Range: bytes=0-0
# Action: pre
# Origin: https://web-pro2.cjjd18.com
# Connection: keep-alive
# Referer: https://web-pro2.cjjd18.com/download-v2/?params=aHR0cHM6Ly9kb3dubG9hZC1jZG4uMTIzcGFuLmNuLzEyMy04MC8zNGZhNzdhZi8xODE1MTgxNTI0LTAvMzRmYTc3YWY0MzY3OTY5OTA5NmM3NjA2YTdmNDYwNTAvYy1tMj92PTUmdD0xNjg0OTczMjYxJnM9MTY4NDk3MzI2MWY0MmEzY2NiZDI4NTQ4Y2UxODNiNTFkNzFlYmZiMTQ1JnI9U09RWEc0JmZpbGVuYW1lPXJlcXVpcmVtZW50cy50eHQmeC1tZi1iaXotY2lkPWRmYTNhYTU0LWU4YmItNGE4MC05OTY0LWQxYmQzNzM2MGNkMS02ZWFhNzcmYXV0b19yZWRpcmVjdD0w&is_s3=0
# Pragma: no-cache
# Cache-Control: no-cache

# real download
# 3 GET /download-cdn.123pan.cn/123-80/34fa77af/1815181524-0/34fa77af43679699096c7606a7f46050/c-m2?v=5&t=1684973261&s=1684973261f42a3ccbd28548ce183b51d71ebfb145&r=SOQXG4&filename=requirements.txt&x-mf-biz-cid=dfa3aa54-e8bb-4a80-9964-d1bd37360cd1-6eaa77&auto_redirect=0&xmfcid=36161c8e-8e24-494b-b6db-3d15f5cd8147-cd8a62355-6450-65 HTTP/1.1
# Host: 111-40-113-9.d.cjjd15.com:30443
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Connection: keep-alive
# Upgrade-Insecure-Requests: 1
# Pragma: no-cache
# Cache-Control: no-cache
###########################################################
def download(url,Referer): 
    p = parse.urlparse(Referer)
    Origin = p.scheme + '://' + p.netloc
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        #"Accept-Encoding": "gzip, deflate, br",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        #'Host':'download-cdn.123pan.cn',
        'Origin': Origin,
        'Connection': 'close',
        #'Connection': 'keep-alive',
        'Referer': Referer,
        'User-Agent': USER_AGENT
    }
    print('download:',url[0:130])
    #response = requests.get(url,headers=headers,allow_redirects=True)
    response = class_proxies.get_response(url,headers=headers,allow_redirects=True,timeout=300)
    #html = response.__dict__
    #print(response.reason,response.content)
    #print(response.headers.get('Content-Type'),response.headers.get('Content-disposition'))
    #if 'binary/octet-stream'==headers.get('Content-Type'):
    if 'OK'==response.reason:
        file_obj = open("cache.zip", 'wb')
        file_obj.write(response.content)
        file_obj.close()
        del response
        #print(gc.collect())
        return True
    else:
        print('download::error',response.reason)
        return False
###########################################################
def unzip_cache(folder,filename,mainfolder=MP3_ROOT): 
    """
    unzip or copy jpg to floder
    :param path:
    :return:
    """
    src_path = 'cache.zip'
    dest_folder = mainfolder + '/' + folder
    if not os.path.exists(dest_folder):
        print('unzip:mkdir::',dest_folder)
        os.mkdir(dest_folder)
    if folder==IMG_FLODER:
        dest_path = dest_folder + '/' + filename
        os.rename(src_path,dest_path)
        print('unzip:rename cache.zip to img/*.jpg ok',folder,dest_path) 
        return True
    r = zipfile.is_zipfile(src_path)
    if r:     
        zipFile = zipfile.ZipFile(src_path, 'r')
        for file in zipFile.namelist():
            zipFile.extract(file, dest_folder)
            print('unzip:ok',folder,file) 
        zipFile.close()
        return True
    else:
        print('This is not zip')
        return False
###########################################################
def zip_file(src_path): 
    """
    zip to file
    :param path:
    :return:
    """
    dest_path = src_path[0:-4] + '.zip'
    name_split = str.split(src_path,'/')
    arcname = name_split[len(name_split)-1]
    print(name_split,arcname)
    zipFile = zipfile.ZipFile(dest_path, 'w')
    zipFile.write(src_path,arcname)
    zipFile.close()
    print('zip:ok',dest_path) 
###########################################################
def file_in_floder(filename,folder,mainfolder=MP3_ROOT): 
    """
    判断zip文件内mp3是否下载并解压到相应文件夹下
    :param path:
    :return:
    """
    mp3_path = mainfolder + '/' + folder + '/' +filename[0:-4] + '.mp3'
    if os.path.exists(mp3_path):
        return True
    mp3_path = mainfolder + '/' + folder + '/' +filename[0:-4] + '.m4a'
    if os.path.exists(mp3_path):
        return True
    mp3_path = mainfolder + '/' + folder + '/' +filename[0:-4] + '.aac'
    if os.path.exists(mp3_path):
        return True
    return False
###########################################################
def trim_str_by_start_end(text,str_s,str_e): 
    """
    获取text下中起始之间的内容，不包含str_s,str_e
    :param path:
    :return:
    """
    start = text.find(str_s)
    if -1!=start:
        temp = text[start:]
        end = temp.find(str_e)
        if -1!=end:
            ret_str = temp[len(str_s):end]
            return ret_str
    return None
###########################################################
def remove_by_floder(floder): 
    """
    export::
    删除所有文件，文件夹
    :param floder:
    :return:total_remove
    """
    if len(floder)==0:
        print('Remove::floder name is null',floder)
        return
    folder_path = MP3_ROOT + '/' + floder
    for file_name in os.listdir(folder_path):
        file_path = folder_path + '/' + file_name
        print('Remove::',file_path)
        os.remove(file_path)
    os.rmdir(folder_path)
###########################################################
def cmd_mem(  ):
    mem_r = 2**20
    mem = psutil.virtual_memory()
    print('Memory percent:',mem.percent,'total:',mem.total//mem_r,'available:',mem.available//mem_r,'used:',mem.used//mem_r,'free:',mem.free//mem_r)
    return True
###########################################################
def download_by_ShareKey(MAX_DOWNLOAD,ShareKey,SharePwd,floder,sleep=120): 
    """
    export::
    下载无提取码的123网盘分享页面的所有文件
    :param ShareKey:
    :return:total_download
    """
    total_download = 0
    class_proxies.best_proxies()
    if not os.path.exists(MP3_ROOT):
        print('download_by_ShareKey:mkdir::',MP3_ROOT)
        os.mkdir(MP3_ROOT)
    url = 'https://www.123pan.com/s/' + ShareKey + '.html'
    if SharePwd:
        res_json = get_g_initialProps_password(ShareKey,SharePwd)
    else:
        res_json = get_g_initialProps(ShareKey)
    if 0==res_json.get('code'):
        InfoList = res_json.get('data').get('InfoList')
        len_Info = len(InfoList)
        for info in InfoList:
            cmd_mem()
            if total_download > MAX_DOWNLOAD:
                print('gc.collect()',gc.collect())
                print('total_download > MAX_DOWNLOAD',total_download)
                return total_download
            if not class_variable.get_download_enable():
                print('gc.collect()',gc.collect())
                print('Download disabled, please set enable',total_download)
                return total_download
            filename = info.get('FileName')
            print(total_download,'/',len_Info,ShareKey, floder, filename)
            if 'zip'!=filename[-3:len(filename)]:
                if 'jpg'!=filename[-3:len(filename)]:
                    continue
            if file_in_floder(filename,floder):
                continue
            info_json = get_info(ShareKey,info,url)
            if 0==info_json.get('code'):
                time.sleep(2+int(random.random()*3))
                DownloadURL = info_json.get('data').get('DownloadURL')
                #DownloadURL = 'https://web-pro2.cjjd18.com/download-v2/?params=aHR0cHM6Ly9kb3dubG9hZC1jZG4uMTIzcGFuLmNuLzEyMy04MC8zNGZhNzdhZi8xODE1MTgxNTI0LTAvMzRmYTc3YWY0MzY3OTY5OTA5NmM3NjA2YTdmNDYwNTAvYy1tMj92PTUmdD0xNjg0OTE4NjkzJnM9MTY4NDkxODY5M2M3YzAwOGIzNTJkYjAxNjgyZjU2NzA1NzQxYzFkODc2JnI9NFdXWDdMJmZpbGVuYW1lPXJlcXVpcmVtZW50cy50eHQmeC1tZi1iaXotY2lkPWQ0YmIxZWVlLWE0MDYtNDI5Yi1hYTNiLWVjNzg1MmJmNDllNS01ODQwMDAmYXV0b19yZWRpcmVjdD0w&is_s3=0'
                #DownloadURL = 'https://web-pro2.cjjd18.com/download-v2/?params=aHR0cHM6Ly9kb3dubG9hZC1jZG4uMTIzcGFuLmNuLzEyMy04MC8zNGZhNzdhZi8xODE1MTgxNTI0LTAvMzRmYTc3YWY0MzY3OTY5OTA5NmM3NjA2YTdmNDYwNTAvYy1tMj92PTUmdD0xNjg0OTczMjYxJnM9MTY4NDk3MzI2MWY0MmEzY2NiZDI4NTQ4Y2UxODNiNTFkNzFlYmZiMTQ1JnI9U09RWEc0JmZpbGVuYW1lPXJlcXVpcmVtZW50cy50eHQmeC1tZi1iaXotY2lkPWRmYTNhYTU0LWU4YmItNGE4MC05OTY0LWQxYmQzNzM2MGNkMS02ZWFhNzcmYXV0b19yZWRpcmVjdD0w&is_s3=0'
                params = trim_str_by_start_end(DownloadURL,'?params=','&')
                params_bytes = bytes(params, encoding='utf-8')
                #print(type(params_bytes),params_bytes)
                decode_url = base64.b64decode(params_bytes)
                #print(decode_url)
                time.sleep(2+int(random.random()*3))
                redirect_url_json = get_redirect_url(decode_url,DownloadURL)
                if 'ok'==redirect_url_json.get('message'):
                    download_url = redirect_url_json.get('data').get('redirect_url')
                    time.sleep(2+int(random.random()*3))
                    isok = download(download_url,DownloadURL)
                    if isok:
                        unzip_cache(floder,filename)
                        total_download += 1
                else:
                    print('redirect_url_json:',redirect_url_json)
            else:
                print("info_json:",info_json)
            time.sleep(10+sleep+int(random.random()*10))
            class_proxies.best_proxies()
    else:
        print('download_by_ShareKey::res_json:',res_json)
    print('gc.collect()',gc.collect())
    print('download_by_ShareKey ok::',ShareKey,total_download)
    return total_download


if __name__ == '__main__':
    ss = '01-The-Beatles-yesterday.zip'
    # print(ss[-3:len(ss)])
    # print(ss[0:-4])
    #unzip_cache('img','filename.jpg')
    print(int(random.random()*10))
    ShareKey = 'MrBtVv-w0xpA'
    #download_by_ShareKey(ShareKey,None,'temp')
    ShareKey = 'MrBtVv-SUxpA'
    # res_json = get_g_initialProps_password(ShareKey,'9945')
    # print(res_json)
    #zip_file('mp3/01-The-Beatles-yesterday.mp3')
    # print(file_in_floder(ss,ShareKey))
    # remove_by_ShareKey(ShareKey)
    #print(s.encode('utf-8'))
    download_by_ShareKey(ShareKey,'9945','temp')