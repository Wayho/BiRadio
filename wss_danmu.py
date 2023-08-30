# -*- coding: utf-8 -*-
import asyncio
import random
import time
import blivedm
import os
import random
from queue import Queue
import class_viewer as class_viewer
import danmu as danmu
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
    WIDGET_GIFT_STAR_PROCESS = 8    # 礼物星球

ROOM_IDS = [
    30356247,
    30338274,
    27791346
]

TEXT_THANKS_GIFTNAME_AT_UNAME = '谢谢你的{}@{}'

#cmd=LIKE_INFO_V3_NOTICE, command={'cmd': 'LIKE_INFO_V3_NOTICE', 'data': {'content_segments': [{'font_color': '#F494AF', 'text': '本场点赞已累计500，快去号召直播间用户继续为你助力吧~', 'type': 1}], 'danmaku_style': {'background_color': None}, 'terminals': [2, 5]}, 'is_report': False, 'msg_id': '2124967025070080', 'send_time': 1692606932950}
#cmd=LIKE_INFO_V3_UPDATE, command={'cmd': 'LIKE_INFO_V3_UPDATE', 'data': {'click_count': 504}, 'is_report': False, 'msg_id': '2124967049188354', 'send_time': 1692606932996}
# [9453708] 醒目留言 ¥30 樱花色零奈：SuperChatMessage(price=30, message='喊那么大声想吓死谁？我七夕有高额存款陪有问题吗？没问题行不行', message_trans='そんなに大声で叫んで誰を怖がらせたいのですか。私は七夕に高額な預金がありますが、問題がありますか。大丈夫ですか', start_time=1692608460, end_time=1692608520, time=59, id=7861813, gift_id=12000, gift_name='醒目留言', uid=669791412, uname='樱花色零奈', face='https://i0.hdslb.com/bfs/face/ce0a8d39eef5cb64d46bd191fb8cb9e8132a6efe.jpg', guard_level=3, user_level=10, background_bottom_color='#2A60B2', background_color='#EDF5FF', background_icon='', background_image='', background_price_color='#7497CD')
#购买GuardBuyMessage(uid=2032937960, username='超级无敌顶级甜妹里里', guard_level=2, num=1, price=1998000, gift_id=10002, gift_name='提督', start_time=1692666308, end_time=1692666308)
#购买GuardBuyMessage(uid=279648384, username='冰碗冷面', guard_level=3, num=1, price=198000, gift_id=10003, gift_name='舰长', start_time=1692674539, end_time=1692674539)


