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
                    raise Exception()
                logger.info('Upgrade %s succeed'%(eid))
                return data
            except:
                time.sleep(2)
                t += 1

    def do_degrade(self, eid):
        data = {
                'op' : 1005,
                'id' : str(eid),
            }
        res = util.send_data(data)
        logger.info('degrade %s succeed'%(eid))

    def run(self):
        logger.info('suapaiming start, will upgrade %d times'%(Times))
        if Delay_Time > 0:
            logger.info('I will start upgrade at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        while True:
            ei = EquipInfo()
            magic = ei.get_magic_value()
            logger.info('magic is %d'%(magic))
            if magic > 71:
                goldnum = ei.get_magic_needgold()
                res = self.do_upgrade(Eid, magic)
                self.do_degrade(Eid)
                time.sleep(278)
            else:
                time.sleep(598)

def parsearg():
    global Delay_Time, Times, Ename, Eid, NeedGold, Auto_Upgrade
    parser = argparse.ArgumentParser(description='upgrade equip')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay')
    parser.add_argument('-n', '--equip_name', required=False, type=str, help='equip name')
    parser.add_argument('-i', '--equip_id', required=False, type=str, default='642951', help='equip id')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Ename = res.equip_name
    Eid = res.equip_id

if __name__ == '__main__':
    parsearg()
    thread = UpgradeThread()
    thread.start()
