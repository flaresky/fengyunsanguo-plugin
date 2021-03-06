#!/usr/bin/python
#encoding: utf-8
import threading
import argparse
from sanguo import Sanguo
import time
import Logger
import util
import traceback
import json
from GeneralInfo import GeneralInfo

logger = Logger.getLogger()

Type = None
Delay = 0
Campaign=1
g_previous_armyid = 0

black_list = (
                102, 
                #107, 
                202, 
                #208
                301, 
                401, 
                501, 
            )
op_config = {
            106 : 3017,
            115 : 3017,
            210 : 3017,
            219 : 3017,
            310 : 3017,
            320 : 3017,
            411 : 3017,
            420 : 3017,
            511 : 3017,
            520 : 3017,
            }

class pozenThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False

    def bianzhen(self, keji):
        retry = 10
        t = 1 
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.bianzhen(keji)
                sanguo.close()
                if not data:
                    logger.error('bianzhen failed, data None')
                    raise Exception()
                return data
            except:
                logger.info('bianzhen failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1

    def get_max_level(self, tpe):
        ret = 1
        data = {'op' : 1019}
        res = util.send_data(data, 'userAppoints')
        for ap in res['userAppoints']:
            if int(tpe) == int(ap['type']):
                ret = max(ret, int(ap['appointLevel']))
        return str(ret)

    def get_pozen_info(self, campaignid):
        dicdata = {
                'op' : 3001,
                'campaignId' : int(campaignid)
            }
        retry = 10
        t = 1
        while t <= retry:
            try:
                res = ''
                sanguo = Sanguo()
                sanguo.login()
                sanguo.login()
                data = sanguo.compose_data(dicdata)
                sanguo.tcpClientSock.send(data)
                time.sleep(2)
                res += sanguo.tcpClientSock.recv(4096)
                if len(res) < 5:
                    raise Exception()
                data = util.decode_data(res)
                if not data or len(data) < 1:
                    logger.error('no data')
                    raise Exception()
                sanguo.close()
                return data[1]['armys']
            except:
                time.sleep(2)
                t += 1

    def get_next_id(self, campaignid):
        retry = 10
        while retry > 0:
            retry -= 1
            try:
                res = self.get_pozen_info(campaignid)
                #print json.dumps(res, sort_keys = False, indent = 4)
                #sys.exit()
                for info in res:
                    if info['status'] == 1:
                        armyid = int(info['armyId'])
                        if armyid not in black_list:
                            return armyid
                return -1
            except:
                time.sleep(3)

    def do_pozen(self, armyid):
        retry = 10
        t = 1 
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = None
                if op_config.has_key(armyid):
                    data = sanguo.pozen(armyid, op_config[armyid])
                else:
                    data = sanguo.pozen(armyid)
                sanguo.close()
                if not data:
                    logger.error('pozen failed, data None')
                    raise Exception()
                logger.info('pozen succeed')
                return data
            except:
                logger.info('do_pozen failed, will sleep %d seconds'%(t*2))
                time.sleep(t*2)
                t += 1

    def run(self):
        global g_previous_armyid
        logger.info('pozen Thread start, will pozen campaign %s'%(str(Campaign)))
        if Delay_Time > 0:
            logger.info('I will start pozen at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        #self.bianzhen('yanxing')
        time.sleep(2)
        for campaignid in Campaign:
            while True:
                try:
                    #res = self.get_pozen_info(2)
                    #print json.dumps(res, sort_keys = False, indent = 4)
                    #return
                    armyid = self.get_next_id(campaignid)
                    if armyid is None:
                        logger.info('pozen network error')
                        time.sleep(2)
                        continue
                    elif armyid == -1:
                        logger.info('pozen %d finished'%(campaignid))
                        break
                    elif armyid == g_previous_armyid:
                        logger.info('pozen %d falied, %d lose'%(campaignid,  armyid))
                        return
                    g_previous_armyid = armyid
                    time.sleep(2)
                    logger.info('pozen army %d'%(armyid))
                    res = self.do_pozen(armyid)
                    if res.has_key('exception'):
                        logger.error('Got Exception "%s"'%(res['exception']['message']))
                        if 'waittingOrder' == res['exception']['message']:
                            gi = GeneralInfo()
                            sp = util.get_sleep_time(gi.get_mobility_CDTime(), gi.get_localTime()-gi.get_serverTime())
                            logger.info('I will sleep for mobility CD to %s'%(util.next_time(sp)))
                            time.sleep(sp)
                            g_previous_armyid = 0
                            continue
                        return
                    time.sleep(2)
                except:
                    logger.info(traceback.format_exc())
                    time.sleep(10)

def parsearg():
    global Delay_Time, Campaign
    parser = argparse.ArgumentParser(description='pozen')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to pozen')
    parser.add_argument('-c', '--campagins', type=int, nargs='*', default=[5], help='')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    Campaign = res.campagins
            
if __name__ == '__main__':
    parsearg()
    pozenthread = pozenThread()
    pozenthread.start()
