#!/usr/bin/python
#encoding: utf-8
import threading
from sanguo import Sanguo
import time
import sys 
import Logger
import argparse
import datetime
import util
import traceback
from GeneralInfo import GeneralInfo

logger = Logger.getLogger()

Delay_Time = 0 

class HusongThread(threading.Thread):
    def __init__(self, count=18):
        threading.Thread.__init__(self)
        self.daemon = False
        self.count = count
    
    def do_husong(self):
        retry = 10
        t = 1 
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.husong()
                sanguo.close()
                if not data:
                    logger.error('Husong failed, data None')
                    raise Exception()
                logger.info('Husong succeed')
                return data
            except:
                logger.info('do_husong failed, will sleep %d seconds'%(t*2))
                logger.info(traceback.format_exc())
                time.sleep(t*2)
                t += 1

    def run(self):
        logger.info('HusongThread start')
        res = self.do_husong()
        if res.has_key('exception'):
            logger.error('Got Exception "%s"'%(res['exception']['message']))
        logger.info('HusongThread stop')

def parsearg():
    global Delay_Time
    parser = argparse.ArgumentParser(description='husong')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to husong')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60

if __name__ == '__main__':
    parsearg()
    thread = HusongThread()
    thread.start()
