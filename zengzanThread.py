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
from NpcInfo import NpcInfo
from settings import *

logger = Logger.getLogger()

Delay_Time = 0 
Npc_String = None
Times = 100
FirstTime = True
global_times = 0

class zengzanThread(threading.Thread):
    def __init__(self, count=18):
        threading.Thread.__init__(self)
        self.daemon = False
        self.count = count
    
    def do_zengzan(self, nstr):
        retry = 10
        t = 1 
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.zengzan(nstr)
                sanguo.close()
                if not data:
                    raise Exception()
                return data
            except:
                logger.info('do_zengzan failed, will sleep 2 seconds')
                time.sleep(2)
                t += 1

    def zengzan(self, nstr, times=1):
        global global_times
        res = None
        for i in range(times):
            if global_times >= Times:
                logger.info('zengzan %d times, exit'%(Times))
                sys.exit()
            res = self.do_zengzan(nstr)
            if res.has_key('exception'):
                return res
            global_times += 1
            logger.info('zengzan %s %d times'%(nstr, global_times))
            if i < times-1:
                time.sleep(2)
        return res

    def getNpcInfo(self):
        global FirstTime
        nid = NPC_ID[Npc_String]
        if FirstTime:
            FirstTime = False
            times = 1
        else:
            times = 15
        for i in range(times):
            ni = NpcInfo(nid)
            remain_times = ni.getNumber()
            logger.info('%s remain number %d, serverTime: %s'%(Npc_String, remain_times, util.format_time(ni.getServerTime())))
            if remain_times > 0:
                return ni
            time.sleep(2)
        return ni

    def run(self):
        global FirstTime, Times
        logger.info('zengzanThread start')
        if Delay_Time > 0:
            logger.info('I will start zengzan at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        while True:
            ni = self.getNpcInfo()
            remain_times = ni.getNumber()
            if remain_times > 0:
                time.sleep(2)
                res = self.zengzan(Npc_String, remain_times + 100)
                if res.has_key('exception'):
                    msg = res['exception']['message']
                    logger.info('zengzan exception: %s'%(msg))
                    if msg == 'waittingOrder':
                        gi = GeneralInfo()
                        sp = util.get_sleep_time(gi.get_mobility_CDTime(), gi.get_localTime()-gi.get_serverTime())
                        logger.info('I will sleep for mobility CD to %s'%(util.next_time(sp)))
                        time.sleep(sp)
                        FirstTime = True
                        continue
                    elif msg == 'lessMobility':
                        return
                    else:
                        time.sleep(2)
                        FirstTime = True
                        continue
            nrt = util.get_next_refresh_time(ni.getServerTime())
            sp = util.get_sleep_time(nrt, ni.getLocalTime()-ni.getServerTime()) + 1
            logger.info('I will sleep till time %s'%(util.next_time(sp)))
            time.sleep(sp)

def parsearg():
    global Delay_Time, Npc_String, Times
    parser = argparse.ArgumentParser(description='zengzan')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to zengzan')
    parser.add_argument('-n', '--npc_id', required=False, type=str, default='yinlongjia', help='npc string')
    parser.add_argument('-t', '--times', required=False, type=int, default=100, help='zengzan times')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Npc_String = res.npc_id
    Times = res.times

if __name__ == '__main__':
    parsearg()
    thread = zengzanThread()
    thread.start()
