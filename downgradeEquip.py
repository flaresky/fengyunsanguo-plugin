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

class downgradeThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def do_downgrade(self, eid):
        retry = 10
        t = 1 
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.downgradeEquip(eid)
                sanguo.close()
                if not data:
                    logger.error('downgrade failed, data None')
                    raise Exception()
                #logger.info('downgrade succeed')
                return data
            except:
                logger.info('do_downgrade failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1

    def run(self):
        logger.info('downgradeThread start, will downgrade %d times'%(Times))
        if Delay_Time > 0:
            logger.info('I will start downgrade at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        if int(Eid) < 0:
            ei = EquipInfo()
            #logger.info('get %d equips'%(len(ei.get_equip_ids())))
            for eid in ei.get_equip_ids():
                level = ei.get_level_by_id(eid)
                star = ei.get_starLevel_by_id(eid)
                if level > star:
                    logger.info('Downgrade equip %s'%(eid))
                    exception = ""
                    for i in range(int(level)):
                        res = self.do_downgrade(eid)
                        if res.has_key('exception'):
                            logger.info('got Exception %s'%(res['exception']['message']))
                            exception = res['exception']['message']
                            #sys.exit()
                            break
                        logger.info('Downgrade %d times'%(i+1))
                        time.sleep(2)
                    if exception == 'beyondMaxSilver':
                        logger.info('Exit for Exception %s'%(exception))
                        break
        else:
            for i in range(Times):
                res = self.do_downgrade(Eid)
                if res.has_key('exception'):
                    logger.info('Exit for Exception %s'%(res['exception']['message']))
                    break
                logger.info('Downgrade %d times'%(i+1))
                time.sleep(2)

def parsearg():
    global Delay_Time, Times, Eid
    parser = argparse.ArgumentParser(description='downgrade equip')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay')
    parser.add_argument('-i', '--equip_id', required=False, type=str, default='471179', help='equip id')
    parser.add_argument('-t', '--times', required=False, type=int, default=1, help='downgrade times')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Times = res.times
    Eid = res.equip_id

if __name__ == '__main__':
    parsearg()
    thread = downgradeThread()
    thread.start()
