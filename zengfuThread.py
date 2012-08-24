
import threading
from sanguo import Sanguo
import time
import sys
import Logger
import argparse
import datetime
import util
import traceback

logger = Logger.getLogger()

Local_Server_Diff = 0
Server_Time = 0

class ZengfuThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False

    def sync_time(self):
        global Local_Server_Diff
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                stime = sanguo.login()
                if not stime:
                    raise Exception()
                ltime = int(time.time())
                sanguo.close()
                Local_Server_Diff = ltime - stime
                logger.info('sync time succeed. ltime=%d stime=%d diff=%d'%(ltime, stime, Local_Server_Diff))
                return
            except:
                logger.debug(traceback.format_exc())
                time.sleep(t*2)
                t += 1
    
    def do_zengfu(self):
        logger.info('do_zengfu localtime=%d'%(int(time.time())))
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.zengfu('xinye', 'zaozilong')
                sanguo.close()
                if len(data) < 20 :
                    logger.error('zengfu failed. data len %d'%(len(data)))
                    raise Exception()
                else:
                    logger.info('zengfu succeed. data len %d'%(len(data)))
                return
            except:
                logger.info('do_zengfu failed, will sleep %d seconds'%(t*2))
                logger.debug(traceback.format_exc())
                time.sleep(t*2)
                t += 1
    
    def run(self):
        logger.info('ZengfuThread start, do server_time %d'%(Server_Time))
        if Server_Time > 0:
            self.sync_time()
            while int(time.time()) < Server_Time + Local_Server_Diff:
                st = int(Server_Time + Local_Server_Diff - int(time.time())) / 2
                if st > 0:
                    logger.info('I will sleep %d seconds'%(st))
                    time.sleep(st)
                if st > 10000:
                    self.sync_time()
        self.do_zengfu()

def parsearg():
    global Server_Time
    parser = argparse.ArgumentParser(description='Get zengfu')
    parser.add_argument('-s', '--server_time', required=False, type=str, metavar='5:0:1', help='the server time will action')
    res = parser.parse_args()
    if res.server_time:
        Server_Time = util.server_time_to_sec(res.server_time)
    else:
        Server_Time = 0
            
if __name__ == '__main__':
    parsearg()
    thread = ZengfuThread()
    thread.start()
