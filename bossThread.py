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

class BossThread(threading.Thread):
    def __init__(self, count=18):
        threading.Thread.__init__(self)
        self.daemon = False
        self.count = count

    def bianzhen(self, keji):
        retry = 10
        t = 1 
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.bianzhen(keji)
                sanguo.close()
                if not data:
                    logger.error('bianzhen failed, data None')
                    raise Exception()
                logger.info('bianzhen %s succeed'%(keji))
                return data
            except:
                logger.info('bianzhen failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1
    
    def do_attack(self):
        retry = 10
        t = 1 
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.attackBoss()
                sanguo.close()
                if not data:
                    logger.error('Boss failed, data None')
                    raise Exception()
                logger.info('attack Boss succeed')
                return data
            except:
                logger.info('do_attack failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1

    def run(self):
        logger.info('BossThread start')
        if Delay_Time > 0:
            logger.info('I will start attack at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        self.bianzhen('cangse')
        time.sleep(2)

        gi = GeneralInfo()
        start_time = util.get_xiongsou_refresh_time(gi.get_serverTime())
        ls_diff = gi.get_localTime() - gi.get_serverTime()
        sp = util.get_sleep_time(start_time, ls_diff) + 1
        if sp > 0:
            logger.info('I will sleep till start time, will attack at %s'%(util.next_time(sp)))
            time.sleep(sp)
        else:
            time.sleep(2)

        times = 0
        while True:
            times += 1
            if times > Times:
                logger.info('already attack %d times, exit'%(Times))
                break

            res = self.do_attack()
            if res.has_key('exception'):
                logger.error('Got Exception "%s"'%(res['exception']['message']))
                if 'attackCoolTime' == res['exception']['message']:
                    times -= 1
                else:
                    break
            logger.info('attacked %d times'%(times))

            gi = GeneralInfo()
            cd = gi.get_xiongsou_CDTime()
            stime = gi.get_serverTime()
            if cd > stime:
                sp = cd - stime + 1
                logger.info('I will sleep CD, will attack at %s'%(util.next_time(sp)))
                time.sleep(sp)
            else:
                time.sleep(2)
        self.bianzhen('yanxing')

def parsearg():
    global Delay_Time, Times
    parser = argparse.ArgumentParser(description='Get attack')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to attack')
    parser.add_argument('-t', '--times', required=False, type=int, default=5, help='attack times')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Times = res.times

if __name__ == '__main__':
    parsearg()
    thread = BossThread()
    thread.start()
