
import threading
from sanguo import Sanguo
import time
import Logger
import argparse
import datetime
import util
import sys
from KejiInfo import KejiInfo
from GeneralInfo import GeneralInfo
from settings import *

logger = Logger.getLogger()

Delay_Time = 0
Kid_List = []
Times = 0
Sleep_Time = 60 # minutes

class KejiThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def do_keji(self, kid):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.keji(kid)
                sanguo.close()
                if not data:
                    logger.error('Keji %s failed.'%(kid))
                    raise Exception()
                logger.info('Keji %s succeed.'%(kid))
                return data
            except:
                logger.info('do_keji %s failed, will sleep %d seconds'%(kid, t*2))
                time.sleep(t*2)
                t += 1

    def get_next_kname(self, gi, ki):
        level = gi.get_jianzu_level_by_jid('103')
        for kname, level_step in KEJI_LIST:
            kid = KEJI[kname]
            jlevel = ki.get_level_by_kid(kid)
            if jlevel < int(level / level_step):
                return kname
        return None

    def run(self):
        logger.info('KejiThread start, will do %d times'%(Times))
        #logger.info('I upgrade keji: ' + ' '.join(Kid_List))
        if Delay_Time > 0:
            logger.info('I will start keji at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        inteval = 30
        ci = 1
        if Times > 0:
            while ci <= Times:
                for i in range(len(Kid_List)):
                    self.do_keji(Kid_List[i])
                    if i < len(Kid_List) - 1:
                        time.sleep(inteval)
                if ci == Times:
                    break
                logger.info('sleeping %d seconds in %d time'%(Sleep_Time, ci))
                logger.info('next round will at ' + util.next_time(Sleep_Time))
                ci += 1
                time.sleep(Sleep_Time)
        else:
            while True:
                # get general info
                gi = GeneralInfo()
                ki = KejiInfo()
                next_keji_cd = gi.get_next_keji_CDTime()
                stime = gi.get_serverTime()
                next_kname = self.get_next_kname(gi, ki)
                sp = 0
                if not next_kname:
                    logger.info('I will send notify at server time: ' + util.next_time(gi.get_next_keji_CDTime() - gi.get_serverTime()))
                    time.sleep(gi.get_next_keji_CDTime() - gi.get_serverTime())
                    logger.info('All keji has upgraded to max level, will exit')
                    util.notify('All keji has upgraded to max level')
                    break
                if next_keji_cd > stime:
                    sp = next_keji_cd - stime + 1
                if sp > 0:
                    logger.info('I will start upgrade %s at %s'%(next_kname, util.next_time(sp)))
                    time.sleep(sp)
                else:
                    logger.info('I will start upgrade %s now'%(next_kname))
                res = self.do_keji(next_kname)
                if res.has_key('exception'):
                    msg = res['exception']['message']
                    logger.error('Got Exception "%s", will exit'%(msg))
                    if msg == 'CDTimeNotCool':
                        continue
                    return
                time.sleep(2)

def parsearg():
    global Delay_Time, Kid_List, Times, Sleep_Time
    parser = argparse.ArgumentParser(description='upgrade keji')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to upgrade keji')
    parser.add_argument('-s', '--sleep', required=False, type=int, default=60, help='the time will sleep in each round, in minutes')
    parser.add_argument('-t', '--times', type=int, default=0, help='times would do')
    parser.add_argument('-k', '--kids', type=str, nargs='*', default=['hudun'], help='kid list will upgrade')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Kid_List = res.kids
    Times = res.times
    Sleep_Time = res.sleep * 60
    if not util.check_keji(Kid_List):
        logger.error('kid list error: ' + ' '.join(Kid_List))
        sys.exit()
            
if __name__ == '__main__':
    parsearg()
    thread = KejiThread()
    thread.start()
