
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
Jianzhu_List = []
Times = 0
Sleep_Time = 60 # minutes
Max_zuceng_level = 120
Auto_Upgrade_Zuceng = True # will auto upgrade zuceng if all other jianzhu is up to max level

class JianzhuThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def do_jianzhu(self, jid):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.jianzhu(jid)
                sanguo.close()
                if not data:
                    logger.error('Jianzhu %s failed.'%(jid))
                    raise Exception()
                logger.info('Jianzhu %s succeed.'%(jid))
                return data
            except:
                logger.info('do_jianzhu %s failed, will sleep %d seconds'%(jid, t*2))
                time.sleep(t*2)
                t += 1

    def get_next_jname(self, gi):
        level = gi.get_level()
        for jname in JIANZHU_LIST:
            jid = JIANZHU[jname]
            jlevel = gi.get_jianzu_level_by_jid(jid)
            if jname == 'zuceng' and jlevel < Max_zuceng_level:
                return jname
            if jlevel < level:
                return jname
        if Auto_Upgrade_Zuceng and level < Max_zuceng_level:
            return 'zuceng'
        return None

    def run(self):
        logger.info('JianzhuThread start, will do %d times'%(Times))
        #logger.info('I will jianzhu: ' + ' '.join(Jianzhu_List))
        if Delay_Time > 0:
            logger.info('I will start jianzhu at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        inteval = 30
        ci = 1
        # old
        if Times > 0:
            while ci <= Times:
                for i in range(len(Jianzhu_List)):
                    self.do_jianzhu(Jianzhu_List[i])
                    if i < len(Jianzhu_List) - 1:
                        time.sleep(inteval)
                logger.info('sleeping %d seconds in %d time'%(Sleep_Time, ci))
                logger.info('next round will at ' + util.next_time(Sleep_Time))
                ci += 1
                time.sleep(Sleep_Time)
        else:
            while True:
                # get general info
                gi = GeneralInfo()
                next_cd = gi.get_next_CDTime()
                stime = gi.get_serverTime()
                next_jname = self.get_next_jname(gi)
                sp = 0
                if not next_jname:
                    logger.info('I will send notify at server time: ' + util.next_time(gi.get_next_CDTime()-gi.get_serverTime()))
                    time.sleep(max(0, gi.get_next_CDTime() - gi.get_serverTime()))
                    logger.info('All jianzu has upgraded to max level, will exit')
                    util.notify('All jianzu has upgraded to max level')
                    break
                if next_cd > stime:
                    sp = next_cd - stime + 1
                if sp > 0:
                    logger.info('I will start upgrade %s at %s'%(next_jname, util.next_time(sp)))
                    time.sleep(sp)
                else:
                    logger.info('I will start upgrade %s now'%(next_jname))
                res = self.do_jianzhu(next_jname)
                if res.has_key('exception'):
                    msg = res['exception']['message']
                    logger.error('Got Exception "%s", will exit'%(msg))
                    if msg == 'CDTimeNotCool':
                        continue
                    elif msg == 'noBuildTeamUsable':
                        continue
                    elif msg == 'maintenance':
                        time.sleep(2000)
                        continue
                    return
                time.sleep(2)

def parsearg():
    global Delay_Time, Jianzhu_List, Times, Sleep_Time
    default_sleep = 15
    parser = argparse.ArgumentParser(description='Jianzhu')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay before first round')
    parser.add_argument('-s', '--sleep', required=False, type=int, default=default_sleep, help='the time will sleep in each round, default is %d minutes'%(default_sleep))
    parser.add_argument('-t', '--times', type=int, default=0, help='times would upgrade jianzhu')
    parser.add_argument('-j', '--jids', type=str, nargs='*', default=['yinku'], help='jid list will upgrade')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Jianzhu_List = res.jids
    Times = res.times
    Sleep_Time = res.sleep * 60
    if not util.check_jianzhu(Jianzhu_List):
        logger.error('jid list error: ' + ' '.join(Jianzhu_List))
        sys.exit()
            
if __name__ == '__main__':
    parsearg()
    thread = JianzhuThread()
    thread.start()
