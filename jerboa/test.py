# encoding=utf8
'''
Created on 2015年7月30日

@author: 俞永鹏
'''
from log import Mylogger
import ConfigParser
import os
from exception.myerror import *


if __name__ == '__main__':
    logger = Mylogger.Mylogger().getlog()
    logger.info("ffffffffffffffffffffffffffff")
    logger.info("ffffffffffffffffffffffffffff")
    cf = ConfigParser.ConfigParser()
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    cf.read("./conf/default.conf")
    user = cf.get("rabbitmq", "user")
    print user
    
    raise ConfigkeyError("user","xxxxxx")
    print "dddddd"
    