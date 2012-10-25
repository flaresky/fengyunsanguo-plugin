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
Ename = None
Eid = None
NeedGold = None
Auto_Upgrade = None

class UpgradeThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def do_upgrade(self, eid, magic, buymagic=0):
        retry = 10
        t = 1 
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.upgradeEquip(eid, magic, buymagic)
                sanguo.close()
                if not data:
                    logger.error('Upgrade failed, data None')
                    raise Exception()
                logger.info('Upgrade succeed')
                return data
            except:
                logger.info('do_upgrade failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1

    def run(self):
        logger.info('UpgradeThread start, will upgrade %d times'%(Times))
        if Delay_Time > 0:
            logger.info('I will start upgrade at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        ei = EquipInfo()
        magic = ei.get_magic_value()
        goldnum = ei.get_magic_needgold()
        def shengji(times):
            for i in range(times):
                time.sleep(2)
                if NeedGold:
                    res = self.do_upgrade(Eid, magic, goldnum)
                else:
                    res = self.do_upgrade(Eid, magic)
                if res.has_key('exception'):
                    msg = res['exception']['message']
                    if msg == 'equipIsPiece':
                        logger.info('exit for equipIsPiece')
                    elif msg == 'maxEquipLevel':
                        logger.info('exit for maxEquipLevel')
                    elif msg == 'CDTimeNotCool':
                        logger.info('exit for CDTimeNotCool')
                    else:
                        logger.info('exit for %s'%(res['exception']['message']))
                    raise Exception(msg)
        if Auto_Upgrade:
            try:
                logger.info('auto mode, upgrade 4 times')
                shengji(4)
                sp = 1205
                logger.info('I will start upgrade 3 times at ' + util.next_time(sp))
                time.sleep(sp)
                shengji(3)
                sp = 305
                logger.info('I will start upgrade 2 times at ' + util.next_time(sp))
                time.sleep(sp)
                shengji(2)
            except:
                return
        else:
            try:
                shengji(Times)
            except:
                return

def parsearg():
    global Delay_Time, Times, Ename, Eid, NeedGold, Auto_Upgrade
    parser = argparse.ArgumentParser(description='upgrade equip')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay')
    parser.add_argument('-n', '--equip_name', required=False, type=str, help='equip name')
    parser.add_argument('-i', '--equip_id', required=False, type=str, default='1130008', help='equip id')
    parser.add_argument('-t', '--times', required=False, type=int, default=1, help='upgrade times')
    parser.add_argument('-g', '--needgold', required=False, action='store_true', help='use gold to upgrade')
    parser.add_argument('-a', '--auto_upgrade', required=False, action='store_true', help='auto upgrade mode')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Times = res.times
    Ename = res.equip_name
    Eid = res.equip_id
    NeedGold = res.needgold
    Auto_Upgrade = res.auto_upgrade

if __name__ == '__main__':
    parsearg()
    thread = UpgradeThread()
    thread.start()
