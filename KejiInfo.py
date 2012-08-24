#!/usr/bin/python
#encoding: utf-8
from sanguo import Sanguo
import time
import Logger
import argparse
import datetime
import util
import sys
import json
from settings import UID,KEJI

class KejiInfo:
    def __init__(self):
        self.data = self.get_keji_info()
        self.kid_dict = {}
        for kinfo in self.data['userTechs']:
            self.kid_dict[kinfo['typeId']] = kinfo
        self.kname_dict = {}
        for k,v in KEJI.items():
            self.kname_dict[v] = k

    def check_result(self, res):
        return res.has_key('userTechs')

    def get_keji_info(self):
        retry = 10
        t = 1
        while t <= retry:
            try:
                sanguo = Sanguo()
                sanguo.login()
                data = sanguo.getKejiInfo()
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

    def get_keji_ids(self):
        for hinfo in self.data['userTechs']:
            yield hinfo['typeId']

    def get_level_by_kid(self, kid):
        return int(self.kid_dict[kid]['level'])

    def format_print(self):
        #print 'Get %d kejis'%(len(self.kid_dict))
        for kid in self.get_keji_ids():
            if self.kname_dict.has_key(kid):
                print 'keji: %s\tLevel: %d'%(self.kname_dict[kid], self.get_level_by_kid(kid))

if __name__ == '__main__':
    ki = KejiInfo()
    ki.format_print()
    #ki.raw_print()
