#!/usr/local/bin/python
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
import random
from settings import *
from GeneralInfo import GeneralInfo
import json
import traceback

logger = Logger.getLogger()

Delay_Time = 0
Times = 0
People_List = []
local_server_diff = 0

class LanjieThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def do_lanjie(self, people):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.lanjie(people)
                sanguo.close()
                if not data:
                    logger.error('lanjie failed. return None')
                    raise Exception()
                logger.info('lanjie %s succeed.'%(people))
                return data
            except:
                logger.info('do_lanjie failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1
    
    def get_husong_list(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.husong_list()
                sanguo.close()
                if not data:
                    raise Exception()
                return data
            except:
                logger.info('husong_list failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1

    def suaxin_husong_list(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.husong_suaxin()
                sanguo.close()
                if not data:
                    raise Exception()
                return data
            except:
                logger.info('husong_suaxin failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1

    def find_lanjie_target(self, viewlist, servertime):
        min_reward = 36
        min_beautyId = 5
        for view in viewlist:
            isnpc = int(view['isNPC'])
            reward = int(view['blockReward'])
            beautyId = int(view['beautyId'])
            startTime = int(view['startTime'])
            endTime = int(view['endTime'])
            if isnpc == 1 and beautyId >= min_beautyId and reward >= min_reward and startTime <= servertime and servertime <= endTime:
                #print json.dumps(view, sort_keys = False, indent = 4)
                logger.info('Will lanjie %s'%(view['userName']))
                return view['id'] 
        return None
    
    def run(self):
        while True:
            try:
                hlist = self.get_husong_list()
                serverTime = int(hlist['serverTime'])
                maxBlockTimes = int(hlist['userConvoyStatus']['maxBlockTimes'])
                blockTimes = int(hlist['userConvoyStatus']['blockTimes'])
                logger.info('blockTimes %d, maxBlockTimes %d'%(blockTimes, maxBlockTimes))
                if blockTimes >= maxBlockTimes:
                    logger.info('Reach maxBlockTimes %d, will exit'%(maxBlockTimes))
                    return
                find = self.find_lanjie_target(hlist['userConvoyStatus']['viewOtherConvoy'], serverTime)
                time.sleep(4)
                if find is not None:
                    res = self.do_lanjie(find)

                # get suaxin cd
                gi = GeneralInfo()
                lanjiecd = max(
                                gi.get_husong_suaxin_CDTime(),
                                gi.get_block_CDTime()
                              )
                if lanjiecd <> 0:
                    sp = lanjiecd - gi.get_serverTime() + 1
                    sp = max(sp , 0)
                    logger.info('sleep cd, will start at %s'%(util.next_time(sp)))
                    time.sleep(sp)
                else:
                    time.sleep(2)

                # suaxin
                logger.info('suaxin husong list')
                self.suaxin_husong_list()
                time.sleep(2)
            except:
                logger.error(traceback.format_exc())
                time.sleep(1200)

def parsearg():
    global Delay_Time, Times, People_List
    parser = argparse.ArgumentParser(description='Get lanjie')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to lanjie')
    parser.add_argument('-t', '--times', type=int, default=1, help='times would lanjie')
    parser.add_argument('-p', '--peoples', type=str, nargs='*', default=['cenyufeng'], help='people list will lanjie')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Times = res.times
    People_List = res.peoples
            
if __name__ == '__main__':
    parsearg()
    thread = LanjieThread()
    thread.start()
