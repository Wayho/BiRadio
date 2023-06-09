# coding=utf-8
import leancloud							#requirements leancloud-sdk>=1.0.9,<=2.0.0
import os

def ShareKeyArray(sitename):
    # return array
    DBClass = leancloud.Object.extend( "ShareKey" )
    query = DBClass.query
    query.equal_to('on', True)
    query.equal_to('sitename', sitename)
    query.descending('updatedAt')
    return query.find()

if __name__ == '__main__':
        a=1
        