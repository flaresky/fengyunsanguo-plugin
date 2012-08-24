
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

logger = Logger.getLogger()

Delay_Time = 0
Times = 0
People_List = []
local_server_diff = 0

class AttackThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def do_attack(self, people):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.attack(people)
                sanguo.close()
                if not data:
                    logger.error('attack failed. return None')
                    raise Exception()
                logger.info('attack %s succeed.'%(people))
                return data
            except:
                logger.info('do_attack failed, will sleep %d seconds'%(t*2))
                #logger.debug(traceback.format_exc())
                time.sleep(t*2)
                t += 1
    
    def run(self):
        global local_server_diff
        logger.info('AttackThread start, will attack %d times'%(Times))
        logger.info('I will attack peoples: ' + ' '.join(People_List))
        if Delay_Time > 0:
            logger.info('I will start attack at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        user = People_List[0]
        uid = PEOPLE_ID[user]
        # get user info
        next_time = 0
        ci = 1
        uinfo = util.get_user(uid)
        protectTime = int(uinfo['protectTime'])
        serverTime = int(uinfo['serverTime'])
        sp = protectTime - serverTime + 1
        logger.info('protectTime:%d'%(protectTime))
        #if int(protectTime) == 0:
        if sp < 2:
            self.do_attack(user)
            time.sleep(1)
            uinfo = util.get_user(uid)
            protectTime = int(uinfo['protectTime'])
            serverTime = int(uinfo['serverTime'])
            sp = protectTime - serverTime + 1
            ci += 1

        #server_time, local_server_diff = util.sync_time()
        #sp = util.get_sleep_time(protectTime, local_server_diff)
        logger.info('Attacked %d time, I will sleep %d seconds for next attack'%(ci-1, sp))
        time.sleep(sp)

        while ci <= Times:
            self.do_attack(user)
            if ci >= Times:
                logger.info('Attacked %d time, I will exit'%(ci))
                break
            time.sleep(1)
            uinfo = util.get_user(uid)
            protectTime = int(uinfo['protectTime'])
            serverTime = int(uinfo['serverTime'])
            sp = protectTime - serverTime + 1
            if sp < 2:
                logger.info('Not in protectTime after attack, will exit')
                break
            else:
                #sp = util.get_sleep_time(protectTime, local_server_diff)
                logger.info('Attacked %d time, I will sleep %d seconds for next attack'%(ci, sp))
                if sp < 0:
                    break
                time.sleep(sp)
            ci += 1


def parsearg():
    global Delay_Time, Times, People_List
    parser = argparse.ArgumentParser(description='Get attack')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to attack')
    parser.add_argument('-t', '--times', type=int, default=1, help='times would attack')
    parser.add_argument('-p', '--peoples', type=str, nargs='*', default=['jiange'], help='people list will attack')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Times = res.times
    People_List = res.peoples
    if not util.check_peoples(People_List):
        logger.error('People list error: ' + ' '.join(People_List))
        sys.exit()
            
if __name__ == '__main__':
    parsearg()
    thread = AttackThread()
    thread.start()
