
import threading
import argparse
from sanguo import Sanguo
import time
import Logger
import util
import traceback

logger = Logger.getLogger()

Times = 0
Delay_Time = 0
Hero = None

class TufeiThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def do_tufei(self, hero):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.tufei(hero)
                sanguo.close()
                if not data:
                    logger.error('Tufei %s failed.'%(hero))
                    raise Exception()
                logger.info('tufei %s succeed'%(hero))
                return data
            except:
                t += 1
                logger.info('do_tufei failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
    
    def run(self):
        logger.info('Tufei Thread start, will tufei %s %d times'%(Hero, Times))
        if Delay_Time > 0:
            logger.info('I will start tufei at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        sp = 598
        cnt = 1
        while True:
            try:
                idx = (cnt-1) % len(Hero)
                self.do_tufei(Hero[idx])
                logger.info('sleeping %d seconds in %d time'%(sp, cnt))
                if cnt >= Times:
                    return
                cnt += 1
                time.sleep(sp)
            except:
                logger.info(traceback.format_exc())
                time.sleep(sp)

def parsearg():
    global Times, Hero, Delay_Time
    parser = argparse.ArgumentParser(description='Get tax')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to upgrade keji')
    parser.add_argument('-t', '--times', required=False, type=int, default=50000, help='tufei times')
    parser.add_argument('-e', '--hero', required=True, type=str, nargs='*', default=['zuge'], help='tufei hero list')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Times = res.times
    Hero = res.hero
    if not util.check_heroes(Hero):
        logger.error('Hero list error: ' + ' '.join(Hero))
        sys.exit()
            
if __name__ == '__main__':
    parsearg()
    if Hero:
        tufeithread = TufeiThread()
        tufeithread.start()
