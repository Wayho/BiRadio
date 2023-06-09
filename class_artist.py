# coding=utf-8
import leancloud							#requirements leancloud-sdk>=1.0.9,<=2.0.0
import os

def artist_array(sitename):
    # return array
    DBClass = leancloud.Object.extend( "artist" )
    query = DBClass.query
    query.equal_to('play', True)
    query.equal_to('sitename', sitename)
    query.ascending('rank')
    return query.find()

def rank(objectId):
    DBClass = leancloud.Object.extend( "artist" )
    artist = DBClass.create_without_data(objectId)
    artist.increment('rank', 1)
    artist.save()

if __name__ == '__main__':
        a=1
        