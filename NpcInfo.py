#!/usr/local/bin/python
#encoding: utf-8
from sanguo import Sanguo
import time
import Logger
import argparse
import datetime
import util
import sys
import json

logger = Logger.getLogger()

class NpcInfo:
    def __init__(self, nid):
        self.nid = nid
        self.local_time = None
        self.data = self.get_npc_info()

    def check_result(self, res):
        return res.has_key('number')

    def get_npc_info(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                data = {
                        'armyId' : self.nid,
                        'op' : 503,
                    }
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.sendData(data)
                self.local_time = int(time.time())
                sanguo.close()
                if not data:
                    raise Exception()
                if not self.check_result(data):
                    raise Exception()
                return data
            except:
                logger.info('get_npc_info failed, will retry')
                time.sleep(2)
                t += 1

    def raw_print(self):
        print json.dumps(self.data, sort_keys = False, indent = 4)

    def canAttack(self):
        return self.data['canAttack'] == 1

    def getNumber(self):
        return int(self.data['number'])

    def getExploit(self):
        return int(self.data['exploit'])

    def getServerTime(self):
        return int(self.data['serverTime'])

    def getLocalTime(self):
        return self.local_time

    def format_print(self):
        print 'Npc %d Info:'%(self.nid)
        print '\tcanAttack: %s'%('True' if self.canAttack() else 'False')
        print '\tRemain Number: %d'%(self.getNumber())
        print '\tExploit: %d'%(self.getExploit())
        print '\tServerTime: %d'%(self.getServerTime())
        print '\tLocalTime: %d'%(self.local_time)

if __name__ == '__main__':
    gi = NpcInfo(1317)
    gi.format_print()
    #gi.raw_print()
