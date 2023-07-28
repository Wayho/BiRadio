# coding=utf-8
import leancloud							#requirements leancloud-sdk>=1.0.9,<=2.0.0
import os

# https://u6.y.qq.com/cgi-bin/musics.fcg?_webcgikey=get_song_detail&_=1690507656282&sign=zzbd9393c9accbpjoarbiak0joh0tzwpg02b0406e
# {"code":0,"ts":1690507656513,"start_ts":1690507656482,"traceid":"2dded9f0486c4a72","req_0":{"code":0,"data":{"track_info":{"id":13795,"type":0,"mid":"004WVo0X2RJEaj","name":"Baby对不起","title":"Baby对不起","subtitle":"","singer":[{"id":260,"mid":"003gNFzb0MYOnM","name":"CoCo李玟","title":"CoCo李玟","type":1,"uin":0}],"album":{"id":1093,"mid":"000NdddH2RnGI5","name":"Promise","title":"Promise","subtitle":"","time_public":"2001-10-13","pmid":"000NdddH2RnGI5_1"},"mv":{"id":530233,"vid":"r0022xw508c","name":"","title":"","vt":0},"interval":215,"isonly":0,"language":0,"genre":1,"index_cd":0,"index_album":3,"time_public":"2001-10-13","status":0,"fnote":4009,"file":{"media_mid":"002AUqT84YqfGG","size_24aac":0,"size_48aac":1309959,"size_96aac":2626210,"size_192ogg":5156859,"size_192aac":5218024,"size_128mp3":3452140,"size_320mp3":8630028,"size_ape":0,"size_flac":44303391,"size_dts":0,"size_try":960887,"try_begin":53240,"try_end":79496,"url":"","size_hires":0,"hires_sample":0,"hires_bitdepth":0,"b_30s":0,"e_30s":60000,"size_96ogg":2565581,"size_360ra":[],"size_dolby":0,"size_new":[158860006,25273879,63627212,8822947,0]},"pay":{"pay_month":1,"price_track":200,"price_album":0,"pay_play":1,"pay_down":1,"pay_status":0,"time_free":0},"action":{"switch":16897281,"msgid":13,"alert":41,"icons":12992510,"msgshare":0,"msgfav":0,"msgdown":0,"msgpay":6,"switch2":0,"icon2":0},"ksong":{"id":43922,"mid":"002hJWtF18YxZp"},"volume":{"gain":-6.832,"peak":0.861,"lra":5.81},"label":"0","url":"","bpm":0,"version":0,"trace":"","data_type":0,"modify_stamp":0,"pingpong":"","ppurl":"","tid":0,"ov":0,"sa":17408,"es":"","vs":["061EVZQl1lERuU","","","003zR4l60Ek0pJ","001KaBnz0iQfcW","",""],"vi":[5]},"info":[{"title":"演唱者","type":"JUMP_TO_SINGER","content":[{"id":260,"value":"CoCo李玟","mid":"003gNFzb0MYOnM","type":0,"show_type":0,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":0,"more":0,"selected":"singer","use_platform":2},{"title":"作词","type":"lyricist","content":[{"id":0,"value":"李玟 / 楼南蔚","mid":"","type":0,"show_type":0,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":8,"more":0,"selected":"","use_platform":0},{"title":"作曲","type":"JUMP_TO_SINGER","content":[{"id":948384,"value":"Omar Alfanno","mid":"003hM0wc3Ac8eL","type":0,"show_type":0,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":8,"more":0,"selected":"","use_platform":0},{"title":"歌曲语种","type":"JUMP_TO_CATEGORY","content":[{"id":1,"value":"国语","mid":"","type":0,"show_type":2,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":11,"more":0,"selected":"lan","use_platform":3},{"title":"歌曲流派","type":"JUMP_TO_CATEGORY","content":[{"id":40,"value":"Pop","mid":"","type":0,"show_type":2,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":12,"more":0,"selected":"genre","use_platform":3},{"title":"唱片公司","type":"JUMP_TO_COMPANY","content":[{"id":5,"value":"索尼音乐","mid":"","type":0,"show_type":0,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":51,"more":0,"selected":"company","use_platform":1},{"title":"延展阅读","type":"MP_ARTICLE","content":[],"pos":99,"more":0,"selected":"","use_platform":0},{"title":"歌词","type":"lyric","content":[{"id":0,"value":"[ti:Baby对不起]\n[ar:李玟]\n[al:Promise]\n[by:]\n[offset:0]\n[00:00.00]Baby对不起 - CoCo李玟 (CoCo Lee)\n[00:04.42]词：李玟/楼南蔚\n[00:08.84]曲：Omar Alfanno\n[00:13.27]听到我的电话 响了一声就暂停\n[00:16.99]会不会是你 我总怀疑\n[00:20.22]因为这原因 心情不稳定\n[00:23.84]\n[00:26.22]我们之间的问题 是我不相信你\n[00:29.89]敏感又多心 怕你变了心\n[00:33.12]因为爱你 害怕失去你\n[00:36.71]\n[00:38.40]爱的天气 总是阴晴不定\n[00:43.79]\n[00:44.88]爱的情绪 也在欢笑中哭泣\n[00:50.42]\n[00:52.43]Baby\n[00:53.62]想对你说声对不起\n[00:56.19]\n[00:56.82]用错了方式去爱你\n[00:59.47]\n[01:00.11]因为我太在意\n[01:04.56]如果没有你\n[01:06.31]我的世界只剩回忆\n[01:09.26]\n[01:09.77]每天只面对孤寂\n[01:13.27]已来不及 再说我爱你\n[01:18.91]\n[01:31.23]自从那天分手后\n[01:32.95]停不住泪滴 想念一个人\n[01:36.40]忘记自己 让我爱你\n[01:39.61]什么都愿意\n[01:41.68]\n[01:43.22]爱的天气总是阴晴不定\n[01:48.71]\n[01:49.75]爱的情绪也在欢笑中哭泣\n[01:55.29]Baby\n[01:56.60]\n[01:57.22]Baby\n[01:58.54]想对你说声对不起\n[02:01.01]\n[02:01.62]用错了方式去爱你\n[02:04.52]\n[02:05.08]因为我太在意\n[02:09.48]如果没有你\n[02:11.20]我的世界只剩回忆\n[02:14.63]每天只面对孤寂\n[02:17.59]\n[02:18.15]已来不及 再说我爱你\n[02:24.99]\n[02:36.17]Baby\n[02:37.43]想对你说声对不起\n[02:40.10]\n[02:40.63]用错了方式去爱你\n[02:43.56]\n[02:44.07]因为我太在意\n[02:47.63]\n[02:48.35]如果没有你\n[02:50.20]我的世界只剩回忆\n[02:53.52]每天只面对孤寂 已来不及\n[02:59.32]\n[03:00.16]再说我爱你\n[03:04.83]\n[03:14.90]如果能再遇见你 把你抱紧\n[03:18.55]从此不分离\n[03:20.06]绝不放弃 我要告诉你\n[03:23.27]\n[03:24.06]Baby I&apos;m sorry","mid":"","type":0,"show_type":0,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":100,"more":0,"selected":"","use_platform":0}],"extras":{"name":"Baby对不起","transname":"","subtitle":"","from":"","wikiurl":""}}}}
# {"code":0,"ts":1690510924954,"start_ts":1690510924922,"traceid":"7c99c5110b5e4b1a","req_0":{"code":0,"data":{"track_info":{"id":102182656,"type":0,"mid":"003XQm272rwG7Z","name":"想你的365天","title":"想你的365天","subtitle":"","singer":[{"id":260,"mid":"003gNFzb0MYOnM","name":"CoCo李玟","title":"CoCo李玟","type":1,"uin":0}],"album":{"id":1103,"mid":"003fHjgK3Ts4J4","name":"碰碰看爱情","title":"碰碰看爱情","subtitle":"","time_public":"1998-08-14","pmid":"003fHjgK3Ts4J4_2"},"mv":{"id":530250,"vid":"r0022g43402","name":"","title":"","vt":0},"interval":330,"isonly":0,"language":0,"genre":1,"index_cd":0,"index_album":3,"time_public":"1998-08-14","status":0,"fnote":4009,"file":{"media_mid":"00104ECe47Zh4z","size_24aac":0,"size_48aac":2016314,"size_96aac":4048615,"size_192ogg":7950551,"size_192aac":7981989,"size_128mp3":5291993,"size_320mp3":13229665,"size_ape":0,"size_flac":36370776,"size_dts":0,"size_try":960887,"try_begin":79702,"try_end":114531,"url":"","size_hires":0,"hires_sample":0,"hires_bitdepth":0,"b_30s":0,"e_30s":60000,"size_96ogg":3939750,"size_360ra":[],"size_dolby":0,"size_new":[235051273,35563972,90740792,13666390,0]},"pay":{"pay_month":1,"price_track":200,"price_album":0,"pay_play":0,"pay_down":1,"pay_status":0,"time_free":0},"action":{"switch":16889603,"msgid":14,"alert":2,"icons":8527740,"msgshare":0,"msgfav":0,"msgdown":0,"msgpay":6,"switch2":393216,"icon2":0},"ksong":{"id":116153,"mid":"003v7SLK1iv101"},"volume":{"gain":-7.404,"peak":0.971,"lra":8.142},"label":"0","url":"","bpm":0,"version":0,"trace":"","data_type":0,"modify_stamp":0,"pingpong":"","ppurl":"","tid":0,"ov":0,"sa":17408,"es":"","vs":["061ayhqA2BDOWn","","","001Q4e0L1QJlEi","002vlgBF27Ci8i","",""],"vi":[5]},"info":[{"title":"演唱者","type":"JUMP_TO_SINGER","content":[{"id":260,"value":"CoCo李玟","mid":"003gNFzb0MYOnM","type":0,"show_type":0,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":0,"more":0,"selected":"singer","use_platform":2},{"title":"作词","type":"lyricist","content":[{"id":3173859,"value":"邬裕康","mid":"","type":0,"show_type":0,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":8,"more":0,"selected":"","use_platform":0},{"title":"作曲","type":"JUMP_TO_SINGER","content":[{"id":14764,"value":"李伟菘","mid":"001Taer33QjYU1","type":0,"show_type":0,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":8,"more":0,"selected":"","use_platform":0},{"title":"编曲","type":"arrangement","content":[{"id":0,"value":"鲍比达","mid":"","type":0,"show_type":0,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":9,"more":0,"selected":"","use_platform":0},{"title":"歌曲语种","type":"JUMP_TO_CATEGORY","content":[{"id":1,"value":"国语","mid":"","type":0,"show_type":2,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":11,"more":0,"selected":"lan","use_platform":3},{"title":"歌曲流派","type":"JUMP_TO_CATEGORY","content":[{"id":40,"value":"Pop","mid":"","type":0,"show_type":2,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":12,"more":0,"selected":"genre","use_platform":3},{"title":"唱片公司","type":"JUMP_TO_COMPANY","content":[{"id":5,"value":"索尼音乐","mid":"","type":0,"show_type":0,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":51,"more":0,"selected":"company","use_platform":1},{"title":"延展阅读","type":"MP_ARTICLE","content":[],"pos":99,"more":0,"selected":"","use_platform":0},{"title":"歌词","type":"lyric","content":[{"id":0,"value":"[ti:想你的365天]\n[ar:CoCo李玟]\n[al:碰碰看爱情]\n[by:]\n[offset:0]\n[00:00.00]想你的365天 - CoCo李玟 (CoCo Lee)\n[00:10.84]词：邬裕康\n[00:21.69]曲：李伟菘\n[00:32.53]编曲：鲍比达\n[00:43.38]春风扬起你我的离别\n[00:51.30]\n[00:52.22]夏雨打湿孤单的屋檐\n[01:00.64]\n[01:01.53]秋叶飘落思念的红叶\n[01:09.30]\n[01:10.74]冬雪转眼又是一年\n[01:18.69]\n[01:19.86]在想你的三百六十五天\n[01:27.47]\n[01:29.06]听你我最爱的那首歌\n[01:35.27]\n[01:38.21]泪总是一不小心翻涌微笑的脸\n[01:46.73]\n[01:48.49]突然我感觉你没走远\n[01:55.46]\n[02:34.21]怀里有你紧拥的温度\n[02:39.85]\n[02:43.08]眼里有你微笑和痛哭\n[02:48.91]\n[02:51.71]心里有你说过的故事\n[02:57.81]\n[03:00.59]梦里你在回家的路\n[03:06.66]\n[03:09.65]在想你的三百六十五天\n[03:16.18]\n[03:18.41]读你写来的每句安慰\n[03:24.44]\n[03:27.27]爱圈住你我在同一个圆\n[03:34.95]\n[03:37.36]你的冷热我能感觉\n[03:45.16]在想你的三百六十五天\n[03:51.62]\n[03:53.86]海我多想能看得更远\n[04:00.05]\n[04:02.77]爱两颗心间不断的长线\n[04:10.49]\n[04:12.80]我的喜悲都让你包围\n[04:18.50]\n[04:25.14]怀里有你紧拥的温度\n[04:30.74]\n[04:33.92]眼里有你微笑和痛哭\n[04:41.22]\n[04:42.78]心里有你说过的故事\n[04:48.77]\n[04:51.62]梦里你在回家的路\n[04:57.71]\n[05:00.44]梦里你在回家的路","mid":"","type":0,"show_type":0,"is_parent":0,"picurl":"","read_cnt":0,"author":"","jumpurl":"","ori_picurl":""}],"pos":100,"more":0,"selected":"","use_platform":0}],"extras":{"name":"想你的365天","transname":"","subtitle":"","from":"","wikiurl":""}}}}
SUBTITLE_PATH = 'srt/coco'

