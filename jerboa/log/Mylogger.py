# encoding=utf8
'''
Created on 2015年7月30日

@author: 俞永鹏
'''
# import logging
import logging.config
import sys,os

class Mylogger(object):
    '''
    处理日志输出的类
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def getlog(self):
#         print os.path.split(os.path.realpath(__file__))[0]
#         print os.getcwd()
#         print sys.path[0]
        os.chdir(os.path.split(os.path.realpath(__file__))[0])
        logging.config.fileConfig("../conf/log.conf")
        logger = logging.getLogger("ssss")
        f_handler=open(logger.parent.handlers[1].baseFilename, 'a') 
#         sys.stderr=f_handler
#         sys.stdout=f_handler 
        print os.getcwd()
        print logger.parent
        return logger
        



if __name__ == "__main__":
    print sys.path[0]
    logging.config.fileConfig("../conf/log.conf")
    logger = logging.getLogger("Myloggerxxxxxx")
    print logger.parent.handle
    
    logger.debug('This is debug message')
    logger.info('This is info message')
    logger.warning('This is warning message')
    sys.stderr.write('Warning, log file not found starting a new one\n')
    f_handler=open(logger.parent.handlers[1].baseFilename, 'a') 
    sys.stderr=f_handler 
    lg = Mylogger()
    lg.et()
