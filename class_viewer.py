# coding: utf-8

import leancloud

DB_NAME = 'viewer'
ROOM_IDS = [
    30338274,
    30356247,
    27791346,
]
print('class_viewer v5.9.0 ROOM_IDS:',ROOM_IDS)
###########################################################
###########################################################
def new_viewer(roomid,uid,uname):
    # return object
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.equal_to('uid', uid)
    find = query.find()
    if find:
        # 老viewer到访,times+1
        viewer = DBClass.create_without_data(find[0].get('objectId'))
        viewer.increment('t_'+str(roomid), 1)
        viewer.save()
        return find[0]
    else:
        viewer = DBClass()
        viewer.set('uid', uid)
        viewer.set('uname', uname)
        viewer.set('ignore', True)
        viewer.set('like', 0)
        for room in ROOM_IDS:
            if room == roomid:
                viewer.set('t_'+str(room), 1)
            else:
                viewer.set('t_'+str(room), 0)
        viewer.save()
        return None
    
def like(uid):
    # return object
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.equal_to('uid', uid)
    find = query.find()
    if find:
        # 老viewer like,like+1
        viewer = DBClass.create_without_data(find[0].get('objectId'))
        viewer.increment('like', 1)
        viewer.save()
        return find[0]
    return None

def gift(uid,coin):
    # return object
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.equal_to('uid', uid)
    find = query.find()
    if find:
        # 老viewer like,like+1
        viewer = DBClass.create_without_data(find[0].get('objectId'))
        viewer.increment('gift', coin)
        viewer.save()
        return find[0]
    return None

def unignore_viewer_by_uname(uname):
    # return array
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.equal_to('uname', uname)
    #query.equal_to('ignore', True)
    find = query.find()
    if find:
        #print(find)
        #return find[0]
        viewer = DBClass.create_without_data(find[0].get('objectId'))
        viewer.set('ignore', False)
        viewer.save()
        return True
    return False

def ignore_array():
    # return array
    DBClass = leancloud.Object.extend( DB_NAME )
    query = DBClass.query
    query.limit(1000)
    query.equal_to('ignore', True)
    return query.find()