DB_NAME = 'subtitle'
print('class_subtitle v5.2.2:',DB_NAME)
def update_subtitle_file(name):
     # name:无扩展名 include 192k-CoCo-
    # return subtitle object
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.equal_to('on', True)
    query.equal_to('name', name)        # include 192k-CoCo-
    find = query.find()
    if find:
        check_path()
        lyric =  find[0].get('lyric')
        lyric = trim_apos(lyric)
        lyric = repalc_n_str(lyric)
        srt_file = open(os.path.join(SUBTITLE_PATH, name+'.srt'), 'w')
        srt_file.write(lyric)
        srt_file.close()
        return True
    return False

def get_subtitle(name):
    # return subtitle object
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.equal_to('on', True)
    query.equal_to('name', name)
    find = query.find()
    if find:
        return find[0]
    return None

def check_path():
    if not os.path.exists(SUBTITLE_PATH):
        print('class_subtitle:mkdir::',SUBTITLE_PATH)
        os.mkdir(SUBTITLE_PATH)

def trim_apos(text):
    for i in range(0,9):
        text = text.replace('&apos;','\'')
    text = text + '\r\n'
    return text

def repalc_n_str(text):
    text_list = text.split('\\n')
    text_list.append("\r\n")
    print(text_list)
    return '\r\n'.join(text_list)

if __name__ == '__main__':
    update_subtitle_file('192k-CoCo-想你的365天')
        