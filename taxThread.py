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
Remain = 0
MaxSilverExit = False

class TaxThread(threading.Thread):
    def __init__(self, count=18):
        threading.Thread.__init__(self)
        self.daemon = False
        self.count = count
    
    def do_tax(self):
        retry = 10
        t = 1 
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.tax()
                sanguo.close()
                if not data:
                    logger.error('Tax failed, data None')
                    raise Exception()
                logger.info('Tax succeed')
                return data
            except:
                logger.info('do_tax failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1

    def run(self):
        logger.info('TaxThread start')
        if Delay_Time > 0:
            logger.info('I will start tax at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        while True:
            gi = GeneralInfo()
            if gi.get_levy_remain() <= Remain:
                logger.info('Tax remain time is %d, will exit'%(gi.get_levy_remain()))
                return
            else:
                logger.info('Tax remain %d times'%(gi.get_levy_remain()))
            cd = gi.get_tax_CDTime()
            stime = gi.get_serverTime()
            if cd > stime:
                sp = cd - stime + 1
                logger.info('I will sleep CD, will tax at %s'%(util.next_time(sp)))
                time.sleep(sp)
            else:
                time.sleep(1)
            res = self.do_tax()
            if res.has_key('exception'):
                logger.error('Got Exception "%s"'%(res['exception']['message']))
                if 'beyondMaxSilver' == res['exception']['message']:
                    if MaxSilverExit:
                        return
                    else:
                        sp = 1800
                        logger.info('I will tax at %s'%(util.next_time(sp)))
                        time.sleep(sp)
                        continue
                time.sleep(60)
            time.sleep(1)

def parsearg():
    global Delay_Time, Times, MaxSilverExit, Remain
    parser = argparse.ArgumentParser(description='Get tax')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to tax')
    parser.add_argument('-r', '--remain', required=False, type=int, default=0, help='tax remain times')
    parser.add_argument('-x', '--exit', required=False, action='store_true', help='exit when beyondMaxSilver')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    MaxSilverExit = res.exit
    Remain = res.remain

if __name__ == '__main__':
    parsearg()
    thread = TaxThread()
    thread.start()