#room=30338274 unknown cmd=WIDGET_GIFT_STAR_PROCESS, command={'cmd': 'WIDGET_GIFT_STAR_PROCESS', 'data': {'ddl_timestamp': 1692547200, 'finished': False, 'process_list': [{'completed_num': 15, 'gift_id': 31036, 'gift_img': 'https://s1.hdslb.com/bfs/live/8b40d0470890e7d573995383af8a8ae074d485d9.png', 'gift_name': '礼物星球', 'target_num': 20}, {'completed_num': 0, 'gift_id': 31039, 'gift_img': 'https://s1.hdslb.com/bfs/live/91ac8e35dd93a7196325f1e2052356e71d135afb.png', 'gift_name': '礼物星球', 'target_num': 10}, {'completed_num': 0, 'gift_id': 31049, 'gift_img': 'https://s1.hdslb.com/bfs/live/96ec38f351a4e190c4a525bc5e11ff09d2874064.png', 'gift_name': '礼物星球', 'target_num': 1}], 'reward_gift': 32267, 'reward_gift_img': 'https://s1.hdslb.com/bfs/live/1d8f2ea594841e70729d9635fa6a7688b94dbaa6.png', 'reward_gift_name': '礼物星球', 'start_date': 20230814, 'version': 1692341473006}, 'is_report': False, 'msg_id': '1985789563525632', 'send_time': 1692341473009}
#cmd=PK_BATTLE_SETTLE_NEW, command={'cmd': 'PK_BATTLE_SETTLE_NEW', 'data': {'battle_type': 6, 'dm_conf': {'bg_color': '#72C5E2', 'font_color': '#FFE10B'}, 'dmscore': 144, 'init_info': {'assist_info': [{'face': 'http://i2.hdslb.com/bfs/face/b6855e2bcc6475406b1e60fd9364be0ae3faa653.jpg', 'rank': 1, 'score': 690, 'uid': 3808439, 'uname': '游艇前卫研究员'}], 'result_type': -1, 'room_id': 30069277, 'votes': 690}, 'match_info': {'assist_info': [{'face': 'http://i1.hdslb.com/bfs/face/7d9e380ec780c5b7250cc0f800396923c75cbb6d.jpg', 'rank': 1, 'score': 952, 'uid': 35432083, 'uname': 'OrientLee阳'}], 'result_type': 2, 'room_id': 29005195, 'votes': 952}, 'pk_id': 329569864, 'pk_status': 601, 'punish_end_time': 1692593694, 'punish_name': '惩罚', 'settle_status': 1, 'timestamp': 1692593514}, 'is_report': False, 'msg_id': '2117931931032064', 'pk_id': 329569864, 'pk_status': 601, 'send_time': 1692593514573, 'timestamp': 1692593514}
#cmd=PK_BATTLE_PUNISH_END, command={'cmd': 'PK_BATTLE_PUNISH_END', 'data': {'battle_type': 6}, 'is_report': False, 'msg_id': '2118026214791681', 'pk_id': '329569864', 'pk_status': 1001, 'send_time': 1692593694405, 'status_msg': '', 'timestamp': 1692593694}
#cmd=NEW_PK_REJECT, command={'cmd': 'NEW_PK_REJECT', 'data': {'attention': 0, 'current_time': 1692595100, 'face': '', 'invited_id': 14230080, 'reject_reason': 0, 'toast': '对方主播正忙，换个主播PK吧~', 'type': 3, 'uid': 3494354431773519, 'uname': '', 'virtual_id': 0}, 'is_report': False, 'msg_id': '2118763210614272', 'room_id': 0, 'send_time': 1692595100113}
#cmd=ENTRY_EFFECT_MUST_RECEIVE, command={'cmd': 'ENTRY_EFFECT_MUST_RECEIVE', 'data': {'basemap_url': 'https://i0.hdslb.com/bfs/live/mlive/d4708dee21646e6ebcc58e7f6fa2a972c1d25b36.png', 'business': 3, 'copy_color': '#000000', 'copy_writing': '欢迎 <%瑜伽梦莹莹%> 进入直播间', 'copy_writing_v2': '欢迎 <^icon^> <%瑜伽梦莹莹%> 进入直播间', 'effect_silent_time': 0, 'effective_time': 2, 'effective_time_new': 0, 'face': 'https://i0.hdslb.com/bfs/face/9a352d29a94f79c92d246468e4a4641234880a7c.jpg', 'highlight_color': '#FFF100', 'icon_list': [2], 'id': 136, 'identities': 22, 'max_delay_time': 7, 'mobile_dynamic_url_webp': '', 'mock_effect': 0, 'new_style': 0, 'priority': 1, 'privilege_type': 0, 'show_avatar': 1, 'target_id': 525088653, 'trigger_time': 1692595788901909800, 'uid': 525088653, 'wealthy_info': None, 'web_basemap_url': 'https://i0.hdslb.com/bfs/live/mlive/d4708dee21646e6ebcc58e7f6fa2a972c1d25b36.png', 'web_close_time': 900, 'web_dynamic_url_apng': '', 'web_dynamic_url_webp': '', 'web_effect_close': 0, 'web_effective_time': 2}, 'is_report': False, 'msg_id': '2119124934206977', 'send_time': 1692595790046}
#cmd=RING_STATUS_CHANGE_V2, command={'cmd': 'RING_STATUS_CHANGE_V2', 'data': {'status': 1}, 'is_report': False, 'msg_id': '2119717139011072', 'send_time': 1692596919587}
#cmd=AREA_RANK_CHANGED, command={'cmd': 'AREA_RANK_CHANGED', 'data': {'action_type': 1, 'conf_id': 16, 
#cmd=COMMON_NOTICE_DANMAKU, command={'cmd': 'COMMON_NOTICE_DANMAKU', 'data': {'content_segments': [{'background_color': None, 'background_color_dark': None, 'font_bold': False, 'font_color': '#FB7299', 'font_color_dark': '', 'highlight_font_color': '', 'highlight_font_color_dark': '', 'img_height': 0, 'img_url': '', 'img_width': 0, 'text': '鹊幸相遇七夕夜：任务即将结束，抓紧完成获取7元红包奖励吧！未完成任务将无法获得奖励', 'type': 1}], 'danmaku_style': {'background_color': None, 'background_color_dark': None}, 'dmscore': 144, 'terminals': [1, 2, 3, 4, 5]}, 'is_report': False, 'msg_id': '2116845312157184', 'send_time': 1692591442012}
#cmd=COMBO_END, command={'cmd': 'COMBO_END', 'data': {'action': '投喂', 'batch_combo_num': 1, 'coin_type': 'gold', 'combo_num': 1, 'combo_total_coin': 6000, 'end_time': 1692591573, 'gift_id': 33190, 'gift_name': '桃花守护', 'gift_num': 1, 'guard_level': 3, 'name_color': '#00D1F1', 'price': 6000, 'r_uname': '瑜伽梦莹莹', 'ruid': 525088653, 'send_master': None, 'start_time': 1692591573, 'uid': 35432083, 'uname': 'OrientLee阳'}, 'is_report': False, 'msg_id': '2116916849170945', 'send_time': 1692591578458}
#cmd=SPREAD_SHOW_FEET, command={'cmd': 'SPREAD_SHOW_FEET', 'data': {'click': 1533, 'coin_cost': 200, 'coin_num': 200, 'order_id': 4030250, 'plan_percent': 100, 'show': 27629, 'timestamp': 1692591659, 'title': '流量包推广', 'total_online': 12328, 'uid': 525088653}, 'is_report': False, 'msg_id': '2116959379937792', 'send_time': 1692591659579}
#cmd=SPREAD_SHOW_FEET_V2, command={'cmd': 'SPREAD_SHOW_FEET_V2', 'data': {'click': 1533, 'coin_cost': 0, 'coin_num': 200, 'cover_btn': '', 'cover_url': '', 'live_key': '407157900347872651', 'order_id': 4030250, 'order_type': 3, 'plan_percent': 0, 'show': 27629, 'status': 2, 'timestamp': 1692591659, 'title': '流量包推广', 'total_online': 12328, 'uid': 525088653}, 'is_report': False, 'msg_id': '2116959373646336', 'send_time': 1692591659567}
#cmd=VOICE_JOIN_LIST, command={'cmd': 'VOICE_JOIN_LIST', 'data': {'apply_count': 0, 'category': 1, 'cmd': '', 'red_point': 1, 'refresh': 1, 'room_id': 9453708}, 'is_report': False, 'msg_id': '2124882713795072', 'room_id': 9453708, 'send_time': 1692606772139}
#cmd=VOICE_JOIN_ROOM_COUNT_INFO, command={'cmd': 'VOICE_JOIN_ROOM_COUNT_INFO', 'data': {'apply_count': 0, 'cmd': '', 'notify_count': 0, 'red_point': 0, 'room_id': 9453708, 'room_status': 1, 'root_status': 1}, 'is_report': False, 'msg_id': '2124882711697920', 'room_id': 9453708, 'send_time': 1692606772135}
#cmd=VOICE_JOIN_STATUS, command={'cmd': 'VOICE_JOIN_STATUS', 'data': {'channel': '17418216', 'channel_type': 'voice', 'current_time': 1692606772, 'guard': 3, 'head_pic': 'https://i2.hdslb.com/bfs/face/997867a563f40d6bfd3657eba2fe483df90ad03e.jpg', 'room_id': 9453708, 'start_at': 1692606772, 'status': 1, 'uid': 10083605, 'user_name': '雪下幡衣', 'web_share_link': 'https://live.bilibili.com/h5/9453708'}, 'is_report': False, 'msg_id': '2124882703306753', 'room_id': 9453708, 'send_time': 1692606772119}
#cmd=ANCHOR_HELPER_DANMU, command={'cmd': 'ANCHOR_HELPER_DANMU', 'data': {'button_label': 1, 'button_name': '去看看', 'button_platform': 3, 'button_target': 'bililive://blink/open_voicelink', 'msg': '我是发电机的狗申请了语音连麦', 'platform': 3, 'report': '', 'report_type': '', 'sender': '直播小助手'}, 'is_report': False, 'msg_id': '2125575250006018', 'send_time': 1692608093047}
#cmd=NEW_PK_REJECT, command={'cmd': 'NEW_PK_REJECT', 'data': {'attention': 0, 'current_time': 1692666172, 'face': 'https://i0.hdslb.com/bfs/face/7501385006102eef0a4baa784efea6f902714c3e.jpg', 'invited_id': 14266170, 'reject_reason': 0, 'toast': '对方主播已取消PK邀请~', 'type': 2, 'uid': 3493281593821614, 'uname': '果果有点甜-缺舰长版', 'virtual_id': 0}, 'is_report': False, 'msg_id': '2156025535276544', 'room_id': 0, 'send_time': 1692666172357}
#cmd=MULTI_VOICE_ENTER_ANCHOR, command={'cmd': 'MULTI_VOICE_ENTER_ANCHOR', 'data': {'actual_position': 5, 'anchor_uid': 694860986, 'avatar': 'https://i2.hdslb.com/bfs/face/ce7930e873b4b5605e87909e840c817ba1cde15b.jpg', 'gender': 0, 'nickname': '柱崽崽c', 'role': 1, 'trace_id': '1361205288d85b9213f22f134364e409', 'uid': 3493272666245684, 'version': 1692666195314198000, 'want_position': 5}, 'is_report': False, 'msg_id': '2156037570307584', 'send_time': 1692666195312}
#cmd=MULTI_VOICE_APPLICATION_ANCHOR, command={'cmd': 'MULTI_VOICE_APPLICATION_ANCHOR', 'data': {'anchor_uid': 694860986, 'channel': '', 'count': 1, 'event': 1, 'operate_uid': 0, 'role': 0, 'roomId': 0, 'toast': '申请了连麦', 'trace_id': '0fdca39e7ff1919d7aed854a8664e409', 'uid': 3537118548724448, 'want_position': 8}, 'is_report': False, 'msg_id': '2156047292192256', 'send_time': 1692666213855}
#cmd=MULTI_VOICE_APPLICATION_USER, command={'cmd': 'MULTI_VOICE_APPLICATION_USER', 'data': {'anchor_uid': 694860986, 'channel': '', 'count': 1, 'event': 1, 'operate_uid': 0, 'role': 0, 'roomId': 27383404, 'toast': '申请了连麦', 'trace_id': '', 'uid': 3537118548724448, 'want_position': 8}, 'is_report': False, 'msg_id': '2156047294814720', 'send_time': 1692666213860}
#cmd=MULTI_VOICE_OPERATIN, command={'cmd': 'MULTI_VOICE_OPERATIN', 'data': {'hat': None, 'position': 6, 'room_id': 26751600, 'total_price': 100000, 'total_price_text': '1000', 'ts': 1692666257002166000, 'uid': 1267555635, 'version': 1692666257002166000}, 'is_report': False, 'msg_id': '2156069909975040', 'send_time': 1692666256995}
#cmd=room_admin_entrance, command={'cmd': 'room_admin_entrance', 'dmscore': 45, 'is_report': False, 'level': 1, 'msg': '系统提示：你已被主播设为房管', 'msg_id': '2156091425705984', 'send_time': 1692666298033, 'uid': 8379992}
#cmd=ROOM_ADMINS, command={'cmd': 'ROOM_ADMINS', 'is_report': False, 'msg_id': '2156091418892800', 'send_time': 1692666298020, 'uids': [229530180, 8379992]}
#cmd=USER_TOAST_MSG, command={'cmd': 'USER_TOAST_MSG', 'data': {'anchor_show': True, 'color': '#E17AFF', 'dmscore': 96, 'effect_id': 398, 'end_time': 1692666308, 'face_effect_id': 43, 'gift_id': 10002, 'guard_level': 2, 'is_show': 0, 'num': 1, 'op_type': 2, 'payflow_id': '2308220904501452879608106', 'price': 1598000, 'role_name': '提督', 'room_effect_id': 591, 'start_time': 1692666308, 'svga_block': 0, 'target_guard_count': 23, 'toast_msg': '<%超级无敌顶级甜妹里里%> 在主播一只憨里里的直播间续费了提督，今天是TA陪伴主播的第36天', 'uid': 2032937960, 'unit': '月', 'user_show': True, 'username': '超级无敌顶级甜妹里里'}, 'is_report': False, 'msg_id': '2156097738133504', 'send_time': 1692666310073}
#cmd=POPULAR_RANK_CHANGED, command={'cmd': 'POPULAR_RANK_CHANGED', 'data': {'cache_key': 'rank_change:258773b2e0d44668a0684db2617efc71', 'countdown': 3226, 'rank': 37, 'timestamp': 1692666375, 'uid': 3494374000298808}, 'is_report': False, 'msg_id': '2156131817377792', 'send_time': 1692666375074}
#cmd=ANCHOR_HELPER_DANMU, command={'cmd': 'ANCHOR_HELPER_DANMU', 'data': {'button_label': 1, 'button_name': '去看看', 'button_platform': 3, 'button_target': 'bililive://blink/open_voicelink', 'msg': '是笨笨竹家的炒丝er申请了语音连麦', 'platform': 3, 'report': '', 'report_type': '', 'sender': '直播小助手'}, 'is_report': False, 'msg_id': '2156188341392384', 'send_time': 1692666482885}
#cmd=GIFT_STAR_PROCESS, command={'cmd': 'GIFT_STAR_PROCESS', 'data': {'status': 1, 'tip': '干杯已点亮'}, 'is_report': False, 'msg_id': '2156876346707968', 'send_time': 1692667795151}
#cmd=ROOM_BLOCK_MSG, command={'cmd': 'ROOM_BLOCK_MSG', 'data': {'dmscore': 30, 'operator': 2, 'uid': 1866017744, 'uname': '取名老难了m'}, 'is_report': False, 'msg_id': '2159658628831744', 'send_time': 1692673101933, 'uid': '1866017744', 'uname': '取名老难了m'}
#cmd=ANCHOR_LOT_END, command={'cmd': 'ANCHOR_LOT_END', 'data': {'id': 4828490}, 'is_report': False, 'msg_id': '2160823380236800', 'send_time': 1692675323520}
#cmd=ANCHOR_LOT_AWARD, command={'cmd': 'ANCHOR_LOT_AWARD', 'data': {'award_dont_popup': 1, 'award_image': '', 'award_name': '告白花束', 'award_num': 1, 'award_price_text': '价值220电池', 'award_type': 1, 'award_users': [{'uid': 99452582, 'uname': 'xuafye', 'face': 'https://i2.hdslb.com/bfs/face/8a53837767e6f5f1c905a67f233043d8b0e184ae.jpg', 'level': 21, 'color': 5805790, 'bag_id': 7024291, 'gift_id': 31157, 'num': 1}], 'id': 4844479, 'lot_status': 2, 'ruid': 333334084, 'url': 'https://live.bilibili.com/p/html/live-lottery/anchor-join.html?is_live_half_webview=1&hybrid_biz=live-lottery-anchor&hybrid_half_ui=1,5,100p,100p,000000,0,30,0,0,1;2,5,100p,100p,000000,0,30,0,0,1;3,5,100p,100p,000000,0,30,0,0,1;4,5,100p,100p,000000,0,30,0,0,1;5,5,100p,100p,000000,0,30,0,0,1;6,5,100p,100p,000000,0,30,0,0,1;7,5,100p,100p,000000,0,30,0,0,1;8,5,100p,100p,000000,0,30,0,0,1', 'web_url': 'https://live.bilibili.com/p/html/live-lottery/anchor-join.html'}}
#cmd=POPULARITY_RED_POCKET_NEW, command={'cmd': 'POPULARITY_RED_POCKET_NEW', 'data': {'lot_id': 13975641, 'start_time': 1692856246, 'current_time': 1692856246, 'wait_num': 0, 'uname': '机智的歆瑶瑶', 'uid': 7996864, 'action': '送出', 'num': 1, 'gift_name': '红包', 'gift_id': 13000, 'price': 20, 'name_color': '#E17AFF', 'medal_info': {'target_id': 0, 'special': '', 'icon_id': 0, 'anchor_uname': '', 'anchor_roomid': 0, 'medal_level': 0, 'medal_name': '', 'medal_color': 0, 'medal_color_start': 0, 'medal_color_end': 0, 'medal_color_border': 0, 'is_lighted': 0, 'guard_level': 0}, 'wealth_level': 27}}
#cmd=POPULARITY_RED_POCKET_START, command={'cmd': 'POPULARITY_RED_POCKET_START', 'data': {'lot_id': 13975641, 'sender_uid': 7996864, 'sender_name': '机智的歆瑶瑶', 'sender_face': 'https://i1.hdslb.com/bfs/face/73a31b9196fc50fcb5c0682742cbcdec07c52e72.jpg', 'join_requirement': 1, 'danmu': '老板大气！点点红包抽礼物', 'current_time': 1692856247, 'start_time': 1692856246, 'end_time': 1692856426, 'last_time': 180, 'remove_time': 1692856441, 'replace_time': 1692856436, 'lot_status': 1, 'h5_url': 'https://live.bilibili.com/p/html/live-app-red-envelope/popularity.html?is_live_half_webview=1&hybrid_half_ui=1,5,100p,100p,000000,0,50,0,0,1;2,5,100p,100p,000000,0,50,0,0,1;3,5,100p,100p,000000,0,50,0,0,1;4,5,100p,100p,000000,0,50,0,0,1;5,5,100p,100p,000000,0,50,0,0,1;6,5,100p,100p,000000,0,50,0,0,1;7,5,100p,100p,000000,0,50,0,0,1;8,5,100p,100p,000000,0,50,0,0,1&hybrid_rotate_d=1&hybrid_biz=popularityRedPacket&lotteryId=13975641', 'user_status': 2, 'awards': [{'gift_id': 31212, 'gift_name': '打call', 'gift_pic': 'https://s1.hdslb.com/bfs/live/461be640f60788c1d159ec8d6c5d5cf1ef3d1830.png', 'num': 2}, {'gift_id': 31214, 'gift_name': '牛哇', 'gift_pic': 'https://s1.hdslb.com/bfs/live/91ac8e35dd93a7196325f1e2052356e71d135afb.png', 'num': 3}, {'gift_id': 31216, 'gift_name': '小花花', 'gift_pic': 'https://s1.hdslb.com/bfs/live/5126973892625f3a43a8290be6b625b5e54261a5.png', 'num': 3}], 'lot_config_id': 3, 'total_price': 1600, 'wait_num': 0}}













