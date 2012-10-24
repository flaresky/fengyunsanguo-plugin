
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
Times = 6
Plantation_List = []

class SoukuangThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def do_soukuang(self, pid):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.soukuang(pid)
                sanguo.close()
                if not data:
                    logger.error('soukuang %s failed.'%(pid))
                    raise Exception()
                logger.info('soukuang %s succeed. data len %d'%(pid, len(data)))
                return data
            except:
                logger.info('do_soukuang failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1

    def run(self):
        logger.info('SoukuangThread start, will soukuang %d times'%(Times))
        if Delay_Time > 0:
            logger.info('I will start at ' + next_time(Delay_Time))
            time.sleep(Delay_Time)
        inteval = 3
        for pid in Plantation_List:
            for st in range(Times):
                res = self.do_soukuang(pid)
                if res.has_key('exception'):
                    logger.info('soukuang exception: %s, will exit'%(res['exception']['message']))
                    break
                if st < Times - 1:
                    time.sleep(inteval)

def parsearg():
    global Delay_Time, Plantation_List, Times
    parser = argparse.ArgumentParser(description='Kuangzan')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay before first round')
    parser.add_argument('-p', '--plantations', type=str, nargs='*', default=['yuzou'], help='plantation id will soukuang')
    parser.add_argument('-t', '--times', type=int, default=10, help='soukuang times')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Plantation_List = res.plantations
    Times = res.times
            
if __name__ == '__main__':
    parsearg()
    thread = SoukuangThread()
    thread.start()
