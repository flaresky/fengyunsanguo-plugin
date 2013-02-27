#!/usr/bin/python
#encoding: utf-8
import threading
from sanguo import Sanguo
import time
import Logger
import argparse
import datetime
import util
import sys
import json

logger = Logger.getLogger()

Delay_Time = 0
Get = False

class huodongThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def print_info(self):
        data = {
                'op' : 1323,
            }
        res = util.send_data(data, 'integral')
        #print json.dumps(res, sort_keys = False, indent = 4)
        print 'Order: %d'%(res.get('order',0) or 0)
        print 'Integral: %s'%(res['integral'])
        print 'Award: %d'%(res['award'])
        print 'IsGet: %s'%('True' if res['isGet']=='1' else 'False')
        print 'ServerTime: %s'%(util.format_time(res['serverTime']))
        print 'EndTime: %s'%(util.format_time(res['endTime']))
        print 'OrderList:'
        for pp in res['orderList'] or []:
            print '\tOrder:%d\tIntegle:%s\tName:%s'%(pp['order'], pp['integle'], pp['userName'])

    def get_money(self):
        data = {
                'op' : 1325,
            }
        res = util.send_data(data)
        logger.info('Got huodong money')
        return res

    def run(self):
        logger.info('huodongThread start')
        if Delay_Time > 0:
            logger.info('I will start at ' + next_time(Delay_Time))
            time.sleep(Delay_Time)
        self.print_info()
        if Get:
            self.get_money()

def parsearg():
    global Delay_Time, Get
    parser = argparse.ArgumentParser(description='huodong')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay before first round')
    parser.add_argument('-g', '--get', action='store_true', help='get money')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Get = res.get
            
if __name__ == '__main__':
    parsearg()
    thread = huodongThread()
    thread.start()
