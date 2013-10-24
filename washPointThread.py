
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
Max_Mean = 40
Hero= None
Orig_Point = None
fields = ('leadership', 'tactics', 'magic')
temp_fields = ('tempLeadership', 'tempTactics', 'tempMagic')

class WashPointThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False

    def get_harmonic_mean(self, args):
        sum = 0
        for v in args:
            v = int(v)
            if v == 0:
                v = 0.1
            sum += 1.0 / v
        return 1.0 / sum

    def run(self):
        logger.info('WashPointThread start, hero is %s'%(Hero))
        if Hero is None:
            return
        if Delay_Time > 0:
            logger.info('I will start training at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        print_old_point = True
        fields_num = 3
        while True:
            try:
                wash_res = util.send_command('washHero', Hero)
                if wash_res.has_key('exception'):
                    logger.error('Got exception %s, exit'%(wash_res['exception']['message']))
                    return
                hero = wash_res['hero']
                oldfs = [int(hero[i]) for i in fields]
                oldfs = [oldfs[i]-Orig_Point[i] for i in range(fields_num)]
                oldmean = self.get_harmonic_mean(oldfs)
                tmpfs = [int(hero[i]) for i in temp_fields]
                tmpfs = [tmpfs[i]-Orig_Point[i] for i in range(fields_num)]
                tmpmean = self.get_harmonic_mean(tmpfs)
                if print_old_point:
                    msg = ['%s=%d'%(fields[i], oldfs[i]) for i in range(fields_num)]
                    msg.append('mean=%.4f'%(oldmean))
                    msg = ', '.join(msg)
                    logger.info(msg)
                msg = ['%s=%d'%(temp_fields[i], tmpfs[i]) for i in range(fields_num)]
                msg.append('mean=%.4f'%(tmpmean))
                msg = ', '.join(msg)
                accepted = tmpmean >= oldmean
                if accepted:
                    msg = '[Accept] ' + msg
                else:
                    msg = '[Refuse] ' + msg
                logger.info(msg)
                curmean = 50
                if accepted:
                    util.send_command('acceptWash', Hero)
                    print_old_point = True
                    curmean = tmpmean
                else:
                    util.send_command('refuseWash', Hero)
                    print_old_point = False
                    curmean = oldmean
                if curmean >= Max_Mean:
                    logger.info('current mean is %.4f, will exit', curmean)
                    return
            except:
                logger.error(traceback.format_exc())
                time.sleep(2)

def parsearg():
    global Delay_Time, Hero, Max_Mean, Orig_Point
    parser = argparse.ArgumentParser(description='WashPoint for hero')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to training')
    parser.add_argument('-e', '--hero', type=str, help='hero you want to wash point')
    parser.add_argument('-i', '--init_point', type=int, nargs=3, help='hero init points, eg. 90 90 100')
    parser.add_argument('-m', '--max_mean', type=int, default=40, help='max harmonic mean')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Hero= res.hero
    Max_Mean = res.max_mean
    Orig_Point = res.init_point
    if len(Orig_Point) != 3:
        sys.exit()
            
if __name__ == '__main__':
    parsearg()
    thread = WashPointThread()
    thread.start()
