
import threading
from sanguo import Sanguo
import time
import Logger
import argparse
import datetime
import util
import sys
from GeneralInfo import GeneralInfo
from settings import *

logger = Logger.getLogger()

Delay_Time = 0
CityName = 'xinye'
Thrive = 3

class TouziThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def do_touzi(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.touzi(CITY_ID[CityName], Thrive)
                sanguo.close()
                if not data:
                    logger.error('Touzi %s failed.'%(CityName))
                    raise Exception()
                logger.info('Touzi %s succeed.'%(CityName))
                return data
            except:
                logger.info('do_touzi %s failed, will sleep %d seconds'%(CityName, t*2))
                time.sleep(t*2)
                t += 1

    def run(self):
        logger.info('TouziThread start')
        if Delay_Time > 0:
            logger.info('I will start touzi at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)

        times = 0
        while True:
            try:
                gi = GeneralInfo()
                next_touzi_cd = gi.get_touzi_CDTime()
                stime = gi.get_serverTime()
                sp = 0
                if next_touzi_cd > stime:
                    sp = next_touzi_cd - stime + 1
                if sp > 0:
                    logger.info('I will start touzi %s at %s'%(CityName, util.next_time(sp)))
                    time.sleep(sp)
                else:
                    logger.info('I will start touzi %s now'%(CityName))

                res = self.do_touzi()
                if res.has_key('exception'):
                    msg = res['exception']['message']
                    logger.error('Got Exception "%s", will exit'%(msg))
                    if msg == 'CDTimeNotCool':
                        continue
                    elif msg == 'in invest CD':
                        continue
                    time.sleep(3600)
                    continue
                times += 1
                logger.info('Succeed touzi %d times'%(times))
            except:
                import traceback
                logger.error(traceback.format_exc())
                time.sleep(100)

def parsearg():
    global Delay_Time, CityName, Thrive
    parser = argparse.ArgumentParser(description='touzi')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to upgrade touzi')
    parser.add_argument('-c', '--city', type=str, default='bajun', help='touzi city name')
    parser.add_argument('-t', '--thrive', type=int, default=3, help='thrive')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    CityName = res.city
    Thrive = res.thrive
            
if __name__ == '__main__':
    parsearg()
    thread = TouziThread()
    thread.start()
