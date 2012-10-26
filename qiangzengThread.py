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
Times = 0 

class EnforcelevyThread(threading.Thread):
    def __init__(self, count=18):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def do_enforcelevy(self):
        retry = 10
        t = 1 
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.enforce_levy()
                sanguo.close()
                if not data:
                    logger.error('Enforcelevy failed, data None')
                    raise Exception()
                logger.info('Enforcelevy succeed')
                return data
            except:
                logger.info('do_enforcelevy failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1

    def run(self):
        logger.info('EnforcelevyThread start, will do %d times'%(Times))
        if Delay_Time > 0:
            logger.info('I will start enforcelevy at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        for i in range(Times):
            try:
                res = self.do_enforcelevy()
                if res.has_key('exception'):
                    logger.error('Got Exception "%s"'%(res['exception']['message']))
                    return
                logger.info('qiangzeng %d times'%(i+1))
                time.sleep(2)
            except:
                pass

def parsearg():
    global Delay_Time, Times
    parser = argparse.ArgumentParser(description='Get enforcelevy')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to enforcelevy')
    parser.add_argument('-t', '--times', required=False, type=int, default=1, help='times')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Times = res.times

if __name__ == '__main__':
    parsearg()
    thread = EnforcelevyThread()
    thread.start()
