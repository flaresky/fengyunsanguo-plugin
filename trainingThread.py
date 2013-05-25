
import threading
from sanguo import Sanguo
import time
import Logger
import argparse
import datetime
import util
import sys
import traceback
from settings import *
from HeroInfo import HeroInfo
import traceback

logger = Logger.getLogger()

Delay_Time = 0
Max_Level = 0
Hero_List = []
Auto_Rebirth = False
Hour = 2

def get_time_by_level(level):
    try:
        return LEVEL_EXP_MAP[level]
    except:
        return 0

class TrainingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False
    
    def rebirth(self, hero):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.zhuanshen(hero)
                sanguo.close()
                if not data:
                    logger.error('rebirth failed.')
                    raise Exception()
                if data.has_key('exception'):
                    logger.error('rebirth got exception: ' + data['exception']['message'])
                else:
                    logger.info('rebirth %s succeed. data len %d'%(hero, len(data)))
                return data
            except:
                #logger.error(traceback.format_exc())
                logger.info('rebirth %s failed, will sleep %d seconds'%(hero, t*2))
                time.sleep(t*2)
                t += 1
    
    def do_training(self, hero):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.training(hero, Hour)
                sanguo.close()
                if not data:
                    logger.error('Training failed.')
                    raise Exception()
                if data.has_key('exception'):
                    logger.error('Training got exception: ' + data['exception']['message'])
                else:
                    logger.info('Training %s succeed. data len %d'%(hero, len(data)))
                return data
            except:
                #logger.error(traceback.format_exc())
                logger.info('do_training %s failed, will sleep %d seconds'%(hero, t*2))
                time.sleep(t*2)
                t += 1

    def run(self):
        global Max_Level
        logger.info('TrainingThread start, Max_Level is %d'%(Max_Level))
        logger.info('I will training heroes: ' + ' '.join(Hero_List))
        if Delay_Time > 0:
            logger.info('I will start training at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        inteval = 100
        sp = 7200 - (len(Hero_List)-1) * inteval + 2 * len(Hero_List)
        cnt = 1
        while True:
            tpsp = sp
            for i in range(len(Hero_List)):
                self.do_training(Hero_List[i])
                try:
                    # get hero info
                    hid = UID[Hero_List[i]]
                    hi = HeroInfo()
                    level = int(hi.get_level_by_id(hid))
                    next_rebirth_level = int(hi.get_nextrebirthlevel_by_id(hid))
                    name = hi.get_name_by_id(hid)
                    trainingEndTime = int(hi.get_trainingEndTime_by_id(hid))
                    nextUpgrade = int(hi.get_nextUpgrade_by_id(hid))
                    serverTime = int(hi.data['serverTime'])
                    localTime = hi.local_time
                    max_level = Max_Level
                    if max_level <= 0 :
                        max_level = next_rebirth_level
                    if level >= int(hi.get_maxLevel_by_id(hid)):
                        msg = 'Hero %s already reach maxLevel %d, will exit'%(name, level)
                        logger.info(msg)
                        util.notify(msg)
                        return
                    if level >= max_level:
                        if Auto_Rebirth:
                            self.rebirth(Hero_List[i])
                            msg = 'Hero %s already reach maxLevel %d, will rebirth'%(name, level)
                            logger.info(msg)
                            util.notify(msg)
                        else:
                            msg = 'Hero %s already reach maxLevel %d, will exit'%(name, level)
                            logger.info(msg)
                            util.notify(msg)
                            return
                    else:
                        total_exp = 0
                        for l in range(level, max_level):
                            total_exp += get_time_by_level(l)
                        total_exp -= hi.calc_cur_exp_by_id(hid)
                        exp_speed = hi.get_exp_speed_by_id(hid)
                        army = int(hi.get_currUnit_by_id(hid))
                        t = total_exp / float(exp_speed)
                        msg = 'Hero %s current level %d, army %d, max level %d, '%(name, level, army, max_level)
                        if t > 24: 
                            d = int(t / 24) 
                            h = t - 24 * d 
                            msg = msg + 'still need %d days %.1f hours'%(d, h)
                        else:
                            msg = msg + 'still need %.1f hours'%(t)
                        logger.info(msg)
                    if level == max_level - 1:
                        if trainingEndTime > nextUpgrade:
                            logger.info('Hero %s will reach level %d in the end of this round'%(name, max_level))
                            sp = util.get_sleep_time(nextUpgrade, localTime-serverTime)
                            time.sleep(sp)
                            if Auto_Rebirth:
                                self.rebirth(Hero_List[i])
                                msg = 'Hero %s already reach maxLevel %d, do rebirth'%(name, level+1)
                                logger.info(msg)
                                util.notify(msg)
                            else:
                                msg = 'Hero %s already reach maxLevel %d'%(name, level+1)
                                logger.info(msg)
                                util.notify(msg)
                            tpsp = trainingEndTime - nextUpgrade + 1
                            continue
                    tpsp = trainingEndTime - serverTime + 1
                except:
                    logger.error(traceback.format_exc())
                if i < len(Hero_List) - 1:
                    time.sleep(inteval)
            logger.info('sleeping %d seconds in %d time'%(tpsp, cnt))
            logger.info('next round will start at ' + util.next_time(tpsp))
            cnt += 1
            time.sleep(max(tpsp, 0))

def parsearg():
    global Delay_Time, Hero_List, Max_Level, Auto_Rebirth, Hour
    parser = argparse.ArgumentParser(description='Training heroes')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to training')
    parser.add_argument('-e', '--heroes', type=str, nargs='*', default=['xusu', 'yuanshao', 'sunsangxiang'], help='hero list will training')
    parser.add_argument('-l', '--max_level', required=False, type=int, default=0, metavar=81 , help='if hero reach max level, will exit training')
    parser.add_argument('-a', '--auto_rebirth', required=False, action='store_true', help='auto rebirth mode')
    parser.add_argument('-m', '--hour_mode', type=int, default=8, help='training hour mode')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Hero_List = res.heroes
    Max_Level = res.max_level
    if not util.check_heroes(Hero_List):
        logger.error('Hero list error: ' + ' '.join(Hero_List))
        sys.exit()
    Auto_Rebirth = res.auto_rebirth
    Hour = res.hour_mode
            
if __name__ == '__main__':
    parsearg()
    thread = TrainingThread()
    thread.start()
