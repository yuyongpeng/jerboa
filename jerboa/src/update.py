'''
Created on 2015年7月28日

@author: admin
'''
#!/usr/bin/python
# encoding=utf-8
#  -*- coding: utf8 -*-

import calendar
import codecs, sys
from datetime import datetime
import json, httplib, urllib
import os
import string
import time
import types 

from MySQLdb import *
import _mysql_exceptions
from elasticsearch import Elasticsearch, helpers


groupTableName = "countarticle"
dropTable = "drop table if exists " + groupTableName
createTable = "create table " + groupTableName + "  (cu int, title varchar(255), subcontent varchar(500), content text, `delete` int)";
# insertData = "insert into "+groupTableName+" select count(*) as c ,json_extract(a.data,\"title\") as title, 0 from slate_article a where appid=1 group by json_extract(a.data,\"title\") HAVING c>=2"
insertData = ("insert into " + groupTableName + " "
    "select count(*) as c ,json_extract(a.data,\"title\") as title,"
    "json_extract(a.data,\"subcontent\") as subcontent,"
    "json_extract(a.data,\"content\") as content,"
    "0 from slate_article a where appid=1 group by title,subcontent,content HAVING c>=2"
    )

testdata = "透支保护是变相借贷？"
selectTempData = " select cu , title from  " + groupTableName + " where `delete`=0 and title = '%s'" 
selectTempData2 = " select cu , title from  " + groupTableName + " where `delete`=0 and title is not null " 
selectSourceData = " select * from slate_article a where json_extract(a.data,'title') = '%s'  " 
updateSourceData = " update slate_article a set  a.`data`=json_set(a.`data`,'tagname','\"%s\"')  where id=%s "
deleteData = " update slate_article a set a.delete=1 where a.id=%s"
selectTagArticle = " select * from slate_tag_article where articleid=%s "
updateTagArticle = " update slate_tag_article a set a.articleid=%s where a.articleid=%s and tagid='%s' and devicetype=%s "
countTagArticle = " select count(*) from slate_tag_article where  a.articleid=%s and tagid='%s' and devicetype=%s "
deleteTagArticle = " update slate_tag_article a set a.delete=1 where a.articleid=%s "
deleteTmp = "update " + groupTableName + " as a set a.delete=1 where a.title='%s'"


try:
    conn = Connection(user="root", passwd="modernmedia", db="slate_new", host="10.0.7.99", port=3306, cursorclass=cursors.DictCursor, charset="utf8")
except:
    print"Could not connect to MySQL server"
    exit(0)
cur = conn.cursor()
# cur.execute(dropTable)
# cur.execute(createTable)
# cur.execute(insertData)
# conn.commit()
# exit(0)
# cur.execute(selectTempData % (testdata))
cur.execute(selectTempData2)
print selectTempData % (testdata)
for rowFetch in cur.fetchall() :
    title = rowFetch["title"]
    print str(rowFetch["cu"]) + "  " + title
    cur.execute(selectSourceData % title)
    alldata = cur.fetchall()
    # print alldata
    if len(alldata) == 0 :
        continue
    id0 = alldata[0]["id"]
    print id0
    # exit(0)
    a = json.loads(alldata[0]['data'], encoding="UTF-8", strict=False)
    if len(a) == 0 or a == None :
        continue
    tagname0 = a.get("tagname")
    if tagname0 is None :
        continue
    print "NO1.tagname=" + tagname0
    # exit(0)
    for row2 in alldata[1:]:
        try :
            js = json.loads(row2["data"], encoding="UTF-8", strict=False)
        except ValueError, e :
            print e
            continue
        idN = row2["id"]
        tagnameN = js.get("tagname")
        if not tagnameN :
            continue
        print updateSourceData % (tagname0 + "," + tagnameN, id0)
        cur.execute(updateSourceData % (tagname0 + "," + tagnameN, id0))
        print "00000000000000000000"
        cur.execute(deleteData % idN)
        print deleteData % idN
        cur.execute(selectTagArticle % idN)
        allr = cur.fetchall()
        print allr
        for rowTagArticle in allr :
            tagid = rowTagArticle["tagid"]
            devicetype = rowTagArticle["devicetype"]
            try :
                print updateTagArticle % (id0, idN, tagid, devicetype)
                cur.execute(updateTagArticle % (id0, idN, tagid, devicetype))
            except _mysql_exceptions.IntegrityError, e :
                print e
                cur.execute(deleteTagArticle % idN)
                print deleteTagArticle % idN
        conn.commit()
    print deleteTmp % title
    cur.execute(deleteTmp % title)
    conn.commit()
cur.close()  
conn.close()  
print "the end"























