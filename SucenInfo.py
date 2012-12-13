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

class SucenInfo:
    def __init__(self):
        self.local_time = None
        self.data = self.get_sucen_info()
        self.sdict = {}
        for sc in self.data['subjects']:
            self.sdict[sc['id']] = sc

    def check_result(self, res):
        return res.has_key('subjects')

    def get_sucen_info(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.get_sucen()
                self.local_time = int(time.time())
                sanguo.close()
                if not data:
                    raise Exception()
                if not self.check_result(data):
                    raise Exception()
                return data
            except:
                time.sleep(2)
                t += 1

    def raw_print(self):
        print json.dumps(self.data, sort_keys = False, indent = 4)

    def getSucenIds(self):
        for sc in self.data['subjects']:
            yield sc['id']

    def getNameById(self, id):
        return self.sdict[id]['name']

    def getLevelById(self, id):
        return int(self.sdict[id]['level'])

    def getContributeById(self, id):
        return int(self.sdict[id]['contribute'])

    def getLastContributeById(self, id):
        return int(self.sdict[id]['lastContribute'])

    def getServerTime(self):
        return int(self.data['serverTime'])

    def getLocalTime(self):
        return self.local_time

    def format_print(self):
        print 'Sucen Info:'
        for sid in self.getSucenIds():
            print '\tName:%s\tLevel:%d\tLastTime:%s\tContribute:%d'%(self.getNameById(sid), self.getLevelById(sid), util.format_time(self.getLastContributeById(sid)), self.getContributeById(sid))

if __name__ == '__main__':
    gi = SucenInfo()
    gi.format_print()
    #gi.raw_print()
