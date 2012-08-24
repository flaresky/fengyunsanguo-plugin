#!/usr/bin/python
import threading
from sanguo import Sanguo
import time
import sys
import Logger
import argparse
import datetime
import util
import traceback
from EmailSender import EmailSender
from GeneralInfo import GeneralInfo

logger = Logger.getLogger()

Local_Server_Diff = 0
Server_Time = 0
Min_Magic = 98

class MagicThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False

    def get_next_half_hour(self):
        global Server_Time
        last_time = datetime.datetime.fromtimestamp(Server_Time)
        logger.info('last server time is %s'%(str(last_time)))
        if last_time.minute < 30:
            last_time = last_time.replace(minute=30, second=1)
        else:
            last_time = last_time + datetime.timedelta(hours=1)
            last_time = last_time.replace(minute=0, second=1)
        logger.info('next half hour is %s'%(str(last_time)))
        Server_Time = int(time.mktime(last_time.timetuple())) 

    def notify(self, magic):
        if magic >= Min_Magic:
            title = 'Magic Value is %d%%'%(magic)
            util.notify(title)
    
    def run(self):
        global Local_Server_Diff,Server_Time
        logger.info('MagicThread start')
        while True:
            try:
                gi = GeneralInfo()
                Server_Time = gi.get_serverTime()
                Local_Server_Diff = gi.get_localTime() - Server_Time
                #logger.info('Server_Time=%d Local_Server_Diff=%d'%(Server_Time, Local_Server_Diff))
                magic = int(gi.get_magic())
                logger.info('get magic=%d'%(magic))
                self.notify(magic)
                self.get_next_half_hour()
                sp = Server_Time + Local_Server_Diff - int(time.time()) + 60
                logger.info('I will sleep %d seconds'%(sp))
                time.sleep(sp)
            except:
                logger.error(traceback.format_exc())
                time.sleep(60)

def parsearg():
    global Min_Magic
    parser = argparse.ArgumentParser(description='Get magic')
    parser.add_argument('-m', '--magic', required=False, type=int, default=95, help='the min magic will notify')
    res = parser.parse_args()
    Min_Magic = res.magic
            
if __name__ == '__main__':
    parsearg()
    thread = MagicThread()
    thread.start()
