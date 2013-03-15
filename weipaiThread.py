#!/usr/local/bin/python
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
MaxLevel = None
SellColor = None
TotalCost = 0

class RoundControl:
    def __init__(self):
        self.last_level = 0
        self.repeat_count = 0

    def can_continue(self, level):
        #return True
        level = int(level)
        if level > self.last_level:
            self.repeat_count = 0
            self.last_level = level
            return True
        elif level == self.last_level:
            self.repeat_count += 1
            if self.repeat_count >= 4:
                return False
            else:
                return True
        else:
            self.last_level = level
            return False

    def reset(self):
        self.last_level = 0
        self.repeat_count = 0

class weipaiThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = False

    def add_cost(self, tpe, level):
        global TotalCost
        cost_map = {
                '3' : {
                        '1' : 8000,
                        '2' : 11000,
                        '3' : 25000,
                        '4' : 40000,
                    },
                '4' : {
                        '1' : 10000,
                        '2' : 18000,
                        '3' : 30000,
                        '4' : 60000,
                    },
            }
        try:
            TotalCost += cost_map[str(tpe)][str(level)]
        except:
            pass

    def get_max_level(self, tpe):
        ret = 1
        data = {'op' : 1019}
        res = util.send_data(data, 'userAppoints')
        for ap in res['userAppoints']:
            if int(tpe) == int(ap['type']):
                ret = max(ret, int(ap['appointLevel']))
        return str(ret)

    def do_weipai(self, tpe, level):
        dicdata = {
                'level' : str(level),
                'op' : 1021,
                'type' : str(tpe),
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
                #res += sanguo.tcpClientSock.recv(1024)
                time.sleep(2)
                res += sanguo.tcpClientSock.recv(4096)
                if len(res) < 5:
                    raise Exception()
                data = util.decode_data(res)
                if not data or len(data) < 1:
                    logger.error('no data')
                    raise Exception()
                sanguo.close()
                if not data[0].has_key('exception'):
                    self.add_cost(tpe, level)
                return data
            except:
                #logger.error(traceback.format_exc())
                time.sleep(2)
                t += 1

    def sell(self, id, price=0):
        global TotalCost
        data = {'op' : 1023, 'id' : str(id)}
        res = util.send_data(data)
        if res:
            TotalCost -= int(price)
        logger.info('sell equip %s succeed'%(id))
    
    def run(self):
        logger.info('weipai Thread start, will weipai type %s'%(Type))
        if Delay_Time > 0:
            logger.info('I will start weipai at ' + util.next_time(Delay_Time))
            time.sleep(Delay_Time)
        cnt = 1
        first_time = True
        rc = RoundControl()
        while True:
            try:
                ml = self.get_max_level(Type)
                if first_time:
                    first_time = False
                else:
                    if int(ml) >= MaxLevel:
                        msg = 'Weipai reach max level %s, TotalCost %d'%(ml, TotalCost)
                        logger.info(msg)
                        util.notify(msg)
                        break
                logger.info('Type:%s MaxLevel:%s'%(Type, ml))
                if not rc.can_continue(ml):
                    rc.reset()
                    gi = GeneralInfo()
                    sp = gi.get_weipai_CDTime() - gi.get_serverTime() - 15
                    logger.info('Break by RoundControl, Next round weipai will start at ' + util.next_time(sp))
                    time.sleep(sp)
                    continue
                res = self.do_weipai(Type, ml)
                if res[0].has_key('exception'):
                    msg = res[0]['exception']['message']
                    logger.info('got exception %s, TotalCost %d'%(msg, TotalCost))
                    if msg == 'CDTimeNotCool':
                        gi = GeneralInfo()
                        sp = gi.get_weipai_CDTime() - gi.get_serverTime()
                        logger.info('Next round weipai will start at ' + util.next_time(sp))
                        time.sleep(sp)
                        continue
                    elif msg == 'maintenance':
                        logger.info('Got Exception %s'%(msg))
                        sp = 3600
                        logger.info('Next round weipai will start at ' + util.next_time(sp))
                        time.sleep(sp)
                        continue
                    else:
                        logger.info('Exit for Exception %s'%(msg))
                        break
                try:
                    eq = res[1]['resArr']['userEquip']
                    logger.info('Got Equip level=%s id=%s color=%s name=%s salePrice=%s maxPiece=%s currPiece=%s'%(ml, eq['id'], eq['type']['color'], eq['type']['name'], eq['type']['salePrice'], eq['maxPiece'], eq['currPiece']))
                    price = int(eq['type']['salePrice']) * int(eq['currPiece']) / int(eq['maxPiece'])
                    if int(eq['type']['color']) <= SellColor:
                        self.sell(eq['id'], price)
                    else:
                        if int(eq['type']['color']) > 5:
                            msg = 'Got Equip %s %s/%s, TotalCost %d'%(eq['type']['name'], eq['currPiece'], eq['maxPiece'], TotalCost)
                            logger.info(msg)
                            util.notify(msg)
                        else:
                            logger.info('I will keep it')
                except:
                    pass
                logger.info('finished %d time, TotalCost %d'%(cnt, TotalCost))
                cnt += 1
                time.sleep(2)
            except:
                logger.info(traceback.format_exc())
                time.sleep(10)

def parsearg():
    global Delay_Time, Type, MaxLevel, SellColor
    parser = argparse.ArgumentParser(description='weipai')
    parser.add_argument('-d', '--delay', required=False, type=str, default='0', metavar='4:23', help='the time will delay to weipai')
    parser.add_argument('-t', '--type', required=False, type=str, default='ma', help='weipai type')
    parser.add_argument('-l', '--max_level', required=False, type=int, default=5, help='got max level will exit')
    parser.add_argument('-s', '--sell_color', required=False, type=int, default=6, help='will sell all color less or equal')
    res = parser.parse_args()
    dlist = res.delay.split(':')
    if len(dlist) == 1:
        Delay_Time = int(dlist[0]) * 60
    elif len(dlist) == 2:
        Delay_Time = int(dlist[0]) * 3600 + int(dlist[1]) * 60
    if res.type == 'ma':
        Type = '3'
    else:
        Type = '4'
    MaxLevel = res.max_level
    SellColor = res.sell_color
            
if __name__ == '__main__':
    parsearg()
    weipaithread = weipaiThread()
    weipaithread.start()
