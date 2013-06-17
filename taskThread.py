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

logger = Logger.getLogger()

Delay_Time = 0 
Times = 0 
MaxSilverExit = False

class TaskThread(threading.Thread):
    def __init__(self, count=18):
        threading.Thread.__init__(self)
        self.daemon = False
        self.count = count
    
    def get_task_list(self):
        retry = 10
        t = 1 
        timeout = 2
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.task_list(timeout+t)
                sanguo.close()
                if not data:
                    #logger.error('get_task_list failed, data None')
                    raise Exception()
                logger.info('get_task_list succeed')
                return data
            except:
                logger.info('get_task_list failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1

    def task_reward(self, ei):
        retry = 10
        t = 1 
        eid = ei['id']
        title = ei['title']
        directions = ei['directions']
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.task_reward(eid)
                sanguo.close()
                if not data:
                    #logger.error('get_task_list failed, data None')
                    raise Exception()
                logger.info('reward %s succeed: %s %s'%(str(eid), title, directions))
                return data
            except:
                logger.info('reward %s failed, will sleep %d seconds'%(str(eid), t*2))
                time.sleep(t*2)
                t += 1

    def run(self):
        logger.info('TaskThread start')
        if Delay_Time > 0:
            logger.info('I will start task at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        task_list = self.get_task_list()
        #print json.dumps(task_list['eventInfos'], sort_keys = False, indent = 4)
        for ei in task_list['eventInfos']:
            if ei['isfinish']:
                time.sleep(2)
                self.task_reward(ei)

def parsearg():
    global Delay_Time, Times, MaxSilverExit
    parser = argparse.ArgumentParser(description='Get task')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to task')
    parser.add_argument('-x', '--exit', required=False, action='store_true', help='exit when beyondMaxSilver')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    MaxSilverExit = res.exit

if __name__ == '__main__':
    parsearg()
    thread = TaskThread()
    thread.start()
