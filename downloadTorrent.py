#!/usr/bin/python2.7

# encoding: utf-8
import os
import urllib2
import MySQLdb as mdb
import sys
import uuid
import StringIO
import gzip
from torrentool.api import Torrent

download_con = None

def getConnect():
    global download_con
    if download_con is None:
        download_con = mdb.connect('104.149.11.206', 'test', 'password', 'test',charset='utf8')
    return download_con

def getHashinforList():
    con = getConnect()
    sqlStr = "select id, hashinfor from hashinfor limit 0,1"
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(sqlStr)
    rows = cur.fetchall();
    cur.close()
    return rows

def deleteHashinfor(id):
    delete_sql = "delete from hashinfor where id=value"
    delete_sql = delete_sql.replace("value", str(id))
    con = getConnect()
    print delete_sql
    try:
        cur = con.cursor()
        cur.execute(delete_sql)
        con.commit()
    finally:
        cur.close()
    
        
def downLoadTorrent():
    dir = "/home/pyHome/download/"
    send_headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Host':'torcache.net',
        'Pragma':'no-cache',
        'If-Range': '"558109a1-2ea3"',
        'Cookie':'_spc=47c787d6-f5b3-aa48-1e88-7d49d3c4b8af',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
    }
    rows = getHashinforList()
    
    for row in rows:
        id = row["id"]
        hashinfor = row["hashinfor"]
        file_name = hashinfor + ".torrent"
        local_file_name = "down.torrent"
        url = "http://torcache.net/torrent/value"
        url = url.replace('value', file_name)
        print url
        print "---------------------------------------"
        try:
            req = urllib2.Request(url, headers=send_headers)
            file = urllib2.urlopen(req, timeout=60).read()
            #gz = gzip.GzipFile()
            isGzip = True
            print "isGzip    " + str(isGzip)
            data = None
            if isGzip:
                compressedstream = StringIO.StringIO(file)
                gzipper = gzip.GzipFile(fileobj=compressedstream)
                data = gzipper.read()
            else:
                data = file
            f = open(dir+local_file_name, "w+")
            f.write(data)
            f.flush()
            f.close()
            print "printdasdsadsadsadsadsad"
            getHashinfor()
        except urllib2.HTTPError, e:
            print e
            continue
        finally:
            print id
            deleteHashinfor(id)

def getHashinfor():
    dir = "/home/pyHome/download/"
    file_path = dir+"down.torrent"
    file_name = ""
    #print file_path
    my_torrent = None
    my_torrent = Torrent.from_file(file_path)
    #print type(my_torrent)
    print my_torrent.magnet_link
    files = my_torrent.files
    con = getConnect()
    print files
    print "------------------------------------------"
    try:
        uuid1 = str(uuid.uuid1())
        for file in files:
            sqlStr = "insert into torrent_info (name, size, mangent, fkey) VALUES('v1', v2, 'v3', 'v4')"
            name = file[0].replace("'", "\'");
            sqlStr = sqlStr.replace("v1", name)
            sqlStr = sqlStr.replace("v2", str(file[1]))
            sqlStr = sqlStr.replace("v3", "#")
            sqlStr = sqlStr.replace("v4", uuid1)
            print sqlStr
            cur = con.cursor()
            cur.execute(sqlStr)
            con.commit()
    finally:
        cur.close()
    #    print "asd"

if __name__ == '__main__':
    #getHashinfor()
    downLoadTorrent()