
import threading
from sanguo import Sanguo
import time
import sys
import Logger
import argparse
import datetime
import util
import traceback
import random

logger = Logger.getLogger()

Delay_Time = 0
Times = 0
Sleep_Time = 60 # minutes
Army_List = []

class ZuduiThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def do_zudui(self, armyid):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.zudui(armyid)
                sanguo.close()
                if len(data) < 20 :
                    logger.error('zudui failed. data len %d'%(len(data)))
                    raise Exception()
                else:
                    logger.info('zudui %s succeed. data len %d'%(armyid, len(data)))
                return
            except:
                logger.info('do_zudui failed, will sleep %d seconds'%(t*2))
                logger.debug(traceback.format_exc())
                time.sleep(t*2)
                t += 1
    
    def run(self):
        logger.info('ZuduiThread start, will zudui %d times'%(Times))
        logger.info('I will zudui armys: ' + ' '.join(Army_List))
        if Delay_Time > 0:
            logger.info('I will start zudui at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        inteval = 1
        sp = Sleep_Time - inteval * (len(Army_List) - 1)
        ci = 1
        while ci <= Times:
            for armyid in Army_List:
                self.do_zudui(armyid)
                time.sleep(inteval)
            if ci == Times:
                return
            tpsp = sp
            logger.info('sleeping %d seconds in %d time'%(tpsp, ci))
            logger.info('next zudui will at ' + util.next_time(tpsp))
            ci += 1
            if ci <= Times:
                time.sleep(tpsp)


def parsearg():
    global Delay_Time, Times, Sleep_Time, Army_List
    parser = argparse.ArgumentParser(description='Get zudui')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to zudui')
    parser.add_argument('-s', '--sleep', required=False, type=int, default=15, help='the time will sleep in each round, in minutes')
    parser.add_argument('-t', '--times', type=int, default=1, help='times would zudui')
    parser.add_argument('-a', '--armys', type=str, nargs='*', default=['wan'], help='army list will zudui')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Times = res.times
    Sleep_Time = res.sleep * 60
    Army_List = res.armys
    if not util.check_armys(Army_List):
        logger.error('Army list error: ' + ' '.join(Army_List))
        sys.exit()
            
if __name__ == '__main__':
    parsearg()
    thread = ZuduiThread()
    thread.start()
