
import threading
from sanguo import Sanguo
import time
import Logger
import argparse
import datetime
import util
import sys

logger = Logger.getLogger()

Delay_Time = 0
Plantation_List = []
Enter = False
Soukuang = False

class KuangzanThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def do_enter(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.kuangzan()
                sanguo.close()
                if not data:
                    logger.error('Enter kuangzan failed. data None')
                    raise Exception()
                logger.info('Enter kuangzan succeed.')
                return data
            except:
                logger.info('do_enter failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1

    def run(self):
        logger.info('KuangzanThread start')
        if Delay_Time > 0:
            logger.info('I will start at ' + next_time(Delay_Time))
            time.sleep(Delay_Time)
        if Enter:
            self.do_enter()

def parsearg():
    global Delay_Time, Plantation_List, Enter, Soukuang
    parser = argparse.ArgumentParser(description='Kuangzan')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay before first round')
    parser.add_argument('-e', '--enter', action='store_true', default=True, help='enter plantation')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Enter = res.enter
            
if __name__ == '__main__':
    parsearg()
    thread = KuangzanThread()
    thread.start()
