
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
Max_Mean = 0
Hero = None
Weight = None
fields = ('leadership', 'tactics', 'magic')
temp_fields = ('tempLeadership', 'tempTactics', 'tempMagic')

class WashPointThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False

    def get_harmonic_mean(self, args):
        fields_num = 3
        sum = 0
        fs = 0
        for i in range(fields_num):
            v = int(args[i])
            if v == 0:
                v = 0.1
            sum += 1.0 * Weight[i] / v
            fs += Weight[i]
        return 1.0 * fs / sum

    def run(self):
        logger.info('WashPointThread start, hero is %s'%(Hero))
        if Hero is None:
            return
        if not UID.has_key(Hero):
            logger.error('can not found %s in UID'%(Hero))
            return
        if not INIT_POINT.has_key(Hero):
            logger.error('can not found %s in INIT_POINT'%(Hero))
            return
        if Delay_Time > 0:
            logger.info('I will start training at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        print_old_point = True
        fields_num = 3
        times = 0
        accepted = False
        while True:
            try:
                wash_res = util.send_command('washHero', Hero)
                if wash_res.has_key('exception'):
                    exp = wash_res['exception']['message']
                    if exp == 'previousChangPointNotFinish':
                        if accepted:
                            flag = 'Accept'
                        else:
                            flag = 'Refuse'
                        logger.info('Repost[%s]'%(flag))
                        time.sleep(2)
                        if accepted:
                            util.send_command('acceptWash', Hero)
                            print_old_point = True
                        else:
                            util.send_command('refuseWash', Hero)
                            print_old_point = False
                        time.sleep(2)
                        continue
                    logger.error('Got exception %s, exit'%(exp))
                    return
                times += 1
                hero = wash_res['hero']
                oldfs = [int(hero[i]) for i in fields]
                oldfs = [oldfs[i]-INIT_POINT[Hero][i] for i in range(fields_num)]
                oldmean = self.get_harmonic_mean(oldfs)
                tmpfs = [int(hero[i]) for i in temp_fields]
                tmpfs = [tmpfs[i]-INIT_POINT[Hero][i] for i in range(fields_num)]
                tmpmean = self.get_harmonic_mean(tmpfs)
                if print_old_point:
                    msg = ['%s=%d'%(fields[i], oldfs[i]) for i in range(fields_num)]
                    msg.append('mean=%.4f'%(oldmean))
                    msg = ', '.join(msg)
                    logger.info(msg)
                msg = ['%s=%d'%(temp_fields[i], tmpfs[i]) for i in range(fields_num)]
                msg.append('mean=%.4f'%(tmpmean))
                msg = ', '.join(msg)
                accepted = False
                if tmpmean >= oldmean:
                    accepted = True
                if accepted:
                    msg = '[Accept][' + str(times) + '] ' + msg
                else:
                    msg = '[Refuse][' + str(times) + '] ' + msg
                logger.info(msg)
                curmean = 50
                if accepted:
                    time.sleep(3)
                    util.send_command('acceptWash', Hero)
                    print_old_point = True
                    curmean = tmpmean
                else:
                    time.sleep(2)
                    util.send_command('refuseWash', Hero)
                    print_old_point = False
                    curmean = oldmean
                if curmean >= Max_Mean:
                    logger.info('current mean is %.4f, will exit', curmean)
                    return
                time.sleep(2)
            except:
                logger.error(traceback.format_exc())
                time.sleep(2)

def parsearg():
    global Delay_Time, Hero, Max_Mean, Weight
    parser = argparse.ArgumentParser(description='WashPoint for hero')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to training')
    parser.add_argument('-e', '--hero', type=str, help='hero you want to wash point')
    parser.add_argument('-m', '--max_mean', type=int, default=120, help='max harmonic mean')
    parser.add_argument('-w', '--weight', type=float, nargs=3, default=[1.0, 1.0, 1.0], help='weight of 3 fields')
    parser.add_argument('-i', '--init_point', type=int, nargs=3, help='init point to calc')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Hero= res.hero
    Max_Mean = res.max_mean
    Weight = res.weight
    if res.init_point is not None:
        thread = WashPointThread()
        print thread.get_harmonic_mean(res.init_point)
        sys.exit()
            
if __name__ == '__main__':
    parsearg()
    thread = WashPointThread()
    thread.start()
