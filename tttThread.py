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

Formations = ['yanxing', 'cangse']
ChangeFormationGap = 50
Delay_Time = 0 
Times = 0 
MaxSilverExit = False

class tttThread(threading.Thread):
    def __init__(self, count=18):
        threading.Thread.__init__(self)
        self.daemon = False
        self.count = count
        self.formation = 0

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
    
    def do_ttt(self):
        retry = 10
        t = 1 
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.tongtianta()
                sanguo.close()
                if not data:
                    logger.error('ttt failed, data None')
                    raise Exception()
                logger.info('tongtianta succeed, result %d'%(data['result']))
                return data
            except:
                logger.info('do_ttt failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                #t += 1

    def run(self):
        global Times
        logger.info('tttThread start')
        if Delay_Time > 0:
            logger.info('I will start ttt at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        t = 0
        while True:
            time.sleep(3)
            res = self.do_ttt()
            if res['result'] == 2:
                t += 1
                if t >= Times:
                    time.sleep(3)
                    self.bianzhen('yanxing')
                    sys.exit()
                rem = (t / ChangeFormationGap) % len(Formations)
                if self.formation != rem:
                    time.sleep(3)
                    self.bianzhen(Formations[rem])
                    self.formation = rem

def parsearg():
    global Delay_Time, Times, MaxSilverExit
    parser = argparse.ArgumentParser(description='Get ttt')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to ttt')
    parser.add_argument('-t', '--times', required=False, type=int, default=200, help='fail times')
    parser.add_argument('-x', '--exit', required=False, action='store_true', help='exit when beyondMaxSilver')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    MaxSilverExit = res.exit
    Times = res.times

if __name__ == '__main__':
    parsearg()
    thread = tttThread()
    thread.start()