Global_30s_times = 0
__Global_like_queue = Queue()  # 创建进入、点赞队列对象
__Global_danmu_queue = Queue()  # 创建弹幕队列对象
__Global_gift_queue = Queue()  # 创建送礼队列对象
#{"time":int,"uid":uid,"uname":uname,"type":MsgType,"message":diff type}

print('wss_danmu v5.9.5 ROOM_IDS:',ROOM_IDS,TEXT_THANKS_GIFTNAME_AT_UNAME)

####################### class_voice #########################################
def put_like(uid,uname,itype,message):
    global __Global_like_queue
    now = time.time()
    msg = {
        "time":now,
        "uid":uid,
        "uname":uname,
        "type":itype,
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

def put_danmu(uid,uname,itype,message):
    global __Global_danmu_queue
    now = time.time()
    msg = {
        "time":now,
        "uid":uid,
        "uname":uname,
        "type":itype,
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

def put_gift(uid,uname,itype,message):
    # 附加回弹幕的返回，True=需回弹幕
    # 同一个人的同一gift_id礼物只在__Global_gift_queue里存一次
    # 同一个人的不同gift_id礼物可以回不同danmu，避免超20字
    global __Global_gift_queue
    now = time.time()
    # 先把gift取出来，看看新的是否需要加上，再放回去
    msg_list = get_gift_all()
    not_in_list = not is_uid_gift_in_list(message,msg_list)
    if not_in_list:
        msg = {
            "time":now,
            "uid":uid,
            "uname":uname,
            "type":itype,
            "message":message
        }
        # 加上新的
        __Global_gift_queue.put(msg)
    for msg in msg_list:
        # 放回去
        __Global_gift_queue.put(msg)
    return not_in_list

def is_uid_gift_in_list(message,msg_list):
    for msg in msg_list:
        if msg.get('message').uid == message.uid:
            if msg.get('message').gift_id == message.gift_id:
                return True
    return False

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
            print("INTERACT",str(ROOM_IDS[0])[0:4],obj.get('t_'+str(ROOM_IDS[0])),str(ROOM_IDS[1])[0:4],obj.get('t_'+str(ROOM_IDS[1])),str(ROOM_IDS[2])[0:4],obj.get('t_'+str(ROOM_IDS[2])),"like:",obj.get('like'),obj.get('uid'),obj.get('uname'))
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
            print("LIKE_CLICK:record:",str(ROOM_IDS[0])[0:4],obj.get('t_'+str(ROOM_IDS[0])),str(ROOM_IDS[1])[0:4],obj.get('t_'+str(ROOM_IDS[1])),str(ROOM_IDS[2])[0:4],obj.get('t_'+str(ROOM_IDS[2])),"gift:",obj.get('gift'),"like:",obj.get('like'),obj.get('uid'),obj.get('uname'))
        else:
            print(f"LIKE_INFO_V3_CLICK: not found:{command['data']['uname']}")
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
        if put_gift(message.uid,message.uname,MsgType.SEND_GIFT,message):
            text = TEXT_THANKS_GIFTNAME_AT_UNAME.format(message.gift_name,message.uname)
            danmu.delay_send(client.room_id,text,random.randint(5,8))
        print('#'*20,'SEND_GIFT','#'*20)
        print(f'[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
              f' （{message.coin_type}瓜子x{message.total_coin}）')
        obj = class_viewer.gift(message.uid,message.total_coin)
        if obj:
            print("GIFT:record:",str(ROOM_IDS[0])[0:4],obj.get('t_'+str(ROOM_IDS[0])),str(ROOM_IDS[1])[0:4],obj.get('t_'+str(ROOM_IDS[1])),str(ROOM_IDS[2])[0:4],obj.get('t_'+str(ROOM_IDS[2])),"gift:",obj.get('gift'),"like:",obj.get('like'),obj.get('uid'),obj.get('uname'))
        else:
            print("GIFT: uid not found",message.uid)

    async def _on_buy_guard(self, client: blivedm.BLiveClient, message: blivedm.GuardBuyMessage):
        put_gift(message.uid,message.username,MsgType.GUARD_BUY,message)
        print('#'*20,'GUARD_BUY','#'*20)
        #danmu.send(client.room_id,TEXT_THANKS_GIFTNAME_AT_UNAME.format(message.gift_name,message.uname))
        print(f'[{client.room_id}] {message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, client: blivedm.BLiveClient, message: blivedm.SuperChatMessage):
        put_gift(message.uid,message.username,MsgType.SUPER_CHAT_MESSAGE,message)
        print(f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')

def start(room_id):
    asyncio.run(start_client(room_id))

if __name__ == '__main__':
    asyncio.run(start_client(ROOM_IDS[0]))
    #asyncio.run(await_start())
