#encoding=utf8
'''
Created on 2015年7月30日

@author: admin
'''

class ConfigkeyError(Exception):
    def __init__(self, confkey, confvalue):
        self.__confkey = confkey
        self.__confvalue= confvalue

    def __str__(self):
        print "配置文件的 key=%s 不存在" % self.__confkey
        
class ConfigvalueError(Exception):
    def __init__(self, confkey, confvalue):
        self.__confkey = confkey
        self.__confvalue= confvalue

    def __str__(self):
        print "配置文件的 key=%s 必须有值" % self.__confkey