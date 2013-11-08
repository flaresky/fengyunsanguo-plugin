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
import json
from EquipInfo import EquipInfo

logger = Logger.getLogger()

Delay_Time = 0 
Times = 0 
Eid = None
Level = 0

class jinglianThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False

    def run(self):
        logger.info('jinglianThread %s start, will jinglian to level %d'%(Eid, Level))
        if Delay_Time > 0:
            logger.info('I will start jinglian at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        level = 0
        while level < Level:
            res = util.send_command('jinglianEquip', Eid)
            if res is not None:
                if res.has_key('exception'):
                    msg = res['exception']['message']
                    if msg == 'upFail':
                        logger.info('jinglian fail')
                    else:
                        logger.info('got Exception %s, exit'%(msg))
                        sys.exit()
                else:
                    level = int(res['userEquip']['starLevel'])
                    logger.info('jinglian to level %d'%(level))
                    if level >= Level:
                        sys.exit()
                sp = 300
                logger.info('next round will start at ' + util.next_time(sp))
                time.sleep(sp)

def parsearg():
    global Delay_Time, Times, Eid, Level
    parser = argparse.ArgumentParser(description='jinglian equip')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay')
    parser.add_argument('-i', '--equip_id', required=False, type=str, default='471179', help='equip id')
    parser.add_argument('-l', '--level', required=False, type=int, default=1, help='max jinglian level')
    #parser.add_argument('-t', '--times', required=False, type=int, default=1, help='jinglian times')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    #Times = res.times
    Eid = res.equip_id
    Level = res.level

if __name__ == '__main__':
    parsearg()
    thread = jinglianThread()
    thread.start()